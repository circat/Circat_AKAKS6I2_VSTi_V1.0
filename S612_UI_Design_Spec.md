# S612 VST Plugin - UI Design Specification

## Plugin Dimensions
- **Width:** 920px
- **Height:** 420px
- **Background:** Black (#1C1C1C) - Brushed metal look

---

## SECTION 1: REC (Recording) - LEFT
**Position:** x=15, y=85, width=130, height=310

| Control | Type | Position | Size | Color |
|---------|------|----------|------|-------|
| REC LEVEL | Rotary Knob | x=30, y=125 | 100x100 | Red fill |
| MONITOR | Rotary Knob | x=30, y=235 | 80x80 | Grey |
| NEW Button | Toggle | x=30, y=320 | 100x28 | Grey/LED green |
| OVERDUB Button | Toggle | x=30, y=355 | 100x28 | Grey/LED green |
| REC LED | LED | x=130, y=125 | 10x10 | Red (when recording) |

---

## SECTION 2: SCAN (Scanning)  
**Position:** x=155, y=85, width=180, height=310

| Control | Type | Position | Size | Color |
|---------|------|----------|------|-------|
| START/SPLICE Fader | Vertical Slider | x=170, y=105 | 50x250 | Grey/White thumb |
| END POINT Fader | Vertical Slider | x=250, y=105 | 50x250 | Grey/White thumb |

---

## SECTION 3: MODE
**Position:** x=345, y=85, width=140, height=310

| Control | Type | Position | Size | Color |
|---------|------|----------|------|-------|
| ONE SHOT | Toggle Button | x=355, y=115 | 120x28 | LED green when ON |
| LOOPING | Toggle Button | x=355, y=150 | 120x28 | LED green when ON |
| ALT (Alternating) | Toggle Button | x=355, y=185 | 120x28 | LED green when ON |
| MANU. SPLICE | Toggle Button | x=355, y=220 | 120x28 | LED green when ON |

---

## SECTION 4: LFO
**Position:** x=495, y=85, width=180, height=310

| Control | Type | Position | Size | Color |
|---------|------|----------|------|-------|
| SPEED | Rotary Knob | x=510, y=120 | 50x50 | Blue accent |
| DEPTH | Rotary Knob | x=565, y=120 | 50x50 | Blue accent |
| DELAY | Rotary Knob | x=620, y=120 | 50x50 | Blue accent |

**Labels:** Below each knob in grey (#808080)

---

## SECTION 5: OUTPUT
**Position:** x=685, y=85, width=220, height=310

| Control | Type | Position | Size | Color |
|---------|------|----------|------|-------|
| FILTER | Rotary Knob | x=705, y=120 | 60x60 | Blue fill |
| DECAY | Rotary Knob | x=780, y=120 | 60x60 | Standard |
| LEVEL | Rotary Knob | x=855, y=120 | 60x60 | Standard |

**Labels:** Below each knob in grey (#808080)

---

## SECTION 6: KEY TRANS & TUNE
**Position:** x=495, y=280

| Control | Type | Position | Size | Color |
|---------|------|----------|------|-------|
| KEY TRANS | Toggle Button | x=495, y=280 | 80x28 | LED green when ON |
| TUNE | Rotary Knob | x=585, y=270 | 50x50 | Standard (-100 to +100 cent) |

---

## SECTION 7: MIDI
**Position:** x=685, y=280

| Control | Type | Position | Size | Color |
|---------|------|----------|------|-------|
| MIDI CH Display | 7-Segment | x=700, y=280 | 40x25 | Green on black |
| CH UP | Button | x=750, y=280 | 25x25 | Grey |
| CH DOWN | Button | x=780, y=280 | 25x25 | Grey |

---

## SECTION 8: VOICE LEDs
**Position:** x=815, y=280

| Control | Type | Position ||---------|------|----------|------| Size | Color |
-------|
| Voice 1-6 LED | 6 LEDs | x=815, y=280 | 6x10 each | Green (active) |

---

## HEADER (Title Area)
**Position:** x=15, y=15, width=890, height=50

| Element | Position | Size | Font |
|---------|----------|------|------|
| "AKAI" | x=30, y=18 | 120x44 | Arial Black 32pt |
| "S612" | x=140, y=15 | 140x50 | Arial Black 36pt |
| Subtitle | x=30, y=55 | 200x15 | Arial 11pt grey |

---

## Color Palette

| Element | Color Code |
|---------|------------|
| Background | #1C1C1C |
| Panel BG | #2A2A2A |
| Border | #3A3A3A |
| Text Primary | #D0D0D0 |
| Text Secondary | #808080 |
| LED Green (ON) | #00AA00 |
| LED Red (Recording) | #FF0000 |
| Knob Accent (REC) | #AA0000 |
| Knob Accent (Filter) | #0066AA |
| Display BG | #001100 |
| Display Text | #00FF00 |

---

## Required Graphics Assets (Optional)
If designing custom graphics:
- `knob_rec.png` - 100x100 rotary knob
- `knob_std.png` - 60x60 standard knob  
- `knob_small.png` - 50x50 small knob
- `fader_track.png` - 50x250 vertical track
- `fader_thumb.png` - 50x20 fader handle
- `led_green.png` - 10x10 LED
- `led_red.png` - 10x10 LED
- `btn_toggle.png` - button states
- `display_midi.png` - 40x25 seven-segment

---

## Interaction Notes
- All knobs: Mouse drag up/down to change value
- Faders: Mouse drag vertical
- Buttons: Click to toggle
- MIDI CH: Click UP/DOWN to change channel (0-9, 0=Omni)
