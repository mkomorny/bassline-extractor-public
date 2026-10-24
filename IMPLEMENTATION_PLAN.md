# Implementation Plan: Bassline Audio-to-MIDI Extractor

This document tracks planned, in-progress, and completed work for the **Bassline Audio-to-MIDI Extractor** skill. It persists across all version passes.

---

## Completed Work

### v1.0.0 — Initial Release (2026-09-24)
- [x] **Low-End Frequency Clamping (`scripts/bass_extract.py`)**: Enforced strict pitch limits (default: 28 Hz sub-bass floor to 320 Hz low-mid ceiling) inside Spotify Basic Pitch inference to completely reject cymbals, guitars, and vocal bleed. (✅ done in v1.0.0)
- [x] **Sub-Bass Sensitivity Tuning**: Lowered onset threshold to `0.45` to reliably capture deep 808 fundamental frequencies without octave displacement. (✅ done in v1.0.0)
- [x] **Two-Pass Legato & Monophonic Sanitizer**:
  - [x] Pass 1: Merges same-pitch consecutive note fragments across micro-amplitude dips (up to 80ms) for solid sustained lines. (✅ done in v1.0.0)
  - [x] Pass 2: Truncates overlapping notes to guarantee 100% monophonic single-voice output. (✅ done in v1.0.0)
- [x] **Pitch Bend Controls**: Retains natural pitch slides and pitch-wheel glides while offering `--no-bends` for rigid grid quantization. (✅ done in v1.0.0)
- [x] **Automatic Runtime Delegation**: Automatically calls into dedicated `basic-pitch` uv environment (`C:\Users\<you>\AppData\Roaming\uv\tools\basic-pitch\Scripts\python.exe`). (✅ done in v1.0.0)
- [x] **Tri-Platform Deployment**: Established canonical skill in `.agents/skills/bassline-extractor` with NTFS directory junctions to `.claude/skills`, `.grok/skills`, and `.gemini/config/skills`. (✅ done in v1.0.0)
- [x] **Documentation & Versioning**: Authored `SKILL.md`, standardized `HOW_TO_USE.txt`, `README.md`, and permanent `App Changes Tracker.html`. (✅ done in v1.0.0)

---

## Planned Future Work

- [ ] **808 Slide Pitch-Wheel Optimization**: Fine-tune pitch bend slope detection specifically for modern trap 808 glide curves.
- [ ] **Direct Ableton Bass Track Staging**: Option to automatically copy extracted basslines into `A:\User Library\Clips\Basslines`.
- [ ] **Automatic Low-Pass Pre-Filter**: Add digital Butterworth low-pass filter pre-pass for heavily distorted or noisy mixed tracks.
