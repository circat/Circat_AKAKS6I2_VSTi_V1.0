import os

base_dir = r"f:\S612VSTi\Source\UI"
os.makedirs(base_dir, exist_ok=True)

look_and_feel_h = """#pragma once
#include <juce_gui_basics/juce_gui_basics.h>

namespace S612 {
namespace UI {

class LookAndFeel : public juce::LookAndFeel_V4 {
public:
    LookAndFeel();
    ~LookAndFeel() override;

    void drawRotarySlider(juce::Graphics& g, int x, int y, int width, int height,
                          float sliderPos, const float rotaryStartAngle,
                          const float rotaryEndAngle, juce::Slider& slider) override;
                          
    void drawLinearSlider(juce::Graphics& g, int x, int y, int width, int height,
                          float sliderPos, float minSliderPos, float maxSliderPos,
                          const juce::Slider::SliderStyle style, juce::Slider& slider) override;
                          
    void drawButtonBackground(juce::Graphics& g, juce::Button& button,
                              const juce::Colour& backgroundColour,
                              bool shouldDrawButtonAsHighlighted,
                              bool shouldDrawButtonAsDown) override;
                              
    void drawButtonText(juce::Graphics& g, juce::TextButton& button,
                        bool shouldDrawButtonAsHighlighted,
                        bool shouldDrawButtonAsDown) override;
};

} // namespace UI
} // namespace S612
"""

