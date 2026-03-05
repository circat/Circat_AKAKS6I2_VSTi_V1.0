#pragma once

namespace S612 {

// Parameter IDs - extern declarations
extern const char *sampleRate;
extern const char *startPoint;
extern const char *endPoint;
extern const char *splicePoint;
extern const char *manualSplice;
extern const char *scanMode;
extern const char *lfoSpeed;
extern const char *lfoDepth;
extern const char *lfoDelay;
extern const char *filter;
extern const char *filterType;      // Choice: 0=Moog, 1=MS20, 2=TB303, 3=SEM
extern const char *filterResonance; // Float 0.0-1.0
extern const char *filterSweep;     // Float 0.0-1.0 (SEM LP->Notch->HP)
extern const char *decay;
extern const char *transpose;
extern const char *tune;
extern const char *recLevel;
extern const char *outputLevel;
extern const char *monitorLevel;
extern const char *midiChannel;
extern const char *monoPoly;
extern const char *recFreq;
extern const char *midiLearn;

} // namespace S612
