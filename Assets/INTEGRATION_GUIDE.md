# Akai S612 VST UI - Asset Manifest & Integration Guide

**Project:** Akai S612 Digital Sampler VST Plugin
**Graphics Style:** Authentic 1985 Hardware
**Total Assets:** 25 PNG files
**Package Size:** ~201 KB
**Format:** PNG 8-bit RGBA

---

## 🎯 Quick Integration Checklist

- [ ] Copy all PNG files to `src/assets/` directory
- [ ] Load sprite sheets on plugin initialization
- [ ] Map knob rotation values to sprite frame indices
- [ ] Setup LED state management (on/off)
- [ ] Configure fader position calculations
- [ ] Set button state listeners
- [ ] Style panel backgrounds with correct dimensions
- [ ] Test all interactive elements at 100% and 50% zoom levels

---

## 📦 Asset Directory Structure

```
assets/
├── knobs/
│   ├── knob_rec.png (100×100, red, fixed)
│   ├── knob_monitor.png (80×80, gray, fixed)
│   ├── knob_standard_60.png (360×60, sprite sheet, 24 frames)
│   ├── knob_standard_50.png (300×50, sprite sheet, 24 frames)
│   ├── knob_blue_60.png (360×60, sprite sheet, 24 frames)
│   └── knob_blue_50.png (300×50, sprite sheet, 24 frames)
│
├── faders/
│   ├── fader_track.png (50×250)
│   └── fader_thumb.png (50×250)
│
├── buttons/
│   ├── btn_toggle_off.png (120×28, red)
│   ├── btn_toggle_on.png (120×28, red with green LED)
│   ├── btn_ch_up.png (25×25, blue)
│   └── btn_ch_down.png (25×25, blue)
│
├── leds/
│   ├── led_green_on.png (10×10)
│   ├── led_green_off.png (10×10)
│   ├── led_red_on.png (10×10)
│   └── led_red_off.png (10×10)
│
├── display/
│   └── display_7seg.png (40×25)
│
├── panels/
│   ├── panel_bg.png (890×50, header)
│   ├── panel_rec.png (130×310)
│   ├── panel_scan.png (180×310)
│   ├── panel_mode.png (140×310)
│   ├── panel_lfo.png (180×310)
│   └── panel_output.png (220×310)
│
└── reference/
    └── color_palette.png
```

---

## 🔄 Sprite Sheet Frame Mapping

### 60px Knobs (knob_standard_60, knob_blue_60)
```
Dimensions: 360×60 pixels
Frames: 24 (0-23)
Layout: 6 columns × 4 rows

Frame Layout:
Row 0: [0] [1] [2] [3] [4] [5]      (0°-75°)
Row 1: [6] [7] [8] [9] [10] [11]    (90°-165°)
Row 2: [12] [13] [14] [15] [16] [17] (180°-255°)
Row 3: [18] [19] [20] [21] [22] [23] (270°-345°)

Angle to Frame: frameIndex = Math.round((angle / 360) * 24) % 24
Frame to Position:
  x = (frameIndex % 6) * 60
  y = Math.floor(frameIndex / 6) * 60
```

### 50px Knobs (knob_standard_50, knob_blue_50)
```
Dimensions: 300×50 pixels
Frames: 24 (0-23)
Layout: 6 columns × 4 rows

Frame to Position:
  x = (frameIndex % 6) * 50
  y = Math.floor(frameIndex / 6) * 50
```

---

## 🎮 Control Mapping

### Knob Assignments

| Control | Asset | Size | Color | Rotation Range | Default |
|---------|-------|------|-------|-----------------|---------|
| REC LEVEL | knob_rec.png | 100×100 | Red | 0-360° | 0° |
| MONITOR | knob_monitor.png | 80×80 | Gray | N/A | Fixed |
| DECAY | knob_standard_60.png | 60×60 | Gray | 0-360° | 0° |
| LEVEL | knob_standard_60.png | 60×60 | Gray | 0-360° | 0° |
| TUNE | knob_standard_50.png | 50×50 | Gray | 0-360° | 180° |
| LFO SPEED | knob_blue_60.png | 60×60 | Cyan | 0-360° | 0° |
| LFO DEPTH | knob_blue_50.png | 50×50 | Cyan | 0-360° | 0° |
| DELAY | knob_blue_50.png | 50×50 | Cyan | 0-360° | 0° |
| FILTER | knob_blue_60.png | 60×60 | Cyan | 0-360° | 180° |
| OUTPUT DECAY | knob_standard_60.png | 60×60 | Gray | 0-360° | 0° |

### Fader Assignments

| Control | Asset | Orientation | Min | Max | Default |
|---------|-------|-------------|-----|-----|---------|
| START/SPLICE | fader_thumb.png | Vertical | 0 | 250px | 0 |

### Button Assignments

