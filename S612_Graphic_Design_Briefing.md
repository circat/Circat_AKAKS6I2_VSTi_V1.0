# Akai S612 VST Plugin
## Graphic Design Briefing for UI Development

---

## Project Overview

**Product Name:** Akai S612 VST Plugin  
**Type:** Software synthesizer/sampler plugin (VST3)  
**Reference Hardware:** Akai S612 Digital Sampling Station (1985)  
**Design Goal:** Pixel-perfect recreation of the original hardware frontplate

The Akai S612 was a groundbreaking 12-bit digital sampling workstation introduced in 1985. It featured 1MB of RAM, 6-voice polyphony, and innovative sample scanning technology. Your task is to recreate its distinctive frontpanel aesthetic for a modern VST plugin.

---

## Plugin Canvas

- **Dimensions:** 920 × 420 pixels
- **Background:** Brushed metal black (#1C1C1C) with subtle texture
- **Border:** 1px dark grey (#3A3A3A)

---

## Visual Reference Layout

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│  AKAI    S612                                                    S612 SAMPLER      │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  ┌─────────┐  ┌───────────────────┐  ┌──────────────┐  ┌────────────────────────┐  │
│  │   REC   │  │       SCAN        │  │     MODE     │  │          LFO           │  │
│  │         │  │                   │  │              │  │                        │  │
│  │ REC LED │  │                   │  │  ONE SHOT    │  │  SPEED   DEPTH  DELAY  │  │
│  │         │  │  START/  END      │  │  LOOPING     │  │   ○       ○      ○     │  │
│  │ REC LVL │  │  SPLICE  POINT    │  │  ALT         │  │                        │  │
│  │   ○     │  │   │      │        │  │  MANU.SPLICE│  │                        │  │
│  │         │  │   │      │        │  │              │  │                        │  │
│  │ MONITOR │  │   │      │        │  │              │  │  KEY TRANS   TUNE     │  │
│  │   ○     │  │   │      │        │  │              │  │  [ON]         ○       │  │
│  │         │  │   │      │        │  │              │  │                        │  │
│  │  NEW    │  │   │      │        │  │              │  │                        │  │
│  │ [ON]    │  │   │      │        │  │              │  │                        │  │
│  │         │  │   │      │        │  │              │  │                        │  │
│  │OVERDUB  │  │   │      │        │  │              │  │                        │  │
│  │ [ON]    │  │   └───────────────────┘  └──────────────┘  └────────────────────────┘  │
│  └─────────┘                                                                     │
│                                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐│
│  │                                    OUTPUT                                       ││
│  │                                                                                  ││
│  │   FILTER         DECAY         LEVEL                    MIDI CH    VOICES     ││
│  │     ○             ○             ○                       [1] [▲][▼]  ●●●●●●     ││
│  │                                                                                  ││
│  └─────────────────────────────────────────────────────────────────────────────────┘│
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Color Palette

| Element              | Color Code | Usage                          |
|---------------------|------------|--------------------------------|
| Background         | #1C1C1C    | Main canvas (brushed metal)   |
| Panel Background   | #2A2A2A    | Section backgrounds            |
| Panel Border       | #3A3A3A    | Section outlines               |
| Text Primary       | #D0D0D0    | Labels, values                |
| Text Secondary     | #808080    | Control labels, hints         |
| LED Active (Green) | #00AA00    | Active voice/button indicators |
| LED Recording      | #FF0000    | REC LED when active           |
| Knob Accent (Red)  | #AA0000    | REC LEVEL knob fill           |
| Knob Accent (Blue) | #0066AA   | FILTER, LFO knobs             |
| Display Background | #001100    | MIDI channel display BG       |
| Display Text       | #00FF00    | 7-segment green digits        |

---

## Typography

| Element           | Font              | Size   | Color     |
|-------------------|-------------------|--------|-----------|
| "AKAI" Logo       | Arial Black       | 32pt   | #D0D0D0   |
| "S612" Logo       | Arial Black       | 36pt   | #D0D0D0   |
| Subtitle          | Arial             | 11pt   | #808080   |
| Section Headers   | Arial Bold        | 14pt   | #D0D0D0   |
| Control Labels    | Arial             | 10pt   | #808080   |
| Values            | Arial             | 10pt   | #D0D0D0   |
| MIDI Display      | Monospace/Digital| 14pt   | #00FF00   |

---

## Control Specifications

### 1. REC Section (Left)

| Control      | Type        | Size     | Style                                |
|--------------|-------------|----------|---------------------------------------|
| REC LED      | LED         | 10×10    | Red (#FF0000), glows when recording  |
| REC LEVEL    | Rotary Knob | 100×100  | Red accent fill, white indicator    |
| MONITOR      | Rotary Knob | 80×80    | Grey body, white indicator           |
| NEW          | Toggle      | 100×28   | Grey button, green LED when ON       |
| OVERDUB      | Toggle      | 100×28   | Grey button, green LED when ON       |

### 2. SCAN Section

| Control         | Type          | Size     | Style                          |
|-----------------|---------------|----------|--------------------------------|
| START/SPLICE    | Vertical Fader| 50×250  | Grey track, white thumb        |
| END POINT       | Vertical Fader| 50×250  | Grey track, white thumb        |

### 3. MODE Section

| Control        | Type    | Size    | Style                                   |
|----------------|---------|---------|------------------------------------------|
| ONE SHOT       | Toggle  | 120×28  | Grey button, green LED when ON           |
| LOOPING        | Toggle  | 120×28  | Grey button, green LED when ON           |
| ALT            | Toggle  | 120×28  | Grey button, green LED when ON           |
| MANU. SPLICE   | Toggle  | 120×28  | Grey button, green LED when ON           |

### 4. LFO Section

| Control | Type        | Size    | Style                        |
|---------|-------------|---------|------------------------------|
| SPEED   | Rotary Knob | 50×50   | Blue accent, white indicator|
| DEPTH   | Rotary Knob | 50×50   | Blue accent, white indicator|
| DELAY   | Rotary Knob | 50×50   | Blue accent, white indicator|

### 5. OUTPUT Section

| Control | Type        | Size    | Style                        |
|---------|-------------|---------|------------------------------|
| FILTER  | Rotary Knob | 60×60   | Blue fill, white indicator  |
| DECAY   | Rotary Knob | 60×60   | Grey body, white indicator   |
| LEVEL   | Rotary Knob | 60×60   | Grey body, white indicator  |

### 6. KEY TRANS & TUNE

| Control   | Type       | Size   | Style                              |
|-----------|------------|--------|------------------------------------|
| KEY TRANS | Toggle     | 80×28  | Grey button, green LED when ON    |
| TUNE      | Rotary Knob| 50×50  | Grey body, -100 to +100 cents     |

### 7. MIDI Section

| Control      | Type         | Size    | Style                              |
|--------------|--------------|---------|-------------------------------------|
| MIDI CH      | 7-Segment    | 40×25   | Green on black, "1"-"16", "0"=Omni |
| CH UP        | Button       | 25×25   | Grey, ▲ symbol                     |
| CH DOWN      | Button       | 25×25   | Grey, ▼ symbol                     |

### 8. VOICE LEDs

| Control    | Type   | Size          | Style                         |
|------------|--------|---------------|-------------------------------|
| Voice 1-6  | 6 LEDs | 6×10 each     | Green (#00AA00) when active  |

---

## Component Design Guidelines

### Rotary Knobs

- **Body:** Circular with subtle gradient (light to dark grey)
- **Fill Arc:** Colored arc showing value (0-270° range)
- **Indicator Line:** White line from center to edge
- **Shadow:** Subtle drop shadow for depth
- **Interaction:** Drag up/down to adjust value

### Faders

- **Track:** Rectangular groove with dark inset
- **Thumb:** Rectangular handle, white with subtle shadow
- **Value Display:** Optional numeric readout above fader
- **Interaction:** Drag vertically

### Toggle Buttons

- **Off State:** Dark grey (#404040) background, no LED
- **On State:** Dark grey background, green LED indicator lit
- **Label:** Centered white text
- **Interaction:** Single click to toggle

### LEDs

- **Inactive:** Dark (#202020) with subtle outline
- **Active:** Bright color with glow effect (radial gradient)
- **Shape:** Circular or rectangular as specified

### 7-Segment Display

- **Background:** Near-black (#001100)
- **Digits:** Bright green (#00FF00), true segment style
- **Dot:** Optional decimal point for future use

---

## Technical Notes

1. **Framework:** JUCE 7 (C++17)
2. **Rendering:** Custom JUCE LookAndFeel class
3. **Graphics:** Can use JUCE native components or custom-drawn graphics
4. **Resolution:** Vector graphics preferred for scalability

---

## Reference Materials

- Original Akai S612 Operator's Manual
- Original Akai S612 Service Manual
- S612_VST_Briefing_v2_Exakt.docx (technical specs)
- S612_UI_Design_Spec.md (detailed implementation spec)

---

## Deliverables

1. Complete PluginEditor.cpp with all UI controls
2. Custom LookAndFeel class (S612LookAndFeel.h/cpp)
3. All control positions and interactions matching the original hardware layout

---

*Document Version: 1.0*  
*For: Graphic Designer / UI Developer*  
*Date: March 2026*
