#include "S612FilterPanel.h"
#include "../S612Parameters.h"
#include <cmath>

namespace S612 {
namespace UI {

// Static inline colour lookups per filter type
// ───────────────────────────────────────────────────────────────────────────

// Panel background colours (painted per type):
//  Moog  : warm creme       (#D4C5A0)
//  MS-20 : matte black      (#1A1A1A)  + orange stripe
//  TB-303: silver grey      (#A8A8A8)  + orange stripe
//  SEM   : ivory            (#F0EAD6)  + blue pinstripes

juce::Colour FilterPanel::getPanelBaseColour(int type) {
  switch (type) {
  case 0:
    return juce::Colour(0xFFD4C5A0); // Moog creme
  case 1:
    return juce::Colour(0xFF1A1A1A); // MS-20 black
  case 2:
    return juce::Colour(0xFFA8A8A8); // TB-303 silver
  case 3:
    return juce::Colour(0xFFF0EAD6); // SEM ivory
  default:
    return juce::Colour(0xFF2A2A2A);
  }
}

juce::Colour FilterPanel::getLEDColour(int type) {
  switch (type) {
  case 0:
    return juce::Colour(0xFFFFCC00); // Moog: warm amber
  case 1:
    return juce::Colour(0xFFFF7700); // MS-20: orange
  case 2:
    return juce::Colour(0xFFFF4400); // TB-303: red-orange
  case 3:
    return juce::Colour(0xFF44AAFF); // SEM: blue
  default:
    return juce::Colours::white;
  }
}

juce::Colour FilterPanel::getAccentColour(int type) {
  switch (type) {
  case 0:
    return juce::Colour(0xFF8B7355); // Moog: dark tan
  case 1:
    return juce::Colour(0xFFFF6600); // MS-20: orange
  case 2:
    return juce::Colour(0xFFFF5500); // TB-303: orange
  case 3:
    return juce::Colour(0xFF2255AA); // SEM: blue
  default:
    return juce::Colours::grey;
  }
}

// ─── Constructor ─────────────────────────────────────────────────────────────

FilterPanel::FilterPanel(juce::AudioProcessorValueTreeState &apvts)
    : m_apvts(apvts) {

  // ── Cutoff knob ──────────────────────────────────────────────────────────
  addAndMakeVisible(m_cutoffKnob);
  m_cutoffKnob.setName("FILTER_CUTOFF");
  m_cutoffKnob.setKnobStyle(UI::Knob::STYLE_FILTER);
  m_cutoffAttachment =
      std::make_unique<juce::AudioProcessorValueTreeState::SliderAttachment>(
          apvts, S612::filter, m_cutoffKnob);

  // ── Resonance knob ───────────────────────────────────────────────────────
  addAndMakeVisible(m_resonanceKnob);
  m_resonanceKnob.setName("FILTER_RESONANCE");
  m_resonanceKnob.setKnobStyle(UI::Knob::STYLE_FILTER);
  m_resonanceAttachment =
      std::make_unique<juce::AudioProcessorValueTreeState::SliderAttachment>(
          apvts, S612::filterResonance, m_resonanceKnob);

  // ── Sweep knob (SEM only) ─────────────────────────────────────────────────
  addChildComponent(m_sweepKnob); // Starts invisible
  m_sweepKnob.setName("FILTER_SWEEP");
  m_sweepKnob.setKnobStyle(UI::Knob::STYLE_FILTER);
  m_sweepAttachment =
      std::make_unique<juce::AudioProcessorValueTreeState::SliderAttachment>(
          apvts, S612::filterSweep, m_sweepKnob);

  // ── NO TextButtons – selector is painted, clicks handled in mouseDown()
  readTypeFromAPVTS();
  updateKnobVisibility();
  startTimerHz(30); // 30 fps animation
}

FilterPanel::~FilterPanel() { stopTimer(); }

// ─── Switching Logic ─────────────────────────────────────────────────────────

void FilterPanel::switchToType(int newType) {
  if (newType == m_currentType)
    return;

  // Write to APVTS immediately (DSP hears it right away)
  writeTypeToAPVTS(newType);
  m_currentType = newType;

  // Start fade-out animation
  m_pendingType = newType;
  m_isFadingOut = true;
  m_isFadingIn = false;
}

void FilterPanel::writeTypeToAPVTS(int type) {
  if (auto *p = m_apvts.getParameter(S612::filterType))
    p->setValueNotifyingHost(p->convertTo0to1((float)type));
}

void FilterPanel::readTypeFromAPVTS() {
  if (auto *p = m_apvts.getRawParameterValue(S612::filterType))
    m_currentType = (int)(p->load() + 0.5f);

  m_displayType = m_currentType;
}

void FilterPanel::updateKnobVisibility() {
  const bool isSEM = (m_currentType == 3);
  m_sweepKnob.setVisible(isSEM);
}

// ─── Timer (Animation) ───────────────────────────────────────────────────────

void FilterPanel::timerCallback() {
  bool needsRepaint = false;

  if (m_isFadingOut) {
    m_fadeAlpha -= 0.12f; // ~4 frames to reach 0
    if (m_fadeAlpha <= 0.0f) {
      m_fadeAlpha = 0.0f;
      m_isFadingOut = false;
      m_isFadingIn = true;
      m_displayType = m_pendingType; // Swap panel at alpha=0
      updateKnobVisibility();
    }
    needsRepaint = true;
  }

  if (m_isFadingIn) {
    m_fadeAlpha += 0.1f; // slightly slower fade-in for smoothness
    if (m_fadeAlpha >= 1.0f) {
      m_fadeAlpha = 1.0f;
      m_isFadingIn = false;
    }
    needsRepaint = true;
  }

  // Also sync type from APVTS (non-destructive, in case of preset load)
  if (auto *p = m_apvts.getRawParameterValue(S612::filterType)) {
    int apvtsType = (int)(p->load() + 0.5f);
    if (apvtsType != m_currentType && !m_isFadingOut && !m_isFadingIn) {
      m_currentType = apvtsType;
      m_displayType = apvtsType;
      updateKnobVisibility();
      needsRepaint = true;
    }
  }

  if (needsRepaint)
    repaint();
}

// ─── Layout ──────────────────────────────────────────────────────────────────

void FilterPanel::resized() {
  const auto b = getLocalBounds();

  // Selector strip: top 22px
  const int selH = 22;
  const int btnW = 24;

  // Hit regions for the ◄ and ► buttons (painted in drawSelectorStrip)
  m_prevBtnArea =
      juce::Rectangle<int>(b.getX() + 2, b.getY() + 2, btnW, selH - 4);
  m_nextBtnArea = juce::Rectangle<int>(b.getRight() - btnW - 2, b.getY() + 2,
                                       btnW, selH - 4);

  // ─── KNOB LAYOUT: Centered under the selector strip ───
  const int centerX = b.getCentreX();
  const int knobSize = 60; // Equal size for all
  const int knobY = b.getY() + selH + (b.getHeight() - selH - knobSize) / 2;
  const int spacing = 75; // Distance from center for side knobs

  // Resonance is always in the middle slot
  m_resonanceKnob.setBounds(centerX - knobSize / 2, knobY, knobSize, knobSize);

  // Cutoff is always to the left
  m_cutoffKnob.setBounds(centerX - knobSize / 2 - spacing, knobY, knobSize,
                         knobSize);

  // Sweep (SEM only) is to the right
  m_sweepKnob.setBounds(centerX - knobSize / 2 + spacing, knobY, knobSize,
                        knobSize);
}

// ─── Mouse Handling (painted buttons) ────────────────────────────────────────

void FilterPanel::mouseDown(const juce::MouseEvent &e) {
  if (m_prevBtnArea.contains(e.getPosition()))
    switchToType((m_currentType + 3) % 4);
  else if (m_nextBtnArea.contains(e.getPosition()))
    switchToType((m_currentType + 1) % 4);
}

void FilterPanel::mouseMove(const juce::MouseEvent &e) {
  bool prev = m_prevBtnArea.contains(e.getPosition());
  bool next = m_nextBtnArea.contains(e.getPosition());
  if (prev != m_prevHover || next != m_nextHover) {
    m_prevHover = prev;
    m_nextHover = next;
    repaint();
  }
}

void FilterPanel::mouseExit(const juce::MouseEvent &) {
  m_prevHover = m_nextHover = false;
  repaint();
}

// ─── Paint ───────────────────────────────────────────────────────────────────

void FilterPanel::paint(juce::Graphics &g) {
  // Completely transparent background – shows AKAK background image
  drawSelectorStrip(g);
  drawPanelBackground(g, m_displayType, m_fadeAlpha);
}

void FilterPanel::drawPanelBackground(juce::Graphics &g, int type,
                                      float alpha) {
  const auto b = getLocalBounds().toFloat();
  const auto selH = 22.0f;
  const auto panelRect = b.withTrimmedTop(selH);

  // ── Restore Knob Labels ────────────────────────────────────────────────
  const int labelY = (int)panelRect.getBottom() - 22;
  drawKnobLabel(g, "CUTOFF", m_cutoffKnob.getX(), labelY,
                m_cutoffKnob.getWidth(), type);
  drawKnobLabel(g, "RESONANCE", m_resonanceKnob.getX(), labelY,
                m_resonanceKnob.getWidth(), type);

  if (type == 3) {
    drawKnobLabel(g, "SWEEP", m_sweepKnob.getX(), labelY,
                  m_sweepKnob.getWidth(), type);
  }
}

void FilterPanel::drawSelectorStrip(juce::Graphics &g) {
  const auto b = getLocalBounds();
  const int selH = 22;
  const auto selRect =
      juce::Rectangle<int>(b.getX(), b.getY(), b.getWidth(), selH).toFloat();

  // No strip background anymore - transparent to main background

  // ◄ button (left)
  const auto prevR = m_prevBtnArea.toFloat();
  g.setColour(m_prevHover ? juce::Colour(0xFF2A5070)
                          : juce::Colour(0xFF182838));
  g.fillRoundedRectangle(prevR, 3.0f);
  g.setColour(getLEDColour(m_currentType).brighter(0.1f));
  g.setFont(juce::Font("Arial", 10.0f, juce::Font::bold));
  g.drawText(juce::CharPointer_UTF8("\xe2\x97\x84"), prevR.toNearestInt(),
             juce::Justification::centred);

  // ► button (right)
  const auto nextR = m_nextBtnArea.toFloat();
  g.setColour(m_nextHover ? juce::Colour(0xFF2A5070)
                          : juce::Colour(0xFF182838));
  g.fillRoundedRectangle(nextR, 3.0f);
  g.setColour(getLEDColour(m_currentType).brighter(0.1f));
  g.drawText(juce::CharPointer_UTF8("\xe2\x96\xba"), nextR.toNearestInt(),
             juce::Justification::centred);

  // Type name in centre (vivid, larger, and shifted 5px up)
  g.setColour(getLEDColour(m_currentType).brighter(0.35f));
  g.setFont(juce::Font("Arial", 12.0f, juce::Font::bold));
  const int nameX = b.getX() + m_prevBtnArea.getWidth() + 6;
  const int nameW =
      b.getWidth() - m_prevBtnArea.getWidth() - m_nextBtnArea.getWidth() - 12;
  // nameY shifted by -5 (from 4 to -1)
  g.drawText(k_typeNames[m_currentType], nameX, b.getY() - 1, nameW, selH,
             juce::Justification::centred);

  // LED indicator dot (right of type name, left of ► button)
  const int ledX = b.getRight() - m_nextBtnArea.getWidth() - 14;
  const int ledY = b.getY() + (selH - 6) / 2;
  drawLED(g, ledX, ledY, m_currentType);
}

void FilterPanel::drawLED(juce::Graphics &g, int x, int y, int type) {
  const juce::Colour col = getLEDColour(type);

  // Glow
  g.setColour(col.withAlpha(0.35f));
  g.fillEllipse((float)(x - 2), (float)(y - 2), 10.0f, 10.0f);

  // Core
  juce::ColourGradient ledGrad(col.brighter(0.4f), (float)x + 1, (float)y + 1,
                               col.darker(0.2f), (float)x + 5, (float)y + 5,
                               true);
  g.setGradientFill(ledGrad);
  g.fillEllipse((float)x, (float)y, 6.0f, 6.0f);

  // Specular highlight
  g.setColour(juce::Colours::white.withAlpha(0.5f));
  g.fillEllipse((float)x + 1.0f, (float)y + 1.0f, 2.0f, 2.0f);
}

void FilterPanel::drawKnobLabel(juce::Graphics &g, const juce::String &text,
                                int x, int y, int w, int type) {
  // Use a high-contrast label color consistent with other labels
  g.setColour(juce::Colours::whitesmoke.withAlpha(0.8f));
  g.setFont(juce::Font("Arial", 10.0f, juce::Font::bold));
  g.drawText(text, x, y, w, 12, juce::Justification::centred);
}

} // namespace UI
} // namespace S612
