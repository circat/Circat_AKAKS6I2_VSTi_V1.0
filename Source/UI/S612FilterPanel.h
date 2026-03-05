#pragma once
#include "../CircuitBentFilter.h" // For FilterType enum
#include "S612Knob.h"
#include <juce_audio_processors/juce_audio_processors.h>
#include <juce_gui_basics/juce_gui_basics.h>
#include <memory>

namespace S612 {
namespace UI {

/**
 * S612FilterPanel
 *
 * A self-contained JUCE component that renders the filter section
 * in the lower-right corner of the plugin (x:660–960, y:120–230).
 *
 * Features:
 *  - Hardware-styled vintage panel for each of the 4 filter types
 *  - Smooth alpha crossfade when switching filter type (~150ms)
 *  - Type selector strip with illuminated LED indicator
 *  - Cutoff knob (large), Resonance knob (smaller), SEM Sweep knob (only in SEM
 * mode)
 *  - All knobs attached to APVTS via SliderAttachment
 */
class FilterPanel : public juce::Component, public juce::Timer {
public:
  FilterPanel(juce::AudioProcessorValueTreeState &apvts);
  ~FilterPanel() override;

  void paint(juce::Graphics &g) override;
  void resized() override;
  void timerCallback() override;

private:
  // ── APVTS reference ───────────────────────────────────────────────────────
  juce::AudioProcessorValueTreeState &m_apvts;

  // ── Filter state ──────────────────────────────────────────────────────────
  int m_currentType = 0; // 0=Moog, 1=MS20, 2=TB303, 3=SEM
  int m_displayType = 0; // Type being painted (may differ during fade)

  // ── Animation state ───────────────────────────────────────────────────────
  float m_fadeAlpha = 1.0f; // Current panel alpha
  bool m_isFadingOut = false;
  bool m_isFadingIn = false;
  int m_pendingType = 0;

  // ── Knobs (managed here, attached to APVTS) ───────────────────────────────
  Knob m_cutoffKnob;
  Knob m_resonanceKnob;
  Knob m_sweepKnob; // Only visible in SEM mode

  std::unique_ptr<juce::AudioProcessorValueTreeState::SliderAttachment>
      m_cutoffAttachment, m_resonanceAttachment, m_sweepAttachment;

  // ── Type selector: no TextButton – drawn in paint(), clicked via mouseDown
  juce::Rectangle<int> m_prevBtnArea; // ◄ hit region (set in resized)
  juce::Rectangle<int> m_nextBtnArea; // ► hit region
  bool m_prevHover = false;
  bool m_nextHover = false;

  // ── Type label display (painted) ──────────────────────────────────────────
  // Names for selector strip
  static constexpr const char *k_typeNames[4] = {"MOOG", "MS-20", "TB-303",
                                                 "SEM"};

  // ── Draw helpers ──────────────────────────────────────────────────────────
  void drawPanelBackground(juce::Graphics &g, int type, float alpha);
  void drawSelectorStrip(juce::Graphics &g);
  void drawLED(juce::Graphics &g, int x, int y, int type);
  void drawKnobLabel(juce::Graphics &g, const juce::String &text, int x, int y,
                     int w, int type);

  void mouseDown(const juce::MouseEvent &e) override;
  void mouseMove(const juce::MouseEvent &e) override;
  void mouseExit(const juce::MouseEvent &e) override;

  // ── Panel identity helpers ────────────────────────────────────────────────
  static juce::Colour getPanelBaseColour(int type);
  static juce::Colour getLEDColour(int type);
  static juce::Colour getAccentColour(int type);

  // ── Switching logic ───────────────────────────────────────────────────────
  void switchToType(int newType);
  void updateKnobVisibility();
  void writeTypeToAPVTS(int type);
  void readTypeFromAPVTS();

  JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(FilterPanel)
};

} // namespace UI
} // namespace S612
