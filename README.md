# Bassline Audio-to-MIDI Extractor

**Bassline Audio-to-MIDI Extractor** (`bassline-extractor`) is an AI skill and CLI tool built for specialized low-end audio-to-MIDI transcription powered by Spotify's Basic Pitch neural network. It isolates frequencies between 28 Hz and 320 Hz to extract clean, continuous, 100% monophonic MIDI basslines from audio recordings, 808 subs, synth bass loops, and isolated stems.

---

## ⚡ Low-End Guarantees

- **Frequency Clamping (28 Hz - 320 Hz)**: Filters out higher-register acoustic spill from snare cracks, cymbals, rhythm guitars, keyboards, and vocal bleed.
- **Sub-Bass Sensitivity (0.45 Onset Threshold)**: Accurately captures deep 808 fundamental frequencies and sub-bass notes that conventional pitch trackers often miss or shift by an octave.
- **Legato Micro-Gap Merging**: Plucked bass notes and sustained synth pads often have amplitude dips that fool MIDI converters into splitting one note into repetitive machine-gun triggers. The extractor merges gaps under 80ms into solid, continuous sustained notes.
- **Strict Monophonic Guarantee**: Completely prevents overlapping notes through a two-pass sanitizer, ensuring clean lines ready for virtual bass instruments (Serum, Diva, Ableton Drift, SubBoomBass).
- **Pitch Bend Control**: Retains musical slides and pitch-wheel glides while offering `--no-bends` for rigid grid quantization.
- **Transparent Runtime Delegation**: Automatically calls into the dedicated `basic-pitch` uv Python environment (`C:\Users\<you>\AppData\Roaming\uv\tools\basic-pitch\Scripts\python.exe`).
- **Zero-Duplicate Tri-Platform Availability**: Installed canonically in `.agents/skills/bassline-extractor` and linked via NTFS junctions to Claude, Grok, and Antigravity.

---

## 🚀 Usage

### In Chat (Prompts & Slash Commands)

- `/bassline-extractor "C:\Music\bass_stem.wav"`
- *"Extract the bassline MIDI from 'C:\Samples\808_loop.wav' --no-bends"*
- *"Transcribe this bass recording with a 400 Hz ceiling: 'D:\Recordings\funk_bass.mp3'"*
- *"Extract the sub-bass notes from 'C:\Audio\trap_intro.wav' into a clean monophonic MIDI file."*

### Command Line Interface (`scripts/bass_extract.py`)

```powershell
# Standard bass extraction with default 28 Hz - 320 Hz clamping:
python scripts/bass_extract.py "C:\Music\bass.wav"

# Hard-quantized bass without pitch bends:
python scripts/bass_extract.py "C:\Music\808_loop.wav" --no-bends

# Custom frequency ceiling for slap bass or high bass guitar solos:
python scripts/bass_extract.py "C:\Music\funk_bass.mp3" --max-freq 450.0

# Custom output destination:
python scripts/bass_extract.py "C:\Music\sub.wav" --output "C:\Music\Transcriptions\sub_lead.mid"
```

---

## 📁 Repository Structure

```
bassline-extractor/
├── SKILL.md                  # Skill trigger and platform integration instructions
├── HOW_TO_USE.txt            # Quick-reference cheat sheet & prompt guide
├── IMPLEMENTATION_PLAN.md    # Multi-version roadmap and completed tasks
├── App Changes Tracker.html  # Permanent interactive HTML version changelog
├── README.md                 # This overview
└── scripts/
    └── bass_extract.py       # Low-end frequency clamped extraction engine
```

---

## 📜 Documentation & Lifecycle

- **Version History & Releases**: Tracked permanently in [App Changes Tracker.html](App%20Changes%20Tracker.html).
- **Roadmap & Completed Features**: Documented in [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md).
