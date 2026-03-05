# Akai S612 VST UI Graphics - Technical Documentation

## 📋 Asset Inventory & Specifications

### Knobs (Drehregler)

#### Single Frame Knobs
| Asset | Dimensions | Color | Purpose | Rotation |
|-------|-----------|-------|---------|----------|
| `knob_rec.png` | 100×100 | Red | REC Level input | Fixed |
| `knob_monitor.png` | 80×80 | Gray | Monitor Level | Fixed |

#### Sprite Sheet Knobs (24 Frames = 0-360°)
| Asset | Dimensions | Frames | Color | Purpose |
|-------|-----------|--------|-------|---------|
| `knob_standard_60.png` | 360×60 | 24 | Gray | DECAY, LEVEL controls |
| `knob_standard_50.png` | 300×50 | 24 | Gray | TUNE control |
| `knob_blue_50.png` | 300×50 | 24 | Cyan | SPEED, DEPTH, DELAY |
| `knob_blue_60.png` | 360×60 | 24 | Cyan | FILTER control |

**Sprite Sheet Usage:**
```javascript
// For 60px knob (6 columns × 4 rows):
// Frame index = (angle / 15) % 24
// x = (frameIndex % 6) * 60
// y = Math.floor(frameIndex / 6) * 60

// For 50px knob (6 columns × 4 rows):
// Frame index = (angle / 15) % 24
// x = (frameIndex % 6) * 50
// y = Math.floor(frameIndex / 6) * 50
```

**Visual Features:**
- Indicator line on each knob for precise angle visualization
- Glossy highlight for depth perception
- Wear & scratches for authentic 1985 aesthetic
- Subtle anti-aliasing for smooth rotation

---

### Faders (Schieberegler)

| Asset | Dimensions | Type | Range |
|-------|-----------|------|-------|
| `fader_track.png` | 50×250 | Background track | 0-250px vertical |
| `fader_thumb.png` | 50×250 | Complete fader (thumb + track) | Can be used as is |

**Implementation:**
```javascript
// Use fader_thumb at different Y positions:
// thumbY = minY + (position * (maxY - minY))
// where position = 0.0 to 1.0
```

---

### Buttons (Taster)

#### Toggle Buttons
| Asset | Dimensions | States | LED | Purpose |
|-------|-----------|--------|-----|---------|
| `btn_toggle_off.png` | 120×28 | OFF | Dark | Recording modes, ALT modes |
| `btn_toggle_on.png` | 120×28 | ON | Green | Active state indicator |

#### Navigation Buttons
| Asset | Dimensions | Symbol | Color | Purpose |
|-------|-----------|--------|-------|---------|
| `btn_ch_up.png` | 25×25 | ▲ | Blue | Channel up |
| `btn_ch_down.png` | 25×25 | ▼ | Blue | Channel down |

---

### LEDs (Light Emitters)

