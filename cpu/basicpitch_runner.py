from pathlib import Path
import numpy as np
import _patch_env  # noqa: F401
from basic_pitch.inference import predict, build_output_path, OutputExtensions, save_note_events, ICASSP_2022_MODEL_PATH
import basic_pitch.note_creation as infer
from basic_pitch.commandline_printing import file_saved_confirmation, failed_to_save


def merge_notes(note_events, threshold_ms):
    if threshold_ms <= 0 or len(note_events) < 2:
        return note_events
    threshold_s = threshold_ms / 1000.0
    by_pitch = {}
    for start, end, pitch, vel, bends in note_events:
        by_pitch.setdefault(pitch, []).append([start, end, vel, bends])
    merged = []
    for pitch, notes in by_pitch.items():
        notes.sort(key=lambda x: x[0])
        cur = notes[0]
        for n in notes[1:]:
            if n[0] - cur[1] <= threshold_s:
                cur[1] = max(cur[1], n[1])
            else:
                merged.append((cur[0], cur[1], pitch, cur[2], cur[3]))
                cur = n
        merged.append((cur[0], cur[1], pitch, cur[2], cur[3]))
    merged.sort(key=lambda x: x[0])
    return merged


def run_basicpitch(audio_files, output_path, options, progress_callback,
                   original_name=None, merge_threshold_ms=0):
    processed = []
    for f in audio_files:
        src = Path(f)
        if original_name:
            parts = src.stem.split(".")
            stem_part = parts[1] if len(parts) > 1 else parts[0]
            clean_name = f"{original_name}.{stem_part}{src.suffix}"
            dst = src.parent / clean_name
            if not dst.exists():
                src.rename(dst)
            processed.append(dst)
            stem = dst.stem
        else:
            processed.append(src)
            stem = src.stem

    for f in processed:
        s = Path(f).stem
        if options["save_midi"]:
            (output_path / f"{s}_basic_pitch.mid").unlink(missing_ok=True)
        if options["save_outputs"]:
            (output_path / f"{s}_basic_pitch.npz").unlink(missing_ok=True)
        if options["sonify"]:
            (output_path / f"{s}_basic_pitch.wav").unlink(missing_ok=True)
        if options["save_notes"]:
            (output_path / f"{s}_basic_pitch.csv").unlink(missing_ok=True)

    progress_callback(85, "Basic Pitch processing...")
    for f in processed:
        model_output, midi_data, note_events = predict(
            f,
            ICASSP_2022_MODEL_PATH,
            onset_threshold=options["onset_threshold"],
            frame_threshold=options["frame_threshold"],
            minimum_note_length=options["min_note_length"],
            minimum_frequency=options["min_freq"],
            maximum_frequency=options["max_freq"],
        )

        if merge_threshold_ms > 0:
            note_events = merge_notes(note_events, merge_threshold_ms)
            midi_data = infer.note_events_to_midi(note_events)

        s = f.stem

        if options["save_outputs"]:
            npz_path = build_output_path(f, output_path, OutputExtensions.MODEL_OUTPUT_NPZ)
            try:
                np.savez(npz_path, basic_pitch_model_output=model_output)
                file_saved_confirmation(OutputExtensions.MODEL_OUTPUT_NPZ.name, npz_path)
            except Exception as e:
                failed_to_save(OutputExtensions.MODEL_OUTPUT_NPZ.name, npz_path)
                raise e

        if options["save_midi"]:
            midi_path = build_output_path(f, output_path, OutputExtensions.MIDI)
            try:
                midi_data.write(str(midi_path))
                file_saved_confirmation(OutputExtensions.MIDI.name, midi_path)
            except Exception as e:
                failed_to_save(OutputExtensions.MIDI.name, midi_path)
                raise e

        if options["sonify"]:
            wav_path = build_output_path(f, output_path, OutputExtensions.MIDI_SONIFICATION)
            try:
                infer.sonify_midi(midi_data, wav_path)
                file_saved_confirmation(OutputExtensions.MIDI_SONIFICATION.name, wav_path)
            except Exception as e:
                failed_to_save(OutputExtensions.MIDI_SONIFICATION.name, wav_path)
                raise e

        if options["save_notes"]:
            csv_path = build_output_path(f, output_path, OutputExtensions.NOTE_EVENTS)
            try:
                save_note_events(note_events, csv_path)
                file_saved_confirmation(OutputExtensions.NOTE_EVENTS.name, csv_path)
            except Exception as e:
                failed_to_save(OutputExtensions.NOTE_EVENTS.name, csv_path)
                raise e

    progress_callback(100, "Done")
