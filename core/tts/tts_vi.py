"""VieNeu Vietnamese TTS: python core/tts/tts_vi.py lines.json out_dir [--voice "Trúc Ly"] [--speed 1.0] [--sr 24000]
lines.json = [{"id":..., "text":..., "voice":"Trúc Ly", "speed":1.0, "say":"...", "ref_audio":"..."}, ...]
  "say" (optional) = the text actually spoken if it differs from subtitles text (e.g. spelling out numbers).
  "voice" = preset voice name or voice ID (use --list-voices to view all 25+ voices).
  "ref_audio" (optional) = audio file path for zero-shot voice cloning.

Outputs: out_dir/<id>.wav (mono, trimmed) and out_dir/dur.json.
Cached in out_dir/.cache/ so unchanged lines are not re-synthesized.
"""
import sys, io, json, os, re, hashlib, argparse
import numpy as np, soundfile as sf

DEFAULT_VOICE = 'Trúc Ly'
DEFAULT_SR = 24000


def get_engine(mode='v3turbo', precision=None):
    try:
        from vieneu import Vieneu
    except ImportError:
        sys.exit(
            "tts_vi.py: 'vieneu' package is missing.\n"
            "  Install it with: pip install vieneu"
        )
    kwargs = {}
    if precision:
        kwargs['precision'] = precision
    return Vieneu(mode=mode, **kwargs)


def list_preset_voices():
    """Print all available preset voices with details."""
    try:
        from vieneu import Vieneu
        engine = Vieneu()
        voices = engine.list_preset_voices()
        print("\n🎙️ VieNeu-TTS Preset Voices (25+ giọng nói theo Vùng Miền & Giới Tính):")
        print("=" * 70)
        for label, vid in voices:
            print(f"  • {vid:<16} | {label}")
        print("=" * 70)
        print("Sử dụng: python core/tts/tts_vi.py lines.json out_dir --voice \"<Tên Giọng>\"\n")
    except Exception as e:
        sys.exit(f"tts_vi.py: Không thể lấy danh sách giọng: {e}")


def resample_audio(y, orig_sr, target_sr):
    if orig_sr == target_sr:
        return y
    try:
        import soxr
        return soxr.resample(y, orig_sr, target_sr)
    except ImportError:
        pass
    try:
        import librosa
        return librosa.resample(y, orig_sr=orig_sr, target_sr=target_sr)
    except ImportError:
        pass
    from scipy.signal import resample
    num_samples = int(round(len(y) * float(target_sr) / orig_sr))
    return resample(y, num_samples).astype(np.float32)


def trim_silence(a, sr, top_db_threshold=0.02):
    max_amp = np.abs(a).max() if len(a) else 0
    if max_amp == 0:
        return a
    threshold = max_amp * top_db_threshold
    nz = np.where(np.abs(a) > threshold)[0]
    if len(nz):
        pad_start = int(0.03 * sr)
        pad_end = int(0.08 * sr)
        return a[max(0, nz[0] - pad_start): min(len(a), nz[-1] + pad_end)]
    return a


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('lines', nargs='?', help='Path to lines.json')
    ap.add_argument('out_dir', nargs='?', help='Output directory for audio files')
    ap.add_argument('--voice', default=DEFAULT_VOICE, help=f'Default voice (default: {DEFAULT_VOICE})')
    ap.add_argument('--speed', type=float, default=1.0, help='Speech speed multiplier (default 1.0)')
    ap.add_argument('--mode', default='v3turbo', choices=['v3turbo', 'v3nano'], help='Model mode (default v3turbo)')
    ap.add_argument('--sr', type=int, default=DEFAULT_SR, help=f'Target sample rate (default {DEFAULT_SR} Hz)')
    ap.add_argument('--ref-audio', default=None, help='Reference audio for voice cloning')
    ap.add_argument('--list-voices', action='store_true', help='List all available preset voices and exit')
    ap.add_argument('--no-cache', action='store_true', help='Disable caching of generated audio')

    args = ap.parse_args()

    if args.list_voices:
        list_preset_voices()
        sys.exit(0)

    if not args.lines or not args.out_dir:
        ap.print_help()
        sys.exit(2)

    if not os.path.exists(args.lines):
        sys.exit(f"tts_vi.py: Không tìm thấy file lines: {args.lines}")

    with open(args.lines, encoding='utf-8') as f:
        lines = json.load(f)

    os.makedirs(args.out_dir, exist_ok=True)
    cache_dir = os.path.join(args.out_dir, '.cache')
    if not args.no_cache:
        os.makedirs(cache_dir, exist_ok=True)

    print(f"Khởi tạo VieNeu ({args.mode})...")
    engine = get_engine(mode=args.mode)
    native_sr = 48000 if args.mode == 'v3turbo' else 24000

    dur = {}
    total_lines = len(lines)

    for idx, L in enumerate(lines, 1):
        lid = L['id']
        voice = L.get('voice', args.voice)
        speed = float(L.get('speed', args.speed))
        ref_audio = L.get('ref_audio', args.ref_audio)
        say = L.get('say', L.get('text', ''))

        wav_out = os.path.join(args.out_dir, f"{lid}.wav")

        # Cache key based on all synthesis parameters
        cache_key = hashlib.sha1(
            json.dumps([args.mode, voice, speed, say, args.sr, ref_audio], ensure_ascii=False).encode('utf-8')
        ).hexdigest()[:16]
        cached_wav = os.path.join(cache_dir, f"{cache_key}.wav")

        if not args.no_cache and os.path.exists(cached_wav):
            y, sr = sf.read(cached_wav, dtype='float32')
            sf.write(wav_out, y, sr)
            line_dur = round(len(y) / sr, 3)
            dur[lid] = line_dur
            print(f"[{idx}/{total_lines}] (cache) {lid}: {line_dur:.2f}s | {voice} | {say}")
            continue

        infer_kwargs = {}
        if voice:
            infer_kwargs['voice'] = voice
        if ref_audio:
            infer_kwargs['ref_audio'] = ref_audio

        # Synthesize audio using VieNeu
        audio_arr = engine.infer(say, **infer_kwargs)
        if isinstance(audio_arr, np.ndarray):
            y = audio_arr.astype(np.float32)
        else:
            y = np.array(audio_arr, dtype=np.float32)

        # Resample if needed
        if args.sr != native_sr:
            y = resample_audio(y, native_sr, args.sr)
            curr_sr = args.sr
        else:
            curr_sr = native_sr

        # Trim leading / trailing silence
        y = trim_silence(y, curr_sr)

        # Normalize volume gently if max is high
        m = np.abs(y).max() if len(y) else 0
        if m > 0.98:
            y = y * (0.95 / m)

        # Save to output and cache
        sf.write(wav_out, y, curr_sr)
        if not args.no_cache:
            sf.write(cached_wav, y, curr_sr)

        line_dur = round(len(y) / curr_sr, 3)
        dur[lid] = line_dur
        print(f"[{idx}/{total_lines}] ✓ {lid}: {line_dur:.2f}s | {voice} | {say}")

    dur_path = os.path.join(args.out_dir, 'dur.json')
    with open(dur_path, 'w', encoding='utf-8') as f:
        json.dump(dur, f, indent=1, ensure_ascii=False)

    print(f"\n Hoàn tất! Đã lưu {total_lines} câu thoại vào '{args.out_dir}/' và thời lượng vào '{dur_path}'.")


if __name__ == '__main__':
    main()
