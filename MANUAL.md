# CIRCAT AKAKS6I2 V1 - User Manual

![CIRCAT AKAKS6I2 V1](Circat_AKAKS6I2_Screenshot.PNG)

## 🎛 Overview
The **CIRCAT AKAKS6I2 V1** is a character-driven VST3 sampler targeting the iconic 12-bit grit and unique workflow of the vintage S612 hardware (1985). This plugin captures the essence of early digital sampling: raw resolution, linear resampling behaviors, and immediate controls.

## ✨ Core Features
- **12-Bit Engine:** Authentic quantization to 12-bit depth for that classic "crunch" and floor-noise character.
- **Switchable Sampling Rates:** Toggle between **32kHz, 16kHz, and 8kHz** operation. The internal engine dynamically resamples your audio, just like the hardware.
- **Switched Capacitor Filter:** A meticulous emulation of the legendary MF6CN-50 filter, providing a characterful 24dB/oct LPF curve.
- **LFO Modulation:** Modulate the sampling clock for classic pitch-warble and "tape-like" flutter.
- **Manual Splice Logic:** Toggle Manual Splice to fine-tune your loop points with high precision.
- **Alternating Loop:** Support for "Hin & Her" (Forward-Backward) looping, essential for smooth pads and glitchy textures.

## 🕹 Front Panel Controls
### Sample Operation
- **NEW:** Clears the current buffer and enters **Standby Mode**, waiting for an input signal above the threshold to start recording.
- **OVERDUB:** Layers new input audio on top of the existing sample buffer without clearing it first.
- **MONITOR:** Enable this to hear the input signal reaching the sampler.

### Sound Shaping
- **FILTER:** Adjusts the 24dB/oct low-pass filter cutoff frequency.
- **LFO RATE/DEPTH:** Configures the internal sampling clock modulation.
- **DECAY:** Sets the release time for the internal envelope (after note-off).

### Looping & Markers
- **START POINT:** Sets the playback beginning.
- **END POINT:** Sets the playback end/loop point.
- **SPLICE POINT:** When Manual Splice is active, used to adjust the loop return point.
- **MANUAL SPLICE (Toggle):** Enables precise loop editing.
- **ONE SHOT / LOOPING:** Toggles between playing once or sustaining the loop.

## 🚀 Installation & Setup

1.  **Extract the Files:** Download and extract the provided `CIRCAT_AKAKS6I2_V1_Distribution.zip`.
2.  **Locate VST3 Folder:** Copy the `CIRCAT AKAKS6I2 V1.vst3` folder into your system's VST3 directory:
    - **Windows Default:** `C:\Program Files\Common Files\VST3\`
3.  **Rescan DAW:** Restart your Digital Audio Workstation (Ableton, FL Studio, Logic, etc.) and perform a plugin rescan.

## 📝 Troubleshooting & Tips
- **Headroom:** The "REC LEVEL" knob controls the input gain. Watch the meter! Driving it into the red (+3dB) adds genuine digital clipping character.
- **Sidechain Support:** Enable Sidechain in your DAW to record from other tracks directly "into" the AKAKS6I2.
- **Warm-Up Guard:** The plugin has a 150ms "warm-up" period on load to protect your speakers from DAW bus initialization spikes.

---
*Developed by CIRCAT. Precise. Vintage. Grit.*
