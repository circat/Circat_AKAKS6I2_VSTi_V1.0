import os

look_and_feel_h = """#pragma once
#include <juce_gui_basics/juce_gui_basics.h>

namespace S612 {
namespace UI {

class LookAndFeel : public juce::LookAndFeel_V4 {
public:
    LookAndFeel();
    ~LookAndFeel() override;

    void drawRotarySlider(juce::Graphics&, int x, int y, int width, int height,
                          float sliderPos, const float rotaryStartAngle,
                          const float rotaryEndAngle, juce::Slider&) override;

    void drawLinearSlider(juce::Graphics&, int x, int y, int width, int height,
                          float sliderPos, float minSliderPos, float maxSliderPos,
                          const juce::Slider::SliderStyle, juce::Slider&) override;

    void drawButtonBackground(juce::Graphics&, juce::Button&,
                              const juce::Colour& backgroundColour,
                              bool shouldDrawButtonAsHighlighted,
                              bool shouldDrawButtonAsDown) override;

    void drawButtonText(juce::Graphics&, juce::TextButton&,
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
    // S612 specific colors will be handled mostly per-component name
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

    juce::String name = slider.getName();

    // Base body color
    juce::Colour bodyColor = juce::Colour(20, 20, 20); // Default black with green ring
    juce::Colour pointerColor = juce::Colour(64, 192, 128); // Green
    
    if (name == "REC LEVEL") {
        bodyColor = juce::Colour(210, 80, 20); // Orange
        pointerColor = juce::Colour(0, 0, 0); // Black pointer line
    } else if (name == "MONITOR") {
        bodyColor = juce::Colour(220, 220, 210); // White/Cream
        pointerColor = juce::Colour(0, 0, 0);
    } else if (name == "LFO_TUNE") {
        bodyColor = juce::Colour(220, 220, 200); // Yellowish white
        pointerColor = juce::Colour(0, 0, 0);
    } // else default
    
    // Draw shadow / base
    g.setColour(juce::Colour(10, 10, 10));
    g.fillEllipse(rx + 2, ry + 2, rw + 2, rw + 2); // Hard shadow

    // Ridges (simulate gear)
    g.setColour(juce::Colour(10, 10, 10));
    g.fillEllipse(rx, ry, rw, rw);
    g.setColour(bodyColor.darker(0.2f));
    g.fillEllipse(rx + 2, ry + 2, rw - 4, rw - 4);

    // Inner cap
    float capOffset = 4.0f;
    juce::Colour capColor = bodyColor;
    if (name != "REC LEVEL" && name != "MONITOR" && name != "LFO_TUNE") {
        // Black caps have green tops in S612 for LFO/Filter
        capColor = juce::Colour(40, 180, 120);
        capOffset = 8.0f;
    }
    
    g.setColour(capColor);
    g.fillEllipse(rx + capOffset, ry + capOffset, rw - capOffset * 2.0f, rw - capOffset * 2.0f);
    
    // Add realistic wear
    g.setColour(juce::Colour(uint8(255), 255, 255, uint8(30)));
    g.drawEllipse(rx + capOffset + 1, ry + capOffset + 1, rw - capOffset * 2 - 2, rw - capOffset * 2 - 2, 1.0f);

    // Pointer line
    juce::Path p;
    auto pointerLength = radius * 0.9f;
    auto pointerThickness = 2.5f;
    p.addRoundedRectangle(-pointerThickness * 0.5f, -radius + 2.0f, pointerThickness, pointerLength, 1.0f);
    p.applyTransform(juce::AffineTransform::rotation(angle).translated(centreX, centreY));
    g.setColour(pointerColor);
    g.fillPath(p);
}

void LookAndFeel::drawLinearSlider(juce::Graphics& g, int x, int y, int width, int height,
                                   float sliderPos, float minSliderPos, float maxSliderPos,
                                   const juce::Slider::SliderStyle style, juce::Slider& slider) {
    if (style == juce::Slider::LinearHorizontal) {
        // Dark track area
        g.setColour(juce::Colour(15, 15, 15));
        g.fillRoundedRectangle(x, y + height / 2.0f - 4.0f, width, 8.0f, 2.0f);
        
        g.setColour(juce::Colour(100, 100, 100));
        g.drawRect(x, (int)(y + height / 2.0f - 4.0f), width, 8, 1);

        auto thumbWidth = 14.0f;
        auto thumbHeight = 30.0f;
        auto thumbX = (float)x + sliderPos * ((float)width - thumbWidth);
        
        // Fader handle
        g.setColour(juce::Colour(30, 30, 30));
        g.fillRect(thumbX, y + height / 2.0f - thumbHeight / 2.0f, thumbWidth, thumbHeight);
        
        // White line on fader
        g.setColour(juce::Colour(240, 240, 240));
        g.fillRect(thumbX + thumbWidth / 2.0f - 1.0f, y + height / 2.0f - thumbHeight / 2.0f, 2.0f, thumbHeight);
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
    
    juce::String name = button.getName();
    juce::Colour btnCol = juce::Colour(80, 80, 80); // Default grey
    
    if (name.contains("REC_MODE")) btnCol = juce::Colour(220, 40, 60); // Red
    else if (name.contains("MIDI")) btnCol = juce::Colour(140, 140, 200); // Purple
    else if (name.contains("DATA")) btnCol = juce::Colour(210, 210, 200); // White
    else if (name.contains("MODE")) btnCol = juce::Colour(60, 180, 180); // Teal

    // Pressed darken
    if (isDownOrToggleOn) btnCol = btnCol.darker(0.3f);
    // highlight
    if (shouldDrawButtonAsHighlighted && !isDownOrToggleOn) btnCol = btnCol.brighter(0.1f);

    g.setColour(btnCol);
    g.fillRect(bounds.reduced(1)); // Square buttons for S612
    
    // Draw thick border for non-pressed to look 3D
    if (!isDownOrToggleOn) {
        g.setColour(btnCol.brighter(0.2f));
        g.drawLine(bounds.getX(), bounds.getY(), bounds.getRight(), bounds.getY(), 2.0f); // Top highlight
        g.drawLine(bounds.getX(), bounds.getY(), bounds.getX(), bounds.getBottom(), 2.0f); // Left highlight
        g.setColour(btnCol.darker(0.5f));
        g.drawLine(bounds.getX(), bounds.getBottom(), bounds.getRight(), bounds.getBottom(), 2.0f); // Bottom shadow
        g.drawLine(bounds.getRight(), bounds.getY(), bounds.getRight(), bounds.getBottom(), 2.0f); // Right shadow
    }
    
    // Tiny LED dot inside specific buttons
    if (name == "REC_MODE_NEW" || name == "REC_MODE_DUB" || name.contains("MODE")) {
        float cx = 4.0;
        float cy = bounds.getHeight() / 2.0f - 1.5f;
        g.setColour(isDownOrToggleOn ? juce::Colour(255, 40, 40) : juce::Colour(60, 10, 10)); // red led inside button
        g.fillEllipse(cx, cy, 3.0f, 3.0f);
    }
}

void LookAndFeel::drawButtonText(juce::Graphics& g, juce::TextButton& button,
                                 bool shouldDrawButtonAsHighlighted,
                                 bool shouldDrawButtonAsDown) {
    juce::Font font("Arial", 8.0f, juce::Font::bold);
    g.setFont(font);
    
    juce::String name = button.getName();
    // Dark text for white/light color buttons, otherwise white text
    if (name.contains("DATA") || name.contains("MONO")) {
        g.setColour(juce::Colour(20, 20, 20));
    } else {
        g.setColour(juce::Colour(240, 240, 240));
    }
    
    auto bounds = button.getLocalBounds();
    g.drawText(button.getButtonText(), bounds, juce::Justification::centred, true);
}

} // namespace UI
} // namespace S612
"""

