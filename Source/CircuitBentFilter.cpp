#include "CircuitBentFilter.h"
#include <algorithm>

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

// ─── Lifecycle ──────────────────────────────────────────────────────────────

void CircuitBentFilter::prepare(double sampleRate) {
  m_sr = (sampleRate > 0.0) ? sampleRate : 44100.0;
  reset();
}

void CircuitBentFilter::reset() { s1 = s2 = s3 = s4 = 0.0f; }

// ─── Coefficient Update ──────────────────────────────────────────────────────

void CircuitBentFilter::updateCoefficients(float cutoffHz, float resonance,
                                           FilterType type) {
  m_currentType = type;

  // Bilinear pre-warp: maps digital frequency to analog prototype frequency
  const float T = 1.0f / (float)m_sr;
  const float wd = 2.0f * (float)M_PI * cutoffHz;
  const float wa = (2.0f / T) * std::tan(wd * T * 0.5f);
  float g = wa * T * 0.5f;

  // Hard stability limit – g >= 1 causes the ZDF integrators to blow up
  g = std::min(g, 0.998f);
  g = std::max(g, 0.0001f);
  m_coeffs.g = g;

  // Model-specific resonance mapping
  // Each hardware unit has a different feedback topology and range
  switch (type) {
  case FilterType::Moog:
    // 0–4.0; self-oscillation begins around 3.8.
    // We cap at 3.95 to keep it stable by default.
    m_coeffs.res = resonance * 3.95f;
    break;

  case FilterType::MS20:
    // Sallen-Key: res drives diode-clipped feedback.
    // Range 0–2.5 gives the characteristic scream.
    m_coeffs.res = resonance * 2.5f;
    break;

  case FilterType::TB303:
    // Diode cascade: tight mapping, subtle pole-spread handles the squelch.
    m_coeffs.res = resonance * 0.96f;
    break;

  case FilterType::SEM:
    // SVF damping coefficient: 1.0 = max damping (open), 0.0 = self-osc.
    // Invert so user "resonance" feels natural (more = more resonant).
    m_coeffs.res = 1.0f - resonance * 0.97f;
    break;
  }
}

// ─── Main Dispatch
// ────────────────────────────────────────────────────────────

float CircuitBentFilter::processSample(float x) {
  float out;
  switch (m_currentType) {
  case FilterType::Moog:
    out = processMoog(x);
    break;
  case FilterType::MS20:
    out = processMS20(x);
    break;
  case FilterType::TB303:
    out = processTB303(x);
    break;
  case FilterType::SEM:
    out = processSEM(x);
    break;
  default:
    out = processMoog(x);
    break;
  }

  // Safety net – NaN / Inf guard
  if (!std::isfinite(out)) {
    reset();
    return 0.0f;
  }
  return out;
}

// ─── Moog Ladder (24 dB/oct) ─────────────────────────────────────────────────
//
// Classic 4-pole ladder with tanh saturation in every stage.
// The feedback loop creates the characteristic bass-robbing resonance peak.
// Drive path: input → (tanh feedback subtract) → 4× integrator+tanh → output
//
float CircuitBentFilter::processMoog(float x) noexcept {
  const float g = m_coeffs.g;
  const float res = m_coeffs.res;

  // Feedback from output of last integrator, clipped via tanh
  const float feedback = fastTanh(s4 * res);

  // Input with feedback subtraction (ladder characteristic)
  const float driven = fastTanh(x - feedback);

  // Stage 1 – ZDF integrator + per-stage saturation
  const float v1 = (driven - s1) * g;
  float y1 = v1 + s1;
  s1 = y1 + v1;
  y1 = fastTanh(y1);

  // Stage 2
  const float v2 = (y1 - s2) * g;
  float y2 = v2 + s2;
  s2 = y2 + v2;
  y2 = fastTanh(y2);

  // Stage 3
  const float v3 = (y2 - s3) * g;
  float y3 = v3 + s3;
  s3 = y3 + v3;
  y3 = fastTanh(y3);

  // Stage 4 – final pole, output taken here
  const float v4 = (y3 - s4) * g;
  const float y4 = v4 + s4;
  s4 = y4 + v4;

  return y4;
}