look_and_feel_cpp = """#include "S612LookAndFeel.h"

namespace S612 {
namespace UI {

LookAndFeel::LookAndFeel() {
    setColour(juce::ResizableWindow::backgroundColourId, juce::Colour(18, 18, 18));
    setColour(juce::Slider::thumbColourId, juce::Colour(70, 70, 70));
    setColour(juce::Slider::trackColourId, juce::Colour(25, 25, 25));
    setColour(juce::TextButton::buttonColourId, juce::Colour(45, 45, 45));
    setColour(juce::TextButton::buttonOnColourId, juce::Colour(30, 30, 30));
    setColour(juce::TextButton::textColourOffId, juce::Colour(220, 220, 220));
    setColour(juce::TextButton::textColourOnId, juce::Colour(220, 220, 220));
}

LookAndFeel::~LookAndFeel() {}

void LookAndFeel::drawRotarySlider(juce::Graphics& g, int x, int y, int width, int height,
                                   float sliderPos, const float rotaryStartAngle,
                                   const float rotaryEndAngle, juce::Slider& slider) {
    auto radius = (float)juce::jmin(width / 2, height / 2) - 4.0f;
    auto centreX = (float)x + (float)width  * 0.5f;
    auto centreY = (float)y + (float)height * 0.5f;
    auto rx = centreX - radius;
    auto ry = centreY - radius;
    auto rw = radius * 2.0f;
    auto angle = rotaryStartAngle + sliderPos * (rotaryEndAngle - rotaryStartAngle);

    // Fill arc
    juce::Path backgroundArc;
    backgroundArc.addCentredArc(centreX, centreY, radius, radius, 0.0f, rotaryStartAngle, rotaryEndAngle, true);
    g.setColour(juce::Colour(40, 40, 40));
    g.strokePath(backgroundArc, juce::PathStrokeType(lineThickness, juce::PathStrokeType::curved, juce::PathStrokeType::rounded));

    // Knob Body
    g.setColour(juce::Colour(55, 55, 55));
    g.fillEllipse(rx, ry, rw, rw);

    // Subtitle / Label text usually rendered separate but knob stroke here
    juce::Path p;
    auto pointerLength = radius * 0.8f;
    auto pointerThickness = 2.0f;
    p.addRectangle(-pointerThickness * 0.5f, -radius, pointerThickness, pointerLength);
    p.applyTransform(juce::AffineTransform::rotation(angle).translated(centreX, centreY));
    g.setColour(juce::Colour(240, 240, 240));
    g.fillPath(p);
}

void LookAndFeel::drawLinearSlider(juce::Graphics& g, int x, int y, int width, int height,
                                   float sliderPos, float minSliderPos, float maxSliderPos,
                                   const juce::Slider::SliderStyle style, juce::Slider& slider) {
    if (style == juce::Slider::LinearVertical) {
        auto trackWidth = 8.0f;
        g.setColour(juce::Colour(25, 25, 25));
        g.fillRect((float)x + (float)width * 0.5f - trackWidth * 0.5f, (float)y, trackWidth, (float)height);

        auto thumbHeight = 16.0f;
        auto thumbWidth = width * 0.8f;
        auto thumbY = (float)y + sliderPos * ((float)height - thumbHeight);
        
        g.setColour(juce::Colour(70, 70, 70)); // grey fader
        g.fillRect((float)x + (float)width * 0.5f - thumbWidth * 0.5f, thumbY, thumbWidth, thumbHeight);
        
        // Horizontal ridges
        g.setColour(juce::Colour(100, 100, 100));
        g.drawLine((float)x + (float)width * 0.5f - thumbWidth * 0.5f, thumbY + 4, (float)x + (float)width * 0.5f + thumbWidth * 0.5f, thumbY + 4, 1.0f);
        g.drawLine((float)x + (float)width * 0.5f - thumbWidth * 0.5f, thumbY + 8, (float)x + (float)width * 0.5f + thumbWidth * 0.5f, thumbY + 8, 1.0f);
        g.drawLine((float)x + (float)width * 0.5f - thumbWidth * 0.5f, thumbY + 12, (float)x + (float)width * 0.5f + thumbWidth * 0.5f, thumbY + 12, 1.0f);
    } else {
        juce::LookAndFeel_V4::drawLinearSlider(g, x, y, width, height, sliderPos, minSliderPos, maxSliderPos, style, slider);
    }
}

void LookAndFeel::drawButtonBackground(juce::Graphics& g, juce::Button& button,
                                       const juce::Colour& backgroundColour,
                                       bool shouldDrawButtonAsHighlighted,
                                       bool shouldDrawButtonAsDown) {
    auto bounds = button.getLocalBounds().toFloat();
    bool isDownOrToggleOn = shouldDrawButtonAsDown || button.getToggleState();

    g.setColour(isDownOrToggleOn ? juce::Colour(30, 30, 30) : juce::Colour(45, 45, 45));
    g.fillRoundedRectangle(bounds, 2.0f);
    
    g.setColour(juce::Colour(20, 20, 20));
    g.drawRoundedRectangle(bounds, 2.0f, 1.0f);
}

void LookAndFeel::drawButtonText(juce::Graphics& g, juce::TextButton& button,
                                 bool shouldDrawButtonAsHighlighted,
                                 bool shouldDrawButtonAsDown) {
    juce::Font font("Helvetica Neue", 9.0f, juce::Font::plain);
    g.setFont(font);
    g.setColour(juce::Colour(220, 220, 220));
    
    auto bounds = button.getLocalBounds();
    g.drawText(button.getButtonText().toUpperCase(), bounds, juce::Justification::centred, true);
}

} // namespace UI
} // namespace S612
"""

s612_knob_h = """#pragma once
#include <juce_gui_basics/juce_gui_basics.h>

namespace S612 {
namespace UI {

class Knob : public juce::Slider {
public:
    Knob();
    ~Knob() override;

    enum Style {
        STYLE_STANDARD,
        STYLE_LFO
    };

    void setKnobStyle(Style style);
    void paint(juce::Graphics& g) override;

private:
    Style m_style = STYLE_STANDARD;
};

} // namespace UI
} // namespace S612
"""

s612_knob_cpp = """#include "S612Knob.h"

namespace S612 {
namespace UI {

Knob::Knob() : juce::Slider(juce::Slider::RotaryVerticalDrag, juce::Slider::NoTextBox) {
}

Knob::~Knob() {}

void Knob::setKnobStyle(Style style) {
    m_style = style;
    repaint();
}

void Knob::paint(juce::Graphics& g) {
    // Custom painting delegated to LookAndFeel with custom colors logic
    juce::Slider::paint(g);
    
    // Add tiny label
    g.setFont(juce::Font("Helvetica Neue", 8.0f, juce::Font::plain));
    g.setColour(juce::Colour(220, 220, 220));
    g.drawText(getName().toUpperCase(), 0, getHeight() - 12, getWidth(), 12, juce::Justification::centred, false);
}

} // namespace UI
} // namespace S612
"""

