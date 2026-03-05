#pragma once
#include <cmath>

/**
 * CircuitBentFilter – Virtual Analog ZDF Filter Stage
 *
 * Four authentic hardware emulations using Zero-Delay Feedback (ZDF) topology.
 * This module has NO JUCE dependency and can be used in any C++ audio project.
 *
 * Emulated hardware:
 *   Moog   : Moog Minimoog Ladder (24dB/oct, 4-pole, tanh saturation per stage)
 *   MS20   : Korg MS-20 Sallen-Key (12dB/oct, diode clipping in feedback)
 *   TB303  : Roland TB-303 Diode Cascade (~18dB, pole-spread "squelch")
 *   SEM    : Oberheim SEM State Variable (12dB/oct, LP/Notch/HP sweep)
 */

enum class FilterType { Moog = 0, MS20 = 1, TB303 = 2, SEM = 3 };

struct FilterCoefficients {
    float g   = 0.0f;  // Warped frequency coefficient
    float res = 0.0f;  // Resonance / feedback amount (model-specific scaling)
    float h   = 0.0f;  // Reserved for future ZDF correction
};

class CircuitBentFilter {
public:
    CircuitBentFilter() = default;

    /** Call once before processing. sampleRate must be > 0. */
    void prepare(double sampleRate);

    /**
     * Recompute filter coefficients.
     * @param cutoffHz   Cutoff frequency in Hz  (safe range: 20 – sr/2)
     * @param resonance  Normalised resonance     (0.0 = off, 1.0 = max / self-osc)
     * @param type       Filter topology to use
     */
    void updateCoefficients(float cutoffHz, float resonance, FilterType type);

    /** Process a single sample. Call updateCoefficients() before each block. */
    float processSample(float x);

    /** Set the SEM sweep position (0.0 = LP, 0.5 = Notch, 1.0 = HP).
     *  Only audible when currentType == SEM. */
    void setSEMSweep(float sweep01) { m_semSweep = sweep01; }

    /** Reset all internal filter state (call on silence / voice restart). */
    void reset();

private:
    // Four state variables – shared across models
    float s1 = 0.0f, s2 = 0.0f, s3 = 0.0f, s4 = 0.0f;

    FilterCoefficients m_coeffs;
    FilterType m_currentType = FilterType::Moog;
    double m_sr = 44100.0;

    // SEM sweep position (LP→Notch→HP)
    float m_semSweep = 0.0f;

    // ── Per-model processing ────────────────────────────────────────────────
    float processMoog(float x) noexcept;
    float processMS20(float x) noexcept;
    float processTB303(float x) noexcept;
    float processSEM(float x) noexcept;

    // Fast tanh approximation (Padé, accurate to ±2% up to |x|=3)
    static inline float fastTanh(float x) noexcept {
        float x2 = x * x;
        return x * (27.0f + x2) / (27.0f + 9.0f * x2);
    }
};
