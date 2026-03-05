import os

base_dir = r"f:\S612VSTi\Source"

plugin_editor_h = """#pragma once
#include <juce_audio_processors/juce_audio_processors.h>
#include <juce_gui_basics/juce_gui_basics.h>
#include "UI/S612LookAndFeel.h"
#include "UI/S612Knob.h"
#include "UI/S612Fader.h"
#include "UI/S612SevenSegDisplay.h"
#include "UI/S612VoiceLEDs.h"

namespace S612 {

class PluginProcessor;

class PluginEditor : public juce::AudioProcessorEditor {
public:
    explicit PluginEditor(PluginProcessor&);
    ~PluginEditor() override;

    void paint(juce::Graphics&) override;
    void resized() override;

private:
    PluginProcessor& m_processor;
    UI::LookAndFeel m_lookAndFeel;
    
    // JUCE standard attachment types omitted for brevity if not requested fully implemented APVTS yet
    // Assuming UI focus first
    
    // ===== REC SECTION =====
    UI::Knob recLevelKnob;
    UI::Knob monitorKnob;
    juce::TextButton newBtn;
    juce::TextButton overdubBtn;
    juce::TextButton recLed; // Or custom LED
    
    // ===== SCAN SECTION =====
    UI::Fader startFader;
    UI::Fader endFader;
    
    // ===== MODE SECTION =====
    juce::TextButton oneShotBtn;
    juce::TextButton loopingBtn;
    juce::TextButton alternatingBtn;
    juce::TextButton manualSpliceBtn;
    
    // ===== LFO SECTION =====
    UI::Knob lfoSpeedKnob;
    UI::Knob lfoDepthKnob;
    UI::Knob lfoDelayKnob;
    
    // ===== OUTPUT SECTION =====
    UI::Knob filterKnob;
    UI::Knob decayKnob;
    UI::Knob levelKnob;
    
    // ===== KEY TRANS & TUNE =====
    juce::TextButton keyTransBtn;
    UI::Knob tuneKnob;
    
    // ===== MIDI SECTION =====
    UI::SevenSegDisplay midiChDisplay;
    juce::TextButton chUpBtn;
    juce::TextButton chDownBtn;
    
    // ===== VOICE LEDs =====
    // Note: Dummy array for now since PluginProcessor might not have getVoiceActiveFlags exposed
    std::array<std::atomic<bool>, 6> dummyVoiceFlags;
    std::unique_ptr<UI::VoiceLEDs> voiceLeds;
    
    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(PluginEditor)
};

} // namespace S612
"""