s612_fader_h = """#pragma once
#include <juce_gui_basics/juce_gui_basics.h>

namespace S612 {
namespace UI {

class Fader : public juce::Slider {
public:
    Fader();
    ~Fader() override;
    
    void paint(juce::Graphics& g) override;
};

} // namespace UI
} // namespace S612
"""

s612_fader_cpp = """#include "S612Fader.h"

namespace S612 {
namespace UI {

Fader::Fader() : juce::Slider(juce::Slider::LinearVertical, juce::Slider::NoTextBox) {
}
Fader::~Fader() {}

void Fader::paint(juce::Graphics& g) {
    juce::Slider::paint(g);
}

} // namespace UI
} // namespace S612
"""

s612_sevensegdisplay_h = """#pragma once
#include <juce_gui_basics/juce_gui_basics.h>

namespace S612 {
namespace UI {

class SevenSegDisplay : public juce::Component, public juce::Timer {
public:
    SevenSegDisplay();
    ~SevenSegDisplay() override;

    void paint(juce::Graphics& g) override;
    void timerCallback() override;

    void setChar(char c);
    void startBlinking();
    void stopBlinking();

private:
    char m_currentChar = '0';
    bool m_blinkState = true;
    bool m_isBlinking = false;
};

} // namespace UI
} // namespace S612
"""

s612_sevensegdisplay_cpp = """#include "S612SevenSegDisplay.h"

namespace S612 {
namespace UI {

SevenSegDisplay::SevenSegDisplay() {
}

SevenSegDisplay::~SevenSegDisplay() {
    stopTimer();
}

void SevenSegDisplay::paint(juce::Graphics& g) {
    g.fillAll(juce::Colour(10, 10, 10));

    juce::Colour onColor(255, 176, 0);
    juce::Colour offColor(60, 40, 0);

    bool drawA = false, drawB = false, drawC = false, drawD = false, drawE = false, drawF = false, drawG = false;

    char c = m_currentChar;
    
    if (m_isBlinking && !m_blinkState) {
        // all off
    } else {
        if (c == '0') { drawA=drawB=drawC=drawD=drawE=drawF=true; }
        else if (c == '1') { drawB=drawC=true; }
        else if (c == '2') { drawA=drawB=drawD=drawE=drawG=true; }
        else if (c == '3') { drawA=drawB=drawC=drawD=drawG=true; }
        else if (c == '4') { drawB=drawC=drawF=drawG=true; }
        else if (c == '5') { drawA=drawC=drawD=drawF=drawG=true; }
        else if (c == '6') { drawA=drawC=drawD=drawE=drawF=drawG=true; }
        else if (c == '7') { drawA=drawB=drawC=true; }
        else if (c == '8') { drawA=drawB=drawC=drawD=drawE=drawF=drawG=true; }
        else if (c == '9') { drawA=drawB=drawC=drawD=drawF=drawG=true; }
        else if (c == 'd') { drawB=drawC=drawD=drawE=drawG=true; }
        else if (c == 'E') { drawA=drawD=drawE=drawF=drawG=true; }
        else if (c == 'G') { drawA=drawC=drawD=drawE=drawF=true; }
    }

    auto w = getWidth() * 0.8f;
    auto h = getHeight() * 0.8f;
    auto ox = getWidth() * 0.1f;
    auto oy = getHeight() * 0.1f;
    auto thick = w * 0.2f;

    auto drawSeg = [&](bool on, float sx, float sy, float sw, float sh) {
        g.setColour(on ? onColor : offColor);
        g.fillRect(sx, sy, sw, sh);
    };

    drawSeg(drawA, ox + thick, oy, w - 2*thick, thick); // A
    drawSeg(drawB, ox + w - thick, oy + thick, thick, h/2 - 1.5f*thick); // B
    drawSeg(drawC, ox + w - thick, oy + h/2 + 0.5f*thick, thick, h/2 - 1.5f*thick); // C
    drawSeg(drawD, ox + thick, oy + h - thick, w - 2*thick, thick); // D
    drawSeg(drawE, ox, oy + h/2 + 0.5f*thick, thick, h/2 - 1.5f*thick); // E
    drawSeg(drawF, ox, oy + thick, thick, h/2 - 1.5f*thick); // F
    drawSeg(drawG, ox + thick, oy + h/2 - 0.5f*thick, w - 2*thick, thick); // G
}

void SevenSegDisplay::timerCallback() {
    m_blinkState = !m_blinkState;
    repaint();
}

void SevenSegDisplay::setChar(char c) {
    if (m_currentChar != c) {
        m_currentChar = c;
        repaint();
    }
}

void SevenSegDisplay::startBlinking() {
    m_isBlinking = true;
    startTimer(500);
}

void SevenSegDisplay::stopBlinking() {
    m_isBlinking = false;
    m_blinkState = true;
    stopTimer();
    repaint();
}

} // namespace UI
} // namespace S612
"""

