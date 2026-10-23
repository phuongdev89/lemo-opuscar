"""TTS generator for Tuoi Me Con supporting both VieNeu-TTS (offline neural) and Edge-TTS.

Usage:
  python films/tuoi-me-con/tts_vn.py [--engine vieneu|edge] [--voice "Trúc Ly"] [--force] [--list-voices]
"""
import sys, io, json, os, asyncio, subprocess, argparse
import numpy as np, soundfile as sf

SR = 24000
DEFAULT_VIENEU_VOICE = 'Trúc Ly'   # Nữ · Bắc · Phong cách tự nhiên
DEFAULT_EDGE_VOICE = 'vi-VN-HoaiMyNeural'

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
lines_path = os.path.join(HERE, 'lines.json')
out_dir = os.path.join(HERE, 'voices')


def run_vieneu(lines, voice, force=False):
    print(f"🎙️ Đang sinh giọng với VieNeu-TTS (Giọng: {voice})...")
    from core.tts.tts_vi import get_engine, trim_silence, resample_audio

    engine = get_engine(mode='v3turbo')
    native_sr = 48000
    os.makedirs(out_dir, exist_ok=True)
    dur = {}

    for idx, L in enumerate(lines, 1):
        lid = L['id']
        wav_path = os.path.join(out_dir, f"{lid}.wav")
        say = L.get('say', L['text'])

        if not force and os.path.exists(wav_path):
            y, sr = sf.read(wav_path)
            dur[lid] = round(len(y) / sr, 3)
            print(f"[{idx}/{len(lines)}] (sẵn có) {lid}: {dur[lid]}s - {L['text']}")
            continue

        audio_arr = engine.infer(say, voice=voice)
        y = np.array(audio_arr, dtype=np.float32)
        if SR != native_sr:
            y = resample_audio(y, native_sr, SR)
        y = trim_silence(y, SR)

        sf.write(wav_path, y, SR)
        dur[lid] = round(len(y) / SR, 3)
        print(f"[{idx}/{len(lines)}] ✓ {lid}: {dur[lid]}s - {L['text']}")

    dur_path = os.path.join(out_dir, 'dur.json')
    json.dump(dur, open(dur_path, 'w', encoding='utf-8'), indent=1)
    print(f" Hoàn tất với VieNeu! Đã ghi {dur_path}")


async def run_edge(lines, voice, force=False):
    import edge_tts
    print(f"🎙️ Đang sinh giọng với Edge-TTS (Giọng: {voice})...")
    os.makedirs(out_dir, exist_ok=True)
    dur = {}

    async def generate_line(text, path):
        for attempt in range(5):
            try:
                comm = edge_tts.Communicate(text, voice)
                await comm.save(path)
                if os.path.getsize(path) > 100:
                    return True
            except Exception as e:
                print(f"Retry {attempt+1} on {text[:20]}...: {e}", file=sys.stderr)
                await asyncio.sleep(2.0 * (attempt + 1))
        return False

    def to_wav(mp3):
        r = subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', mp3, '-ar', str(SR), '-ac', '1', '-f', 'wav', '-'], capture_output=True, check=True)
        a, sr = sf.read(io.BytesIO(r.stdout), dtype='float32')
        return a, sr

    for idx, L in enumerate(lines, 1):
        lid = L['id']
        wav_path = os.path.join(out_dir, f"{lid}.wav")
        mp3_path = os.path.join(out_dir, f"{lid}.mp3")
        say = L.get('say', L['text'])

        if not force and os.path.exists(wav_path):
            y, sr = sf.read(wav_path)
            dur[lid] = round(len(y) / sr, 3)
            print(f"[{idx}/{len(lines)}] (sẵn có) {lid}: {dur[lid]}s - {L['text']}")
            continue

        ok = await generate_line(say, mp3_path)
        if not ok:
            sys.exit(f"Failed to generate Edge-TTS for {lid}")
        await asyncio.sleep(0.5)
        y, sr = to_wav(mp3_path)

        nz = np.where(np.abs(y) > (np.abs(y).max() if len(y) else 0) * .02)[0]
        if len(nz):
            y = y[max(0, nz[0] - int(.03 * sr)): nz[-1] + int(.10 * sr)]
        sf.write(wav_path, y, sr)
        if os.path.exists(mp3_path):
            os.remove(mp3_path)

        dur[lid] = round(len(y) / sr, 3)
        print(f"[{idx}/{len(lines)}] ✓ {lid}: {dur[lid]}s - {L['text']}")

    dur_path = os.path.join(out_dir, 'dur.json')
    json.dump(dur, open(dur_path, 'w', encoding='utf-8'), indent=1)
    print(f" Hoàn tất với Edge-TTS! Đã ghi {dur_path}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--engine', choices=['vieneu', 'edge'], default='vieneu', help='TTS engine (default: vieneu)')
    parser.add_argument('--voice', default=None, help='Voice name/ID')
    parser.add_argument('--force', action='store_true', help='Re-generate even if audio files exist')
    parser.add_argument('--list-voices', action='store_true', help='List all available VieNeu voices')

    args = parser.parse_args()

    if args.list_voices:
        from core.tts.tts_vi import list_preset_voices
        list_preset_voices()
        return

    with open(lines_path, encoding='utf-8') as f:
        lines = json.load(f)

    if args.engine == 'vieneu':
        v = args.voice or DEFAULT_VIENEU_VOICE
        run_vieneu(lines, v, force=args.force)
    else:
        v = args.voice or DEFAULT_EDGE_VOICE
        asyncio.run(run_edge(lines, v, force=args.force))


if __name__ == '__main__':
    main()
