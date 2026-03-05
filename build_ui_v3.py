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
#include "../../JuceLibraryCode/JuceHeader.h" // For BinaryData / S612Assets

namespace S612 {
namespace UI {

LookAndFeel::LookAndFeel() {
}

LookAndFeel::~LookAndFeel() {}

void LookAndFeel::drawRotarySlider(juce::Graphics& g, int x, int y, int width, int height,
                                   float sliderPos, const float rotaryStartAngle,
                                   const float rotaryEndAngle, juce::Slider& slider) {
    juce::String name = slider.getName();
    juce::Image knobImage;

    if (name == "REC LEVEL") {
        knobImage = juce::ImageCache::getFromMemory(S612Assets::knob_rec_png, S612Assets::knob_rec_pngSize);
    } else if (name == "MONITOR") {
        knobImage = juce::ImageCache::getFromMemory(S612Assets::knob_monitor_png, S612Assets::knob_monitor_pngSize);
    } else {
        // Use regular graphics for others if no image
        auto radius = (float)juce::jmin(width / 2, height / 2) - 4.0f;
        auto centreX = (float)x + (float)width  * 0.5f;
        auto centreY = (float)y + (float)height * 0.5f;
        auto rx = centreX - radius;
        auto ry = centreY - radius;
        auto rw = radius * 2.0f;
        auto angle = rotaryStartAngle + sliderPos * (rotaryEndAngle - rotaryStartAngle);

        juce::Colour bodyColor = (name == "LFO_TUNE") ? juce::Colour(220, 220, 200) : juce::Colour(20, 20, 20);
        juce::Colour pointerColor = (name == "LFO_TUNE") ? juce::Colour(0, 0, 0) : juce::Colour(64, 192, 128);

        g.setColour(juce::Colour(10, 10, 10));
        g.fillEllipse(rx + 2, ry + 2, rw + 2, rw + 2); // shadow
        g.fillEllipse(rx, ry, rw, rw);
        
        g.setColour(bodyColor.darker(0.2f));
        g.fillEllipse(rx + 2, ry + 2, rw - 4, rw - 4);

        float capOffset = (name == "LFO_TUNE") ? 4.0f : 8.0f;
        juce::Colour capColor = (name == "LFO_TUNE") ? bodyColor : juce::Colour(40, 180, 120);
        
        g.setColour(capColor);
        g.fillEllipse(rx + capOffset, ry + capOffset, rw - capOffset * 2.0f, rw - capOffset * 2.0f);

        juce::Path p;
        p.addRoundedRectangle(-1.25f, -radius + 2.0f, 2.5f, radius * 0.9f, 1.0f);
        p.applyTransform(juce::AffineTransform::rotation(angle).translated(centreX, centreY));
        g.setColour(pointerColor);
        g.fillPath(p);
        return;
    }

    if (knobImage.isValid()) {
        auto angle = rotaryStartAngle + sliderPos * (rotaryEndAngle - rotaryStartAngle);
        float scale = juce::jmin((float)width / knobImage.getWidth(), (float)height / knobImage.getHeight());
        
        juce::AffineTransform transform = juce::AffineTransform::rotation(angle, knobImage.getWidth() * 0.5f, knobImage.getHeight() * 0.5f)
                                          .scaled(scale)
                                          .translated(x + (width - knobImage.getWidth() * scale) * 0.5f, 
                                                      y + (height - knobImage.getHeight() * scale) * 0.5f);
        g.drawImageTransformed(knobImage, transform);
    }
}

void LookAndFeel::drawLinearSlider(juce::Graphics& g, int x, int y, int width, int height,
                                   float sliderPos, float minSliderPos, float maxSliderPos,
                                   const juce::Slider::SliderStyle style, juce::Slider& slider) {
    if (style == juce::Slider::LinearHorizontal) {
        juce::Image faderImg = juce::ImageCache::getFromMemory(S612Assets::fader_start_png, S612Assets::fader_start_pngSize);
        if (faderImg.isValid()) {
            float imgW = 16.0f;
            float imgH = 24.0f;
            auto thumbX = (float)x + sliderPos * ((float)width - imgW);
            g.drawImage(faderImg, thumbX, y + height / 2.0f - imgH / 2.0f, imgW, imgH, 0, 0, faderImg.getWidth(), faderImg.getHeight());
        } else {
            g.setColour(juce::Colour(100, 100, 100));
            g.fillRect(x + sliderPos * (width - 10.0f), (float)y, 10.0f, (float)height);
        }
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
    
    if (name == "REC_MODE_NEW") {
        juce::Image btnImg = juce::ImageCache::getFromMemory(S612Assets::btn_new_png, S612Assets::btn_new_pngSize);
        if (btnImg.isValid()) {
            g.drawImage(btnImg, bounds, juce::RectanglePlacement::stretchToFit);
            // Draw a basic red overlay if toggle is on to simulate LED
            if (isDownOrToggleOn) {
                g.setColour(juce::Colour(uint8(255), 0, 0, uint8(60)));
                g.fillRect(bounds);
                g.setColour(juce::Colours::red);
                g.fillEllipse(5, bounds.getHeight() / 2 - 3, 6, 6);
            }
            return;
        }
    }

    // Default procedural fallback for others
    juce::Colour btnCol = juce::Colour(80, 80, 80);
    if (name.contains("REC_MODE")) btnCol = juce::Colour(220, 40, 60);
    else if (name.contains("MIDI")) btnCol = juce::Colour(140, 140, 200);
    else if (name.contains("DATA")) btnCol = juce::Colour(210, 210, 200);
    else if (name.contains("MODE")) btnCol = juce::Colour(60, 180, 180);

    if (isDownOrToggleOn) btnCol = btnCol.darker(0.3f);
    if (shouldDrawButtonAsHighlighted && !isDownOrToggleOn) btnCol = btnCol.brighter(0.1f);

    g.setColour(btnCol);
    g.fillRect(bounds.reduced(1));
    
    if (!isDownOrToggleOn) {
        g.setColour(btnCol.brighter(0.2f));
        g.drawLine(bounds.getX(), bounds.getY(), bounds.getRight(), bounds.getY(), 2.0f);
        g.drawLine(bounds.getX(), bounds.getY(), bounds.getX(), bounds.getBottom(), 2.0f);
        g.setColour(btnCol.darker(0.5f));
        g.drawLine(bounds.getX(), bounds.getBottom(), bounds.getRight(), bounds.getBottom(), 2.0f);
        g.drawLine(bounds.getRight(), bounds.getY(), bounds.getRight(), bounds.getBottom(), 2.0f);
    }
    
    if (name == "REC_MODE_DUB" || name.contains("MODE")) {
        float cx = 4.0;
        float cy = bounds.getHeight() / 2.0f - 1.5f;
        g.setColour(isDownOrToggleOn ? juce::Colour(255, 40, 40) : juce::Colour(60, 10, 10));
        g.fillEllipse(cx, cy, 3.0f, 3.0f);
    }
}

void LookAndFeel::drawButtonText(juce::Graphics& g, juce::TextButton& button,
                                 bool shouldDrawButtonAsHighlighted,
                                 bool shouldDrawButtonAsDown) {
    if (button.getName() == "REC_MODE_NEW") return; // Img has text
    
    juce::Font font("Arial", 8.0f, juce::Font::bold);
    g.setFont(font);
    
    juce::String name = button.getName();
    if (name.contains("DATA") || name.contains("MONO")) {
        g.setColour(juce::Colour(20, 20, 20));
    } else {
        g.setColour(juce::Colour(240, 240, 240));
    }
    g.drawText(button.getButtonText(), button.getLocalBounds(), juce::Justification::centred, true);
}

} // namespace UI
} // namespace S612
"""

plugin_editor_cpp = """#include "PluginEditor.h"
#include "PluginProcessor.h"
#include "S612Parameters.h"
#include "S612Engine.h"
#include "../../JuceLibraryCode/JuceHeader.h"

namespace S612 {

PluginEditor::PluginEditor(PluginProcessor& p)
    : AudioProcessorEditor(&p), m_processor(p) {
    
    setSize(900, 250); // Original width and ratio
    setLookAndFeel(&m_lookAndFeel);
    
    for (auto& flag : m_voiceFlags) flag = false;
    m_voiceFlags[0] = true;
    
    m_voiceLeds = std::make_unique<UI::VoiceLEDs>(m_voiceFlags);
    addAndMakeVisible(m_voiceLeds.get());
    
    auto& apvts = m_processor.getAPVTS();
    
    auto setupKnob = [&](UI::Knob& knob, const juce::String& baseName, const juce::String& uiName,
                         const char* paramID, float min = 0.0f, float max = 1.0f, float def = 0.5f) {
        addAndMakeVisible(knob);
        knob.setName(uiName);
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
    m_monitorAttachment  = setupKnob(m_monitorKnob, "MONITOR", "MONITOR", outputLevel, 0.0f, 1.0f, 0.8f);
    
    setupButton(m_newBtn, "NEW", "REC_MODE_NEW");
    setupButton(m_overdubBtn, "OVER\\nDUB", "REC_MODE_DUB");
    
    // Hook up recording functions
    m_newBtn.setClickingTogglesState(true);
    m_newBtn.onClick = [this]() {
        if (m_newBtn.getToggleState()) {
            m_processor.getEngine().setRecordState(S612Engine::RecordState::RECORDING);
            m_overdubBtn.setToggleState(false, juce::sendNotification);
            m_processor.getEngine().setHasSample(false);
        } else {
            m_processor.getEngine().setRecordState(S612Engine::RecordState::IDLE);
        }
    };
    
    m_overdubBtn.setClickingTogglesState(true);
    m_overdubBtn.onClick = [this]() {
        if (m_overdubBtn.getToggleState()) {
            m_processor.getEngine().setRecordState(S612Engine::RecordState::OVERDUBBING);
            m_newBtn.setToggleState(false, juce::sendNotification);
        } else {
            m_processor.getEngine().setRecordState(S612Engine::RecordState::IDLE);
        }
    };

    // SCAN SECTION (SPLICING AND START/END)
    m_startAttachment = setupFader(m_startFader, "START", startPoint);
    m_endAttachment   = setupFader(m_endFader, "END", endPoint);
    
    // MODE SECTION
    setupButton(m_oneShotBtn, "ONE\\nSHOT", "MODE_ONE");
    setupButton(m_loopingBtn, "LOOPING", "MODE_LOOP");
    setupButton(m_altBtn, "ALTER-\\nNATING", "MODE_ALT");
    m_manualSpliceAttachment = setupButton(m_manualSpliceBtn, "MANUAL\\nSPLICE", "MODE_MANU", manualSplice);
    
    setupButton(m_chUpBtn, "CH\\nUP", "MIDI_UP");
    setupButton(m_chDownBtn, "CH\\nDOWN", "MIDI_DOWN");
    setupButton(m_keyTransBtn, "MONO", "DATA_MONO");
    
    // LFO SECTION
    m_lfoSpeedAttachment = setupKnob(m_lfoSpeedKnob, "SPEED", "LFO_NORM", lfoSpeed, 0.0f, 1.0f, 0.5f);
    m_lfoDepthAttachment = setupKnob(m_lfoDepthKnob, "DEPTH", "LFO_NORM", lfoDepth);
    m_lfoDelayAttachment = setupKnob(m_lfoDelayKnob, "DELAY", "LFO_NORM", lfoDelay, 0.0f, 5.0f, 0.0f);
    m_tuneAttachment     = setupKnob(m_tuneKnob, "TUNE", "LFO_TUNE", tune, -100.0f, 100.0f, 0.0f);
    
    // OUTPUT SECTION
    m_filterAttachment   = setupKnob(m_filterKnob, "FILTER", "OUT_NORM", filter);
    m_decayAttachment    = setupKnob(m_decayKnob, "DECAY", "OUT_NORM", decay);
    m_levelAttachment    = setupKnob(m_levelKnob, "LEVEL", "OUT_NORM", outputLevel);
    
    addAndMakeVisible(m_midiChDisplay);
    m_midiChDisplay.setChar('9');
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
    juce::Image bg = juce::ImageCache::getFromMemory(S612Assets::panel_section_png, S612Assets::panel_section_pngSize);
    if (bg.isValid()) {
        g.drawImage(bg, 0, 0, getWidth(), getHeight(), 0, 0, bg.getWidth(), bg.getHeight());
    } else {
        g.fillAll(juce::Colours::black);
    }
}

void PluginEditor::resized() {
    m_recLevelKnob.setBounds(65, 80, 80, 80);
    m_monitorKnob.setBounds(165, 90, 60, 60);
    
    int btnY = 160;
    m_newBtn.setBounds(275, 145, 38, 32); // Adjust to fit background grid
    m_overdubBtn.setBounds(275, 185, 38, 32);
    
    m_keyTransBtn.setBounds(335, btnY, 35, 35);
    m_chDownBtn.setBounds(375, btnY, 35, 35);
    m_chUpBtn.setBounds(415, btnY, 35, 35);
    
    m_oneShotBtn.setBounds(485, btnY, 35, 35);
    m_loopingBtn.setBounds(525, btnY, 35, 35);
    m_altBtn.setBounds(565, btnY, 35, 35);
    m_manualSpliceBtn.setBounds(605, btnY, 35, 35);
    
    // DARK GLASS CONTENT
    m_inputMeter.setBounds(280, 30, 110, 50); 
    
    // Make sure horizontal faders are visible
    m_startFader.setBounds(540, 48, 120, 20); // Top Fader
    m_endFader.setBounds(540, 85, 120, 20);   // Bottom Fader
    
    // LFO GROUP
    m_lfoSpeedKnob.setBounds(685, 45, 45, 45);
    m_lfoDepthKnob.setBounds(745, 45, 45, 45);
    m_lfoDelayKnob.setBounds(805, 45, 45, 45);
    m_tuneKnob.setBounds(865, 45, 55, 55);
    
    // OUTPUT GROUP
    m_filterKnob.setBounds(685, 150, 45, 45);
    m_decayKnob.setBounds(745, 150, 45, 45);
    m_levelKnob.setBounds(805, 150, 45, 45);
    
    if (m_voiceLeds) m_voiceLeds->setBounds(0, 0, 0, 0); // Hide
    m_midiChDisplay.setBounds(425, 32, 28, 48); // Hide for now or fix
}

} // namespace S612
"""

engine_cpp = """#include "S612Engine.h"
#include "S612VoiceManager.h"
#include "S612Parameters.h"
#include <cmath>

namespace S612
{

void S612Engine::prepareToPlay(double sampleRate, int maximumExpectedSamplesPerBlock)
{
    m_sampleBuffer.resize(MaxSamples, 0.0f);
    m_sampleRate = sampleRate;
    m_phase = 0.0;
}

void S612Engine::releaseResources()
{
    m_sampleBuffer.clear();
    m_sampleBuffer.shrink_to_fit();
}

void S612Engine::processBlock(juce::AudioBuffer<float>& buffer, 
                              const juce::MidiBuffer& midiMessages,
                              juce::AudioProcessorValueTreeState& apvts,
                              juce::AudioBuffer<float>& sidechainBuffer)
{
    auto numSamples = buffer.getNumSamples();
    buffer.clear();
    
    if (m_recordState == RecordState::RECORDING || m_recordState == RecordState::OVERDUBBING) {
        // Fix: Use sidechain input for sampling
        processRecording(sidechainBuffer, apvts);
    }
    
    if (m_voiceManager != nullptr && m_hasSample) {
        m_voiceManager->processBlock(buffer, numSamples);
    }
    
    auto* levelParam = apvts.getParameter("outputLevel");
    float outputLevel = levelParam ? levelParam->getValue() : 0.8f;
    
    for (int ch = 0; ch < buffer.getNumChannels(); ++ch) {
        auto* data = buffer.getWritePointer(ch);
        for (int i = 0; i < numSamples; ++i) {
            data[i] *= outputLevel;
        }
    }
}

void S612Engine::processRecording(const juce::AudioBuffer<float>& sidechainBuffer, 
                                  juce::AudioProcessorValueTreeState& apvts)
{
    if (sidechainBuffer.getNumChannels() == 0) return;
    
    auto* recLevelParam = apvts.getParameter("recLevel");
    float recLevel = recLevelParam ? recLevelParam->getValue() : 1.0f;
    
    int samplesToRecord = juce::jmin(sidechainBuffer.getNumSamples(), MaxSamples - m_writePosition);
    
    if (samplesToRecord > 0) {
        for (int i = 0; i < samplesToRecord; ++i) {
            float sample = sidechainBuffer.getSample(0, i) * recLevel;
            if (m_recordState == RecordState::RECORDING) {
                m_sampleBuffer[m_writePosition + i] = sample;
            } else if (m_recordState == RecordState::OVERDUBBING) {
                m_sampleBuffer[m_writePosition + i] += sample;
            }
        }
        m_writePosition += samplesToRecord;
        m_hasSample = true;
    } else {
        // Buffer full, stop recording automatically
        m_recordState = RecordState::IDLE;
        m_writePosition = 0;
    }
}

} // namespace S612
"""

# Write to disk
with open(r"f:\S612VSTi\Source\UI\S612LookAndFeel.cpp", "w") as f:
    f.write(look_and_feel_cpp)
with open(r"f:\S612VSTi\Source\PluginEditor.cpp", "w") as f:
    f.write(plugin_editor_cpp)
with open(r"f:\S612VSTi\Source\S612Engine.cpp", "w") as f:
    f.write(engine_cpp)