s612_voiceleds_h = """#pragma once
#include <juce_gui_basics/juce_gui_basics.h>
#include <array>
#include <atomic>

namespace S612 {
namespace UI {

class VoiceLEDs : public juce::Component, public juce::Timer {
public:
    VoiceLEDs(std::array<std::atomic<bool>, 6>& voiceFlags);
    ~VoiceLEDs() override;

    void paint(juce::Graphics& g) override;
    void timerCallback() override;

private:
    std::array<std::atomic<bool>, 6>& m_voiceFlags;
    std::array<bool, 6> m_lastState;
};

} // namespace UI
} // namespace S612
"""

s612_voiceleds_cpp = """#include "S612VoiceLEDs.h"

namespace S612 {
namespace UI {

VoiceLEDs::VoiceLEDs(std::array<std::atomic<bool>, 6>& voiceFlags) : m_voiceFlags(voiceFlags) {
    m_lastState.fill(false);
    startTimer(50);
}

VoiceLEDs::~VoiceLEDs() {
    stopTimer();
}

void VoiceLEDs::paint(juce::Graphics& g) {
    auto w = getWidth();
    auto h = getHeight();
    auto spacing = w / 6.0f;
    
    for (int i = 0; i < 6; ++i) {
        bool isOn = m_lastState[i];
        
        auto cx = spacing * i + spacing * 0.5f;
        auto cy = h * 0.5f;
        auto radius = 3.0f;
        
        if (isOn) {
            juce::ColourGradient cg(juce::Colour(100, 255, 100), cx, cy, juce::Colour(0, 100, 0).withAlpha(0.0f), cx, cy, radius * 3.0f, true);
            g.setGradientFill(cg);
            g.fillEllipse(cx - radius * 3.0f, cy - radius * 3.0f, radius * 6.0f, radius * 6.0f);
            
            g.setColour(juce::Colour(50, 220, 50));
            g.fillEllipse(cx - radius, cy - radius, radius * 2.0f, radius * 2.0f);
        } else {
            g.setColour(juce::Colour(10, 40, 10));
            g.fillEllipse(cx - radius, cy - radius, radius * 2.0f, radius * 2.0f);
            g.setColour(juce::Colour(5, 20, 5));
            g.drawEllipse(cx - radius, cy - radius, radius * 2.0f, radius * 2.0f, 0.5f);
        }
    }
}

void VoiceLEDs::timerCallback() {
    bool changed = false;
    for (int i = 0; i < 6; ++i) {
        bool current = m_voiceFlags[i].load();
        if (current != m_lastState[i]) {
            m_lastState[i] = current;
            changed = true;
        }
    }
    if (changed) {
        repaint();
    }
}

} // namespace UI
} // namespace S612
"""

def write_file(filename, content):
    with open(os.path.join(base_dir, filename), "w") as f:
        f.write(content)

write_file("S612LookAndFeel.h", look_and_feel_h)
write_file("S612LookAndFeel.cpp", look_and_feel_cpp)
write_file("S612Knob.h", s612_knob_h)
write_file("S612Knob.cpp", s612_knob_cpp)
write_file("S612Fader.h", s612_fader_h)
write_file("S612Fader.cpp", s612_fader_cpp)
write_file("S612SevenSegDisplay.h", s612_sevensegdisplay_h)
write_file("S612SevenSegDisplay.cpp", s612_sevensegdisplay_cpp)
write_file("S612VoiceLEDs.h", s612_voiceleds_h)
write_file("S612VoiceLEDs.cpp", s612_voiceleds_cpp)

print("Files created.")
