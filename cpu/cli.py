import logging
logging.getLogger().setLevel(logging.ERROR)

import _patch_env  # noqa: F401

import argparse
from pathlib import Path
from basic_pitch.inference import predict_and_save
from basic_pitch import ICASSP_2022_MODEL_PATH

def main():
    parser = argparse.ArgumentParser(
        description="Basic Pitch CLI Converter - audio to MIDI with advanced options"
    )
    parser.add_argument("output_dir", type=str, help="Output directory for results")
    parser.add_argument("audio_files", nargs="+", help="Input audio files (wav, mp3)")
    parser.add_argument("--save-midi", action="store_true", default=True,
                        help="Save MIDI file (default: enabled)")
    parser.add_argument("--save-notes", action="store_true", default=False,
                        help="Save notes CSV (default: disabled)")
    parser.add_argument("--save-model-outputs", action="store_true",
                        help="Save model outputs NPZ")
    parser.add_argument("--sonify-midi", action="store_true",
                        help="Generate audio preview WAV")
    parser.add_argument("--overwrite", action="store_true",
                        help="Overwrite existing files by deleting old outputs")
    parser.add_argument("--onset-threshold", type=float, default=0.5,
                        help="Onset threshold (0-1, default 0.5)")
    parser.add_argument("--frame-threshold", type=float, default=0.3,
                        help="Frame threshold (0-1, default 0.3)")
    parser.add_argument("--minimum-note-length", type=float, default=127.7,
                        help="Minimum note length in ms (default 127.7)")
    parser.add_argument("--minimum-frequency", type=float, default=50.0,
                        help="Minimum frequency in Hz (default 50)")
    parser.add_argument("--maximum-frequency", type=float, default=5000.0,
                        help="Maximum frequency in Hz (default 5000)")
    args = parser.parse_args()

    output_path = Path(args.output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    if args.overwrite:
        for f in args.audio_files:
            stem = Path(f).stem
            if args.save_midi:
                (output_path / f"{stem}_basic_pitch.mid").unlink(missing_ok=True)
            if args.save_model_outputs:
                (output_path / f"{stem}_basic_pitch.npz").unlink(missing_ok=True)
            if args.sonify_midi:
                (output_path / f"{stem}_basic_pitch.wav").unlink(missing_ok=True)
            if args.save_notes:
                (output_path / f"{stem}_basic_pitch.csv").unlink(missing_ok=True)

    predict_and_save(
        [Path(f) for f in args.audio_files],
        output_path,
        sonify_midi=args.sonify_midi,
        model_or_model_path=ICASSP_2022_MODEL_PATH,
        save_midi=args.save_midi,
        save_model_outputs=args.save_model_outputs,
        save_notes=args.save_notes,
        onset_threshold=args.onset_threshold,
        frame_threshold=args.frame_threshold,
        minimum_note_length=args.minimum_note_length,
        minimum_frequency=args.minimum_frequency,
        maximum_frequency=args.maximum_frequency
    )

if __name__ == "__main__":
    main()