// ─── MS-20 Sallen-Key (12 dB/oct) ────────────────────────────────────────────
//
// 2-pole Sallen-Key filter with nonlinear diode clipping in the resonance path.
// Self-oscillation is stable (bounded by tanh). Agressive, "screaming"
// character.
//
float CircuitBentFilter::processMS20(float x) noexcept {
  const float g = m_coeffs.g;
  const float res = m_coeffs.res;

  // Nonlinear feedback – diode clipping modelled by tanh
  const float fb = fastTanh(res * s2);

  // ZDF Sallen-Key topology
  // Denominator ensures TPT (topology preserving transform) stability
  const float denom = 1.0f + g * (2.0f + g);
  const float hp = (x - fb - (2.0f * g + 1.0f) * s1 - s2) / denom;
  const float bp = g * hp + s1;
  s1 = bp + g * hp;
  const float lp = g * bp + s2;
  s2 = lp + g * bp;

  return lp;
}

// ─── TB-303 Diode Cascade (~18 dB/oct) ───────────────────────────────────────
//
// Four-pole ladder with a deliberately spread 4th pole (g * 0.72 instead of g).
// This asymmetry shifts the phase response and creates the rubbery "squelch"
// characteristic of the 303. The classic acid sound lives in the resonance peak
// sweeping near the spread pole.
//
float CircuitBentFilter::processTB303(float x) noexcept {
  const float g = m_coeffs.g;
  const float g4 = g * 0.72f; // 4th pole deliberately detuned
  const float res = m_coeffs.res;

  // Feedback from 4th pole output
  const float input = x - res * s4;

  // Pole 1
  const float v1 = (input - s1) * g;
  const float y1 = v1 + s1;
  s1 = y1 + v1;

  // Pole 2
  const float v2 = (y1 - s2) * g;
  const float y2 = v2 + s2;
  s2 = y2 + v2;

  // Pole 3
  const float v3 = (y2 - s3) * g;
  const float y3 = v3 + s3;
  s3 = y3 + v3;

  // Pole 4 – spread (g4 ≠ g)
  const float v4 = (y3 - s4) * g4;
  const float y4 = v4 + s4;
  s4 = y4 + v4;

  return y4;
}

// ─── Oberheim SEM SVF (12 dB/oct, LP/Notch/HP) ───────────────────────────────
//
// Standard ZDF state variable filter (Topology Preserving Transform).
// The m_semSweep parameter interpolates the output:
//   0.0 = pure LP, 0.5 = Notch, 1.0 = pure HP
// This matches the Oberheim SEM's "TYPE" knob sweep behaviour.
//
float CircuitBentFilter::processSEM(float x) noexcept {
  const float g = m_coeffs.g;
  const float r = m_coeffs.res; // Already mapped: high = damped

  // ZDF SVF – Zoelzer / Välimäki TPT formulation
  const float hp = (x - (2.0f * r + g) * s1 - s2) / (1.0f + g * (2.0f * r + g));
  const float bp = g * hp + s1;
  s1 = g * hp + bp;
  const float lp = g * bp + s2;
  s2 = g * bp + lp;

  // Continuous LP→Notch→HP morphing
  // At sweep=0.5, notch = lp - hp (cancels the bandpass, gives notch response)
  const float sweep = m_semSweep;
  if (sweep <= 0.5f) {
    // LP → Notch
    const float t = sweep * 2.0f; // 0–1
    const float notch = lp + hp;  // simplified notch approximation
    return lp + t * (notch - lp);
  } else {
    // Notch → HP
    const float t = (sweep - 0.5f) * 2.0f; // 0–1
    const float notch = lp + hp;
    return notch + t * (hp - notch);
  }
}
