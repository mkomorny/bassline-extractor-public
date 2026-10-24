#!/usr/bin/env python3
"""
Bassline Audio-to-MIDI Extractor
Specialized low-end bassline extraction powered by Spotify Basic Pitch.

Features:
- Strict frequency clamping (28 Hz - 320 Hz, rejecting guitars/cymbals/vocals).
- Low onset threshold (0.45) to reliably capture deep 808 subs and sub-bass fundamental.
- Sub-bass note-gap merging (prevents choppy, fragmented bass notes).
- Monophonic single-voice enforcement.
"""

import os
import sys
import warnings
import logging
import json
import argparse
import importlib.util
import subprocess
from pathlib import Path

warnings.filterwarnings("ignore")
os.environ["PYTHONWARNINGS"] = "ignore"
logging.basicConfig(level=logging.ERROR)
logging.getLogger().setLevel(logging.ERROR)

BASIC_PITCH_PYTHON = r"C:\Users\<you>\AppData\Roaming\uv\tools\basic-pitch\Scripts\python.exe"

# Auto re-exec in dedicated uv environment if needed
if not importlib.util.find_spec("basic_pitch"):
    if os.path.exists(BASIC_PITCH_PYTHON) and sys.executable.lower() != BASIC_PITCH_PYTHON.lower():
        result = subprocess.run([BASIC_PITCH_PYTHON] + sys.argv)
        sys.exit(result.returncode)

import numpy as np
import pretty_midi
from basic_pitch.inference import predict
from basic_pitch import ICASSP_2022_MODEL_PATH


def clean_bass_monophonic_and_merge(instrument: pretty_midi.Instrument, merge_gap_s: float = 0.08) -> None:
    """Clean bass notes: enforce monophony and merge same-pitch notes across micro-gaps."""
    if not instrument.notes:
        return

    notes = sorted(instrument.notes, key=lambda n: (n.start, n.pitch))
    cleaned = []

    # First pass: merge identical consecutive pitches if separated by a tiny gap (e.g. legato sustain flutter)
    merged = []
    i = 0
    while i < len(notes):
        curr = notes[i]
        j = i + 1
        while j < len(notes) and notes[j].pitch == curr.pitch and notes[j].start - curr.end <= merge_gap_s:
            curr.end = max(curr.end, notes[j].end)
            curr.velocity = max(curr.velocity, notes[j].velocity)
            j += 1
        merged.append(curr)
        i = j

    # Second pass: enforce strict monophonic progression (no overlapping notes)
    for k in range(len(merged)):
        curr_note = merged[k]
        if k + 1 < len(merged):
            next_note = merged[k + 1]
            if curr_note.end > next_note.start:
                curr_note.end = max(curr_note.start + 0.05, next_note.start - 0.005)
        if curr_note.end > curr_note.start + 0.03:
            cleaned.append(curr_note)

    instrument.notes = cleaned


def extract_bassline(
    audio_path: str,
    output_midi_path: str = None,
    onset_threshold: float = 0.45,
    frame_threshold: float = 0.30,
    min_note_length: float = 100.0,
    min_frequency: float = 28.0,     # ~A0
    max_frequency: float = 320.0,    # ~E4
    merge_gap: float = 0.08,
    no_bends: bool = False
) -> dict:
    audio_file = Path(audio_path).resolve()
    if not audio_file.exists():
        raise FileNotFoundError(f"Audio file not found: {audio_file}")

    if output_midi_path is None:
        output_midi_path = audio_file.with_name(f"{audio_file.stem}_bassline.mid")
    else:
        output_midi_path = Path(output_midi_path).resolve()

    output_midi_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"\n[*] Extracting Bassline MIDI: {audio_file.name}")
    print(f"    Low-End Bounds: {min_frequency} Hz - {max_frequency} Hz")
    print(f"    Thresholds: Onset={onset_threshold}, Frame={frame_threshold}, MinLen={min_note_length}ms")

    model_output, midi_data, note_events = predict(
        audio_path=str(audio_file),
        model_or_model_path=ICASSP_2022_MODEL_PATH,
        onset_threshold=onset_threshold,
        frame_threshold=frame_threshold,
        minimum_note_length=min_note_length,
        minimum_frequency=min_frequency,
        maximum_frequency=max_frequency,
        multiple_pitch_bends=False,
        melodia_trick=True
    )

    for inst in midi_data.instruments:
        clean_bass_monophonic_and_merge(inst, merge_gap_s=merge_gap)
        if no_bends:
            inst.pitch_bends = []

    midi_data.write(str(output_midi_path))
    total_notes = sum(len(i.notes) for i in midi_data.instruments)
    print(f"[+] Bassline MIDI saved: {output_midi_path} ({total_notes} notes extracted)")

    return {
        "audio_path": str(audio_file),
        "midi_path": str(output_midi_path),
        "total_notes": total_notes
    }


def main():
    parser = argparse.ArgumentParser(description="Bassline Audio-to-MIDI Extractor (Spotify Basic Pitch)")
    parser.add_argument("audio_path", help="Path to bass audio file or stem (WAV, MP3, FLAC)")
    parser.add_argument("--output", "-o", help="Path to output .mid file")
    parser.add_argument("--onset", type=float, default=0.45, help="Onset threshold (default 0.45)")
    parser.add_argument("--frame", type=float, default=0.30, help="Frame sustain threshold (default 0.30)")
    parser.add_argument("--min-len", type=float, default=100.0, help="Minimum note length in ms")
    parser.add_argument("--min-freq", type=float, default=28.0, help="Minimum sub frequency in Hz (default 28)")
    parser.add_argument("--max-freq", type=float, default=320.0, help="Maximum bass frequency in Hz (default 320)")
    parser.add_argument("--merge-gap", type=float, default=0.08, help="Gap in seconds to merge same-pitch flutter")
    parser.add_argument("--no-bends", action="store_true", help="Strip pitch bends for clean quantized bass notes")

    args = parser.parse_args()

    res = extract_bassline(
        audio_path=args.audio_path,
        output_midi_path=args.output,
        onset_threshold=args.onset,
        frame_threshold=args.frame,
        min_note_length=args.min_len,
        min_frequency=args.min_freq,
        max_frequency=args.max_freq,
        merge_gap=args.merge_gap,
        no_bends=args.no_bends
    )
    print("\n[SUCCESS] Bassline Extracted:")
    print(f"  Audio: {res['audio_path']}")
    print(f"  MIDI:  {res['midi_path']}")
    print(f"  Notes: {res['total_notes']}")


if __name__ == "__main__":
    main()
