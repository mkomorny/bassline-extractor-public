---
name: bassline-extractor
description: Specialized low-end audio-to-MIDI bassline extractor. Enforces strict frequency boundaries (28 Hz - 320 Hz) to eliminate guitar, cymbal, and vocal bleed, merges fragmented legato notes, and guarantees monophonic bass output.
---

# Bassline Audio-to-MIDI Extractor

Extracts clean, accurate monophonic MIDI basslines from audio recordings, isolated bass stems, 808 loops, and synth bass tracks.

## Low-End Guarantees

1. **Frequency Clamping (< 320 Hz)**: Filters out higher-register acoustic spill from drums (snare crack, cymbals), rhythm guitars, keyboards, and vocal bleed.
2. **Sub-Bass Sensitivity (28 Hz floor)**: Captures deep 808 subs and low synth basslines that standard pitch trackers often misidentify or shift by an octave.
3. **Legato Gap Merging**: Bass guitar plucks and sustained synth notes often suffer from amplitude dips that trick audio-to-MIDI converters into splitting one sustained note into rapid repeated notes. The extractor merges these micro-gaps for solid, continuous bass sustain.
4. **Monophonic Guarantee**: Completely prevents overlapping notes, ensuring a clean bassline ready for virtual bass instruments (Serum, Diva, Ableton Drift, SubBoomBass).

---

## Usage

```bash
# Transcribe bass stem to clean MIDI:
python "C:\Users\<you>\.agents\skills\bassline-extractor\scripts\bass_extract.py" "C:\Music\bass.wav"

# Hard-quantized bass without pitch bends:
python "C:\Users\<you>\.agents\skills\bassline-extractor\scripts\bass_extract.py" "C:\Music\808_loop.wav" --no-bends

# Custom frequency ceiling for high slap-bass:
python "C:\Users\<you>\.agents\skills\bassline-extractor\scripts\bass_extract.py" "C:\Music\funk_bass.mp3" --max-freq 450.0
```