plugin_editor_cpp = """#include "PluginEditor.h"
#include "PluginProcessor.h"
#include "S612Parameters.h"

namespace S612 {

PluginEditor::PluginEditor(PluginProcessor& p)
    : AudioProcessorEditor(&p), m_processor(p) {
    
    setSize(1000, 250); // Exact hardware rack ratio
    setLookAndFeel(&m_lookAndFeel);
    
    for (auto& flag : m_voiceFlags) flag = false;
    m_voiceFlags[0] = true;
    
    m_voiceLeds = std::make_unique<UI::VoiceLEDs>(m_voiceFlags);
    addAndMakeVisible(m_voiceLeds.get());
    
    auto& apvts = m_processor.getAPVTS();
    
    auto setupKnob = [&](UI::Knob& knob, const juce::String& baseName, const juce::String& uiName,
                         const char* paramID, float min = 0.0f, float max = 1.0f, float def = 0.5f) {
        addAndMakeVisible(knob);
        knob.setName(uiName); // UI Name for LookAndFeel (colors)
        knob.setRange(min, max);
        knob.setValue(def);
        return std::make_unique<juce::AudioProcessorValueTreeState::SliderAttachment>(apvts, paramID, knob);
    };
    
    auto setupFader = [&](UI::Fader& fader, const juce::String& name, 
                          const char* paramID, float min = 0.0f, float max = 1.0f, float def = 0.5f) {
        addAndMakeVisible(fader);
        fader.setName(name);
        fader.setSliderStyle(juce::Slider::LinearHorizontal);
        fader.setTextBoxStyle(juce::Slider::NoTextBox, false, 0, 0);
        fader.setRange(min, max);
        fader.setValue(def);
        return std::make_unique<juce::AudioProcessorValueTreeState::SliderAttachment>(apvts, paramID, fader);
    };
    
    auto setupButton = [&](juce::TextButton& btn, const juce::String& text, const juce::String& uiName, const char* paramID = nullptr) {
        addAndMakeVisible(btn);
        btn.setName(uiName);
        btn.setButtonText(text);
        if (paramID) {
            btn.setClickingTogglesState(true);
            return std::make_unique<juce::AudioProcessorValueTreeState::ButtonAttachment>(apvts, paramID, btn);
        }
        return std::unique_ptr<juce::AudioProcessorValueTreeState::ButtonAttachment>();
    };
    
    // REC SECTION
    m_recLevelAttachment = setupKnob(m_recLevelKnob, "REC LEVEL", "REC LEVEL", recLevel, 0.0f, 2.0f, 1.0f);
    m_monitorAttachment  = setupKnob(m_monitorKnob, "MONITOR", "MONITOR", outputLevel, 0.0f, 1.0f, 0.8f); // Fake logic map for testing
    
    setupButton(m_newBtn, "NEW", "REC_MODE_NEW");
    setupButton(m_overdubBtn, "OVER\\nDUB", "REC_MODE_DUB");
    
    // SCAN SECTION (SPLICING AND START/END)
    m_startAttachment = setupFader(m_startFader, "START", startPoint);
    m_endAttachment   = setupFader(m_endFader, "END", endPoint);
    
    // MODE SECTION
    setupButton(m_oneShotBtn, "ONE\\nSHOT", "MODE_ONE");
    setupButton(m_loopingBtn, "LOOPING", "MODE_LOOP");
    setupButton(m_altBtn, "ALTER-\\nNATING", "MODE_ALT");
    m_manualSpliceAttachment = setupButton(m_manualSpliceBtn, "MANUAL\\nSPLICE", "MODE_MANU", manualSplice);
    
    // DATA / MIDI Buttons (visual only for replica feel mostly)
    setupButton(m_chUpBtn, "CHANNEL\\nUP", "MIDI_UP");
    setupButton(m_chDownBtn, "CHANNEL\\nDOWN", "MIDI_DOWN");
    setupButton(m_keyTransBtn, "MONO\\n/ POLY", "DATA_MONO"); // reused mapping
    
    // LFO SECTION
    m_lfoSpeedAttachment = setupKnob(m_lfoSpeedKnob, "SPEED", "LFO_NORM", lfoSpeed, 0.0f, 1.0f, 0.5f);
    m_lfoDepthAttachment = setupKnob(m_lfoDepthKnob, "DEPTH", "LFO_NORM", lfoDepth);
    m_lfoDelayAttachment = setupKnob(m_lfoDelayKnob, "DELAY", "LFO_NORM", lfoDelay, 0.0f, 5.0f, 0.0f);
    m_tuneAttachment     = setupKnob(m_tuneKnob, "TUNE", "LFO_TUNE", tune, -100.0f, 100.0f, 0.0f);
    
    // OUTPUT SECTION
    m_filterAttachment   = setupKnob(m_filterKnob, "FILTER", "OUT_NORM", filter);
    m_decayAttachment    = setupKnob(m_decayKnob, "DECAY", "OUT_NORM", decay);
    // m_levelKnob mapping skipped in favor of monitor mapping above since S612 has LINE OUT and REC LEVEL but no separate level knob there, but wait, LFO and OUTPUT sections have SPEED, DEPTH, DELAY, TUNE, FILTER, DECAY, LEVEL.
    m_levelAttachment    = setupKnob(m_levelKnob, "LEVEL", "OUT_NORM", outputLevel);
    
    addAndMakeVisible(m_midiChDisplay);
    m_midiChDisplay.setChar('9'); // Default 9 for that S612 classic look
    
    addAndMakeVisible(m_inputMeter);
    
    startTimer(30);
}

PluginEditor::~PluginEditor() {
    stopTimer();
    setLookAndFeel(nullptr);
}

void PluginEditor::timerCallback() {
    m_inputMeter.setLevel(m_processor.getInputLevel());
    if (m_processor.getMidiActivity()) {
        m_midiLed.midiReceived();
    }
}

void PluginEditor::updateScanModeButtons(int mode) { }
void PluginEditor::updateMidiChannel(int ch) { m_midiChDisplay.setChar('0' + ch); }

void PluginEditor::paint(juce::Graphics& g) {
    // 1. Black Brushed Metal Base
    g.fillAll(juce::Colour(15, 15, 15));
    
    // Add artificial wear & tear
    juce::Random rng(1985); // Stable wear pattern
    g.setColour(juce::Colour(30, 30, 30));
    for (int i=0; i<1000; ++i) {
        g.fillRect(rng.nextInt(getWidth()), rng.nextInt(getHeight()), 2, 1);
    }
    for (int i=0; i<50; ++i) {
        float x = rng.nextFloat() * getWidth();
        float y = rng.nextFloat() * getHeight();
        g.setColour(juce::Colour(uint8(40), 40, 40, uint8(30)));
        g.drawEllipse(x, y, 10.0f, 10.0f, 0.5f);
    }
    
    // RACK SCREWS
    g.setColour(juce::Colour(150, 150, 150));
    g.fillEllipse(10, 10, 10, 10);
    g.fillEllipse(10, getHeight() - 20, 10, 10);
    g.fillEllipse(getWidth() - 20, 10, 10, 10);
    g.fillEllipse(getWidth() - 20, getHeight() - 20, 10, 10);
    
    // LOGO TYPOGRAPHY
    g.setColour(juce::Colour(215, 160, 60)); // Gold
    g.setFont(juce::Font("Arial Black", 24.0f, juce::Font::bold));
    g.drawText("AKAI", 60, 20, 100, 30, juce::Justification::left);
    
    g.setFont(juce::Font("Arial", 10.0f, juce::Font::bold));
    g.drawText("MIDI DIGITAL\\nSAMPLER", 140, 20, 100, 30, juce::Justification::left);
    
    g.setColour(juce::Colour(220, 200, 120)); // Lighter gold
    g.setFont(juce::Font("Arial Black", 26.0f, juce::Font::bold));
    g.drawText("S612", 220, 20, 100, 30, juce::Justification::left);

    // GOLD TEXT UNDER KNOBS
    g.setFont(juce::Font("Arial", 9.0f, juce::Font::bold));
    g.setColour(juce::Colour(210, 150, 50));
    auto t = [&](int x, int y, const char* str) {
        g.drawText(str, x, y, 60, 20, juce::Justification::centred);
    };
    
    t(70, 70, "REC LEVEL");
    t(160, 70, "MONITOR");
    
    // 2. CENTRAL DARK GLASS DISPLAY
    g.setColour(juce::Colour(8, 8, 8));
    g.fillRoundedRectangle(260, 20, 270, 100, 4.0f);
    g.setColour(juce::Colour(25, 25, 25));
    g.drawRoundedRectangle(260, 20, 270, 100, 4.0f, 1.5f);
    
    // "REC LEVEL" inside glass
    g.setColour(juce::Colour(150, 150, 150));
    g.setFont(juce::Font("Arial", 8.0f, juce::Font::bold));
    g.drawText("REC LEVEL", 270, 25, 60, 15, juce::Justification::left);
    g.drawText("MIDI CH", 400, 25, 40, 15, juce::Justification::left);
    g.drawText("I / O", 470, 25, 30, 15, juce::Justification::left);
    g.drawText("SAVE   LOAD", 455, 40, 60, 15, juce::Justification::left);
    
    // Horizontal start/splice label over faders outside the box
    g.setColour(juce::Colour(50, 180, 180));
    g.drawText("START/SPLICE", 540, 20, 80, 15, juce::Justification::left);
    
    // Scale for faders
    g.setColour(juce::Colour(180, 180, 180));
    for (int i=0; i<=10; ++i) {
        g.fillRect(545 + i*13, 50, 1, 4);
    }
    
    // LFO & OUTPUT SEC LABEL
    g.setColour(juce::Colour(210, 150, 50));
    g.drawText("LFO", 760, 15, 100, 15, juce::Justification::centred);
    g.drawLine(700, 22, 755, 22, 1);
    g.drawLine(780, 22, 920, 22, 1);
    
    t(690, 30, "SPEED"); t(750, 30, "DEPTH"); t(810, 30, "DELAY"); t(880, 30, "TUNE");
    
    g.drawText("OUTPUT", 730, 120, 100, 15, juce::Justification::centred);
    t(690, 135, "FILTER"); t(750, 135, "DECAY"); t(810, 135, "LEVEL");
}

void PluginEditor::resized() {
    // REC & MONITOR KNOBS (Left side)
    m_recLevelKnob.setBounds(75, 90, 55, 55);
    m_monitorKnob.setBounds(165, 90, 50, 50);
    
    // BUTTONS BELOW (ROW 1)
    int btnY = 135;
    m_newBtn.setBounds(260, btnY, 40, 30);
    m_overdubBtn.setBounds(260, btnY + 35, 40, 30);
    
    // BUTTONS BELOW (ROW 2 - MIDI / DATA)
    m_keyTransBtn.setBounds(330, btnY + 15, 35, 35);
    m_chDownBtn.setBounds(370, btnY + 15, 35, 35);
    m_chUpBtn.setBounds(410, btnY + 15, 35, 35);
    
    // SAVE VERIFY LOAD (Dummy text buttons, just place some real looking ones)
    // Using manual splice button for layout demonstration to match colors
    
    // BUTTONS BELOW (ROW 3 - MODE)
    m_oneShotBtn.setBounds(480, btnY + 15, 35, 35);
    m_loopingBtn.setBounds(520, btnY + 15, 35, 35);
    m_altBtn.setBounds(560, btnY + 15, 35, 35);
    m_manualSpliceBtn.setBounds(600, btnY + 15, 35, 35);
    
    // DARK GLASS CONTENT
    m_inputMeter.setBounds(270, 45, 120, 40); // VU Meter logic
    m_midiChDisplay.setBounds(405, 45, 30, 40); // the Red 7-seg 9
    
    // SLIDERS (Horizontal to the right of the glass box)
    m_startFader.setBounds(540, 35, 140, 25);
    m_endFader.setBounds(540, 65, 140, 25);
    
    // LFO GROUP
    m_lfoSpeedKnob.setBounds(695, 45, 50, 50);
    m_lfoDepthKnob.setBounds(755, 45, 50, 50);
    m_lfoDelayKnob.setBounds(815, 45, 50, 50);
    m_tuneKnob.setBounds(885, 45, 50, 50);
    
    // OUTPUT GROUP
    m_filterKnob.setBounds(695, 150, 50, 50);
    m_decayKnob.setBounds(755, 150, 50, 50);
    m_levelKnob.setBounds(815, 150, 50, 50);
    
    if (m_voiceLeds) {
        m_voiceLeds->setBounds(10, 100, 10, 10); // Hide mostly
    }
}

} // namespace S612
"""

# Write to disk
with open(r"f:\S612VSTi\Source\UI\S612LookAndFeel.h", "w") as f:
    f.write(look_and_feel_h)
with open(r"f:\S612VSTi\Source\UI\S612LookAndFeel.cpp", "w") as f:
    f.write(look_and_feel_cpp)
with open(r"f:\S612VSTi\Source\PluginEditor.cpp", "w") as f:
    f.write(plugin_editor_cpp)