plugin_editor_cpp = """#include "PluginEditor.h"
#include "PluginProcessor.h"

namespace S612 {

PluginEditor::PluginEditor(PluginProcessor& p)
    : AudioProcessorEditor(&p), m_processor(p) {
    
    setSize(920, 420);
    setLookAndFeel(&m_lookAndFeel);
    
    for (auto& flag : dummyVoiceFlags) flag = false;
    dummyVoiceFlags[0] = true; // test
    
    voiceLeds = std::make_unique<UI::VoiceLEDs>(dummyVoiceFlags);
    addAndMakeVisible(voiceLeds.get());
    
    auto makeKnob = [&](UI::Knob& knob, const juce::String& name, UI::Knob::Style style = UI::Knob::STYLE_STANDARD) {
        addAndMakeVisible(knob);
        knob.setName(name);
        knob.setKnobStyle(style);
    };
    
    auto makeBtn = [&](juce::TextButton& btn, const juce::String& name) {
        addAndMakeVisible(btn);
        btn.setButtonText(name);
        btn.setClickingTogglesState(true);
    };
    
    makeKnob(recLevelKnob, "REC LEVEL");
    makeKnob(monitorKnob, "MONITOR");
    makeBtn(newBtn, "NEW");
    makeBtn(overdubBtn, "OVERDUB");
    
    addAndMakeVisible(startFader);
    startFader.setName("START/SPLICE");
    addAndMakeVisible(endFader);
    endFader.setName("END POINT");
    
    makeBtn(oneShotBtn, "ONE SHOT");
    makeBtn(loopingBtn, "LOOPING");
    makeBtn(alternatingBtn, "ALT");
    makeBtn(manualSpliceBtn, "MANU. SPLICE");
    
    makeKnob(lfoSpeedKnob, "SPEED", UI::Knob::STYLE_LFO);
    makeKnob(lfoDepthKnob, "DEPTH", UI::Knob::STYLE_LFO);
    makeKnob(lfoDelayKnob, "DELAY", UI::Knob::STYLE_LFO);
    
    makeKnob(filterKnob, "FILTER");
    makeKnob(decayKnob, "DECAY");
    makeKnob(levelKnob, "LEVEL");
    
    makeBtn(keyTransBtn, "KEY TRANS");
    makeKnob(tuneKnob, "TUNE");
    
    addAndMakeVisible(midiChDisplay);
    midiChDisplay.setChar('1');
    
    makeBtn(chUpBtn, "CH UP");
    makeBtn(chDownBtn, "CH DOWN");
}

PluginEditor::~PluginEditor() {
    setLookAndFeel(nullptr);
}

void PluginEditor::paint(juce::Graphics& g) {
    g.fillAll(juce::Colour(28, 28, 28)); // brushed metal look base
    
    // Borders
    g.setColour(juce::Colour(58, 58, 58));
    g.drawRect(0, 0, getWidth(), getHeight(), 1);
    
    // Header
    g.setColour(juce::Colour(220, 220, 220));
    g.setFont(juce::Font("Helvetica Neue", 36.0f, juce::Font::bold));
    g.drawText("AKAI", 30, 18, 120, 44, juce::Justification::left);
    
    g.setFont(juce::Font("Helvetica Neue", 36.0f, juce::Font::bold));
    g.drawText("S612", 140, 15, 140, 50, juce::Justification::left);
    
    g.setFont(juce::Font("Helvetica Neue", 11.0f, juce::Font::plain));
    g.setColour(juce::Colour(128, 128, 128));
    g.drawText("MIDI DIGITAL SAMPLER", 30, 55, 200, 15, juce::Justification::left);
    
    // Section BGs
    auto drawSection = [&](int x, int y, int w, int h, const juce::String& title) {
        g.setColour(juce::Colour(42, 42, 42));
        g.fillRect(x, y, w, h);
        g.setColour(juce::Colour(58, 58, 58));
        g.drawRect(x, y, w, h, 1);
        if (title.isNotEmpty()) {
            g.setFont(juce::Font("Helvetica Neue", 10.0f, juce::Font::bold));
            g.setColour(juce::Colour(128, 128, 128));
            g.drawText(title, x + 10, y + 10, w - 20, 15, juce::Justification::left);
        }
    };
    
    // drawSection(15, 85, 130, 310, "REC");
    // Layout matching spec coords
}

void PluginEditor::resized() {
    // Exact positions from `S612_UI_Design_Spec.md`
    // REC SECTION
    recLevelKnob.setBounds(30, 125, 100, 100);
    monitorKnob.setBounds(30, 235, 80, 80);
    newBtn.setBounds(30, 320, 100, 28);
    overdubBtn.setBounds(30, 355, 100, 28);
    
    // SCAN SECTION
    startFader.setBounds(170, 105, 50, 250);
    endFader.setBounds(250, 105, 50, 250);
    
    // MODE SECTION
    oneShotBtn.setBounds(355, 115, 120, 28);
    loopingBtn.setBounds(355, 150, 120, 28);
    alternatingBtn.setBounds(355, 185, 120, 28);
    manualSpliceBtn.setBounds(355, 220, 120, 28);
    
    // LFO SECTION
    lfoSpeedKnob.setBounds(510, 120, 50, 50);
    lfoDepthKnob.setBounds(565, 120, 50, 50);
    lfoDelayKnob.setBounds(620, 120, 50, 50);
    
    // OUTPUT SECTION
    filterKnob.setBounds(705, 120, 60, 60);
    decayKnob.setBounds(780, 120, 60, 60);
    levelKnob.setBounds(855, 120, 60, 60);
    
    // KEY TRANS & TUNE
    keyTransBtn.setBounds(495, 280, 80, 28);
    tuneKnob.setBounds(585, 270, 50, 50);
    
    // MIDI SECTION
    midiChDisplay.setBounds(700, 280, 40, 25);
    chUpBtn.setBounds(750, 280, 25, 25);
    chDownBtn.setBounds(780, 280, 25, 25);
    
    if (voiceLeds) {
        voiceLeds->setBounds(815, 280, 80, 20); // roughly placed
    }
}

} // namespace S612
"""

with open(os.path.join(base_dir, "PluginEditor.h"), "w") as f:
    f.write(plugin_editor_h)
with open(os.path.join(base_dir, "PluginEditor.cpp"), "w") as f:
    f.write(plugin_editor_cpp)

print("PluginEditor files modified.")