| Control | Asset OFF | Asset ON | Type | LED |
|---------|-----------|----------|------|-----|
| NEW | btn_toggle_off | btn_toggle_on | Toggle | Green |
| OVER DUB | btn_toggle_off | btn_toggle_on | Toggle | Green |
| CHANNEL DOWN | btn_ch_down | — | Momentary | — |
| CHANNEL UP | btn_ch_up | — | Momentary | — |
| ONE SHOT | btn_toggle_off | btn_toggle_on | Toggle | Green |
| LOOPING | btn_toggle_off | btn_toggle_on | Toggle | Green |
| ALTERNATING | btn_toggle_off | btn_toggle_on | Toggle | Green |
| KEY TRANS | btn_toggle_off | btn_toggle_on | Toggle | Green |
| MANUAL SPLICE | btn_toggle_off | btn_toggle_on | Toggle | Green |

### LED Assignments

| Indicator | ON Asset | OFF Asset | Type | Meaning |
|-----------|----------|-----------|------|---------|
| POWER | led_green_on | led_green_off | Green | Plugin active |
| RECORD | led_red_on | led_red_off | Red | Recording |
| READY | led_green_on | led_green_off | Green | Ready to record |
| PLAYBACK | led_green_on | led_green_off | Green | Playback active |

---

## 💻 JavaScript Implementation Template

```javascript
// ============================================
// Knob Control Implementation
// ============================================

class KnobControl {
  constructor(options) {
    this.element = options.element;
    this.size = options.size || 60; // 50 or 60
    this.color = options.color || 'gray'; // gray, blue, red
    this.value = options.defaultValue || 0; // 0-360
    this.onValueChange = options.onValueChange || (() => {});
    
    this.spriteSheet = new Image();
    this.spriteSheet.src = `/assets/knob_${this.color}_${this.size}.png`;
    this.spriteSheet.onload = () => this.render();
    
    this.setupInteraction();
  }
  
  setupInteraction() {
    let isDragging = false;
    let lastY = 0;
    
    this.element.addEventListener('mousedown', (e) => {
      isDragging = true;
      lastY = e.clientY;
      this.element.style.cursor = 'grabbing';
    });
    
    document.addEventListener('mousemove', (e) => {
      if (!isDragging) return;
      
      const delta = (lastY - e.clientY) * 2; // Sensitivity
      this.value = (this.value + delta) % 360;
      if (this.value < 0) this.value += 360;
      
      this.render();
      this.onValueChange(this.value);
      lastY = e.clientY;
    });
    
    document.addEventListener('mouseup', () => {
      isDragging = false;
      this.element.style.cursor = 'grab';
    });
    
    // Scroll wheel support
    this.element.addEventListener('wheel', (e) => {
      e.preventDefault();
      const delta = e.deltaY > 0 ? -5 : 5;
      this.value = (this.value + delta) % 360;
      this.render();
      this.onValueChange(this.value);
    });
  }
  
  render() {
    const frameIndex = Math.round((this.value / 360) * 24) % 24;
    const cols = 6;
    const x = (frameIndex % cols) * this.size;
    const y = Math.floor(frameIndex / cols) * this.size;
    
    this.element.style.backgroundImage = 
      `url('${this.spriteSheet.src}')`;
    this.element.style.backgroundPosition = `-${x}px -${y}px`;
    this.element.style.backgroundRepeat = 'no-repeat';
    this.element.style.width = `${this.size}px`;
    this.element.style.height = `${this.size}px`;
  }
  
  setValue(newValue) {
    this.value = Math.max(0, Math.min(360, newValue));
    this.render();
  }
}

// ============================================
// Fader Control Implementation
// ============================================

class FaderControl {
  constructor(options) {
    this.element = options.element;
    this.value = options.defaultValue || 0.5; // 0.0-1.0
    this.onValueChange = options.onValueChange || (() => {});
    
    this.trackHeight = 250;
    this.thumbHeight = 20;
    this.minY = 0;
    this.maxY = this.trackHeight - this.thumbHeight;
    
    this.element.innerHTML = `
      <div class="fader-track" 
           style="background-image: url('/assets/fader_track.png');
                   width: 50px; height: 250px; position: relative;">
        <img class="fader-thumb" 
             src="/assets/fader_thumb.png"
             style="position: absolute; left: 0; width: 50px; height: 20px;">
      </div>
    `;
    
    this.thumb = this.element.querySelector('.fader-thumb');
    this.updatePosition();
    this.setupInteraction();
  }
  
  setupInteraction() {
    let isDragging = false;
    
    this.thumb.addEventListener('mousedown', (e) => {
      isDragging = true;
      e.preventDefault();
    });
    
    document.addEventListener('mousemove', (e) => {
      if (!isDragging) return;
      
      const rect = this.element.parentElement.getBoundingClientRect();
      const y = e.clientY - rect.top;
      this.value = Math.max(0, Math.min(1, y / this.trackHeight));
      
      this.updatePosition();
      this.onValueChange(this.value);
    });
    
    document.addEventListener('mouseup', () => {
      isDragging = false;
    });
  }
  
  updatePosition() {
    const y = this.minY + (this.value * this.maxY);
    this.thumb.style.top = `${y}px`;
  }
  
  setValue(newValue) {
    this.value = Math.max(0, Math.min(1, newValue));
    this.updatePosition();
  }
}

// ============================================
// Button Control Implementation
// ============================================

class ButtonControl {
  constructor(options) {
    this.element = options.element;
    this.state = options.defaultState || 'off'; // on/off
    this.onClick = options.onClick || (() => {});
    
    this.updateDisplay();
    this.element.addEventListener('click', () => this.toggle());
  }
  
  toggle() {
    this.state = this.state === 'on' ? 'off' : 'on';
    this.updateDisplay();
    this.onClick(this.state);
  }
  
  updateDisplay() {
    const imgSrc = this.state === 'on' 
      ? '/assets/btn_toggle_on.png'
      : '/assets/btn_toggle_off.png';
    
    this.element.style.backgroundImage = `url('${imgSrc}')`;
    this.element.style.backgroundRepeat = 'no-repeat';
    this.element.style.width = '120px';
    this.element.style.height = '28px';
    this.element.style.cursor = 'pointer';
  }
  
  setState(newState) {
    this.state = newState;
    this.updateDisplay();
  }
}

// ============================================
// LED Indicator Implementation
// ============================================

class LEDIndicator {
  constructor(options) {
    this.element = options.element;
    this.state = options.defaultState || 'off'; // on/off
    this.color = options.color || 'green'; // green/red
    this.update();
  }
  
  setState(newState) {
    this.state = newState;
    this.update();
  }
  
  update() {
    const imgSrc = `/assets/led_${this.color}_${this.state}.png`;
    
    this.element.style.backgroundImage = `url('${imgSrc}')`;
    this.element.style.backgroundRepeat = 'no-repeat';
    this.element.style.width = '10px';
    this.element.style.height = '10px';
  }
}

// ============================================
// Usage Example
// ============================================

const recLevelKnob = new KnobControl({
  element: document.getElementById('rec-level-knob'),
  size: 100,
  color: 'red',
  defaultValue: 0,
  onValueChange: (value) => {
    console.log('REC Level:', value);
    // Update audio processor
  }
});

const startSpliceFader = new FaderControl({
  element: document.getElementById('start-splice-fader'),
  defaultValue: 0,
  onValueChange: (value) => {
    console.log('Start/Splice:', value);
  }
});

const newButton = new ButtonControl({
  element: document.getElementById('new-button'),
  defaultState: 'off',
  onClick: (state) => {
    console.log('NEW button:', state);
  }
});

const recordLED = new LEDIndicator({
  element: document.getElementById('record-led'),
  color: 'red',
  defaultState: 'off'
});
```