#### Green LEDs
| Asset | Dimensions | State | Usage |
|-------|-----------|-------|-------|
| `led_green_on.png` | 10×10 | Illuminated (#00AA00) | Status indicator active |
| `led_green_off.png` | 10×10 | Dark (#0A2A0A) | Status indicator inactive |

#### Red LEDs
| Asset | Dimensions | State | Usage |
|-------|-----------|-------|-------|
| `led_red_on.png` | 10×10 | Illuminated (#FF0000) | Warning/Error state |
| `led_red_off.png` | 10×10 | Dark (#2A0A0A) | Inactive |

**Note:** LEDs have subtle glow effect. Layer multiple copies for enhanced luminosity.

---

### Display

| Asset | Dimensions | Type | Background |
|-------|-----------|------|------------|
| `display_7seg.png` | 40×25 | 7-Segment Display | Dark green (#001100) |

**Rendering Text:**
- Overlay text in `#00FF00` (bright green) on background
- Use monospace font (Courier, OCR-B styled)
- Center text vertically and horizontally

---

### Panels (Background Elements)

| Asset | Dimensions | Section | Notes |
|-------|-----------|---------|-------|
| `panel_bg.png` | 890×50 | Header/Top bar | Brushed metal texture |
| `panel_rec.png` | 130×310 | REC Level section | Full height panel |
| `panel_scan.png` | 180×310 | START/SPLICE section | Fader panel |
| `panel_mode.png` | 140×310 | Mode buttons | Vertical section |
| `panel_lfo.png` | 180×310 | LFO controls | Cyan knob area |
| `panel_output.png` | 220×310 | Output/Filter | Right side panel |

---

## 🎨 Color Palette

### Core Colors
```
Background:      #1C1C1C (Deep black)
Panel BG:        #2A2A2A (Dark gray)
Border:          #3A3A3A (Medium-dark gray)
Text:            #D0D0D0 (Light gray)
Text Label:      #808080 (Medium gray)
```

### Indicators
```
LED Green ON:    #00AA00 (Bright green)
LED Green OFF:   #0A2A0A (Dark green)
LED Red ON:      #FF0000 (Bright red)
LED Red OFF:     #2A0A0A (Dark red)
```

### Controls
```
Knob Red:        #AA0000 (Deep red)
Knob Blue:       #0066AA (Deep blue)
Knob Gray:       #555555 (Medium gray)
Button Red:      #CC0000 (Bright red)
Button Blue:     #00AACC (Cyan)
Button Beige:    #CCBB99 (Tan)
```

### Display
```
Display BG:      #001100 (Dark green)
Display Text:    #00FF00 (Bright green)
```

---

## 🛠️ Implementation Examples

### React Component Example

```javascript
import React, { useState } from 'react';

const KnobRotary = ({ size = 60, color = 'gray', value = 0 }) => {
  const frameIndex = Math.floor((value / 360) * 24) % 24;
  const frameWidth = size;
  const frameHeight = size;
  const cols = 6;
  
  const x = (frameIndex % cols) * frameWidth;
  const y = Math.floor(frameIndex / cols) * frameHeight;
  
  return (
    <div
      style={{
        width: frameWidth,
        height: frameHeight,
        backgroundImage: `url('/assets/knob_${color}_${size}.png')`,
        backgroundPosition: `-${x}px -${y}px`,
        backgroundSize: 'auto',
      }}
    />
  );
};

const FaderVertical = ({ value = 0.5 }) => {
  const trackHeight = 250;
  const thumbHeight = 20;
  const thumbY = value * (trackHeight - thumbHeight);
  
  return (
    <div style={{
      position: 'relative',
      width: 50,
      height: trackHeight,
      backgroundImage: 'url(/assets/fader_track.png)',
    }}>
      <img
        src="/assets/fader_thumb.png"
        style={{
          position: 'absolute',
          top: thumbY,
          left: 0,
        }}
      />
    </div>
  );
};

const LEDIndicator = ({ state = 'on', color = 'green' }) => {
  return (
    <img
      src={`/assets/led_${color}_${state}.png`}
      alt={`LED ${color} ${state}`}
    />
  );
};
```

### Web Audio Implementation

```javascript
// Knob rotation with mouse
class RotaryControl {
  constructor(element, onValueChange) {
    this.element = element;
    this.value = 0;
    this.onValueChange = onValueChange;
    this.setupDragListener();
  }
  
  setupDragListener() {
    let isDragging = false;
    let startY;
    
    this.element.addEventListener('mousedown', (e) => {
      isDragging = true;
      startY = e.clientY;
    });
    
    document.addEventListener('mousemove', (e) => {
      if (!isDragging) return;
      
      const delta = startY - e.clientY;
      this.value = Math.max(0, Math.min(360, this.value + delta));
      startY = e.clientY;
      
      this.updateDisplay();
      this.onValueChange(this.value);
    });
    
    document.addEventListener('mouseup', () => {
      isDragging = false;
    });
  }
  
  updateDisplay() {
    const frameIndex = Math.floor((this.value / 360) * 24) % 24;
    const frameWidth = 60;
    const cols = 6;
    const x = (frameIndex % cols) * frameWidth;
    const y = Math.floor(frameIndex / cols) * frameWidth;
    
    this.element.style.backgroundPosition = `-${x}px -${y}px`;
  }
}
```

---

## 🎯 Wear & Tear Characteristics

All assets include realistic aging:
- **Scratches**: 3-8 random white lines with varying opacity
- **Dust particles**: 15-30 small translucent spots
- **Panel texture**: Brushed metal effect with grain
- **Patina**: Subtle color shifts indicating oxidation

This creates an authentic mid-80s aesthetic without looking pristine.

---

## 📐 Asset Quality Notes

### Resolution
- **PNG Format**: 8-bit RGBA with alpha transparency
- **Anti-aliasing**: Applied to curved elements for smooth rendering
- **Scalability**: Vector-derived but optimized for pixel-perfect rendering at specified sizes

### Color Accuracy
- Tested against original Akai S612 hardware photographs
- Matches authentic 1985 component aesthetic
- LEDs include proper glow/luminosity simulation

### File Size Optimization
- Compressed PNG with maximum compatibility
- Total asset package: ~201KB
- Individual assets range from 250 bytes (LEDs) to 40KB (sprite sheets)

---

## ⚙️ VST Plugin Integration

### Asset Loading Priority
1. Load all knob sprite sheets on initialization
2. Pre-cache fader components
3. LED states update only on change (not on every frame)
4. Panel backgrounds remain static

### Performance Tips
1. Use CSS transforms for knob rotation (better than re-rendering)
2. Batch LED updates to reduce draw calls
3. Consider hardware acceleration for animated controls
4. Sprite sheets are more efficient than individual frames

---

## 📞 Technical Support

### Common Issues

**Knob appears pixelated:**
- Ensure sprite sheet frame calculation is correct
- Use integer pixel values (no subpixel rendering)

**LEDs not glowing:**
- Layer multiple LED images for enhanced brightness
- Use blend modes (screen/add) in compositing

**Fader jittery:**
- Quantize position values to nearest pixel
- Debounce mouse move events

---

Generated: 2025-03-03
For: Akai S612 Digital Sampler VST Plugin UI
Style: Authentic 1985 Hardware Aesthetic
