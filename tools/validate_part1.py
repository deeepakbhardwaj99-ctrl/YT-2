"""Validate metadata/accepted assets without mistaking reference crops for production plates."""
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]

def validate(require_complete=False):
    scenes = json.loads((ROOT / 'production/scenes.json').read_text())['part1_clips']
    manifest = json.loads((ROOT / 'production/part1/background_manifest.json').read_text())
    vo = json.loads((ROOT / 'production/part1/part1_vo_manifest.json').read_text())['clips']
    accepted = {(p['clip_id'], p['shot_index']): p for p in manifest['plates']}
    assert len(accepted) == len(manifest['plates']), 'Duplicate asset record'
    assert len(scenes) == len(vo) == 25
    assert (ROOT / 'production/script_approved.txt').read_bytes() == (ROOT / 'trojan_war_script_20min_with_dialogue.txt').read_bytes(), 'Locked script changed'
    seen, digests, pending = set(), set(), []
    for clip, source in zip(scenes, vo):
        assert clip['clip_id'] == source['clip_id']
        assert clip['vo_segments'] == source['segments'], 'VO text/timing changed'
        assert clip['duration_s'] == source['duration_s']
        assert clip['overlay_card']['emphasis'] in clip['overlay_card']['headline']
        assert len(clip['shots']) == 5
        end = 0
        for shot in clip['shots']:
            assert abs(shot['t_start'] - end) < .002, 'Gap/overlap in shots'
            assert shot['t_end'] > shot['t_start']
            end = shot['t_end']
            path = shot['bg_path']
            assert path not in seen, 'Reused background masquerading as unique plate'
            seen.add(path)
            assert (ROOT / shot['reference_path']).is_file()
            entry = accepted.get((clip['clip_id'], shot['shot_index']))
            if entry:
                assert shot['asset_status'] == entry['qc_status'] == 'accepted'
                assert entry['path'] == path
                data = (ROOT / path).read_bytes()
                digest = hashlib.sha256(data).hexdigest()
                assert digest == entry['sha256'] and digest not in digests
                digests.add(digest)
                with Image.open(ROOT / path) as im:
                    assert list(im.size) == entry['dimensions']
                    assert abs(im.width / im.height - 16/9) < .03
                    im.verify()
            else:
                assert shot['asset_status'] == 'pending_generation'
                pending.append(path)
        assert abs(end - clip['duration_s']) < .002
    result = {'script_verbatim': True, 'vo_segments_unchanged': True,
              'planned_unique_plates': len(seen), 'accepted_plates': len(accepted),
              'pending_plates': len(pending), 'full_render_ready': not pending}
    if require_complete and pending:
        raise ValueError(f'Full render blocked: {len(pending)} production backgrounds pending')
    return result

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--require-complete', action='store_true')
    args = p.parse_args()
    print(json.dumps(validate(args.require_complete), indent=2))