---

## 🎨 CSS Styling Hints

```css
/* Knob container styling */
.knob {
  display: inline-block;
  cursor: grab;
  user-select: none;
  image-rendering: pixelated;
  image-rendering: crisp-edges;
  transition: filter 0.1s;
}

.knob:hover {
  filter: brightness(1.1);
}

.knob:active {
  cursor: grabbing;
}

/* Fader container */
.fader {
  position: relative;
  display: inline-block;
}

.fader-track {
  background-repeat: no-repeat;
  image-rendering: pixelated;
}

.fader-thumb {
  user-select: none;
  cursor: grab;
}

.fader-thumb:active {
  cursor: grabbing;
}

/* Button styling */
.button {
  display: inline-block;
  background-repeat: no-repeat;
  background-size: contain;
  cursor: pointer;
  border: none;
  padding: 0;
  user-select: none;
  transition: filter 0.05s;
}

.button:hover {
  filter: brightness(1.15);
}

.button:active {
  filter: brightness(0.85);
}

/* LED indicator */
.led {
  display: inline-block;
  background-repeat: no-repeat;
  background-size: contain;
}

/* Panel backgrounds */
.panel {
  background-repeat: repeat;
  background-size: auto;
  image-rendering: pixelated;
}
```

---

## 🔍 Quality Assurance

### Visual Checklist
- [ ] All knobs rotate smoothly (24 frames = 15° per step)
- [ ] Fader thumb moves fluidly without jitter
- [ ] Button press feedback is immediate
- [ ] LEDs have visible glow at both zoom levels
- [ ] Display text is readable at normal size
- [ ] Panel textures appear consistent
- [ ] All assets have proper edge aliasing

### Performance Checklist
- [ ] Sprite sheets loaded once on init
- [ ] No memory leaks from repeated image loading
- [ ] Smooth interaction at 60+ FPS
- [ ] CPU usage < 5% when idle
- [ ] All transitions use requestAnimationFrame

### Browser Compatibility
- [ ] Chrome/Chromium 90+
- [ ] Firefox 88+
- [ ] Safari 14+
- [ ] Edge 90+

---

## 🐛 Troubleshooting

### Knob appears jerky
**Solution:** Use CSS transforms with GPU acceleration
```css
.knob { will-change: transform; }
```

### Fader position incorrect
**Solution:** Ensure pixel-perfect calculations
```javascript
const y = Math.round(minY + (value * maxY));
```

### LEDs not visible
**Solution:** Layer multiple LED elements or use blend modes
```css
.led { mix-blend-mode: screen; }
```

### Panel texture looks pixelated
**Solution:** Use background-size: contain and maintain exact pixel ratio

---

**Last Updated:** March 2025
**Compatibility:** Web Audio API, VST.js, Electron
**License:** Provided for development use only
