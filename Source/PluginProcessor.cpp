#include "PluginProcessor.h"
#include "PluginEditor.h"
#include "S612Engine.h"
#include "S612MidiHandler.h"
#include "S612PanelBg.h"
#include "S612Parameters.h"
#include "S612VoiceManager.h"

using namespace S612;

namespace S612 {

struct PluginProcessor::Impl {
  S612Engine engine;
  S612MidiHandler midiHandler;
  S612VoiceManager voiceManager;
  juce::AudioBuffer<float> sidechainBuffer;

  Impl() = default;
};

PluginProcessor::PluginProcessor()
    : AudioProcessor(
          BusesProperties()
              .withInput("Input", juce::AudioChannelSet::stereo(), true)
              .withOutput("Output", juce::AudioChannelSet::stereo(), true)
              .withInput("Sidechain", juce::AudioChannelSet::stereo(), false)),
      m_apvts(*this, nullptr, "S612Parameters", createParameterLayout()) {
  m_impl = std::make_unique<Impl>();

  // Initialize voice manager with engine
  m_impl->voiceManager.setEngine(&m_impl->engine);
  m_impl->midiHandler.setVoiceManager(&m_impl->voiceManager);
  m_impl->midiHandler.setAPVTS(&m_apvts);
  m_impl->engine.setVoiceManager(&m_impl->voiceManager);

  // Initialize default params for "First Preset"
  if (auto *p = m_apvts.getParameter(recFreq))
    p->setValueNotifyingHost(0.0f); // 32k
  if (auto *p = m_apvts.getParameter(filter))
    p->setValueNotifyingHost(1.0f); // Open
  if (auto *p = m_apvts.getParameter(outputLevel))
    p->setValueNotifyingHost(0.8f);

  // Load default sample from binary data
  m_impl->engine.loadSampleFromMemory(S612BG::START_wav,
                                      (size_t)S612BG::START_wavSize, 32000.0);

  // Explicitly sync the rate to the voice manager for the start sample
  m_impl->voiceManager.setOriginalSampleRate(32000.0);
}

PluginProcessor::~PluginProcessor() = default;

juce::AudioProcessorValueTreeState::ParameterLayout
PluginProcessor::createParameterLayout() {
  juce::AudioProcessorValueTreeState::ParameterLayout layout;

  // Recording
  layout.add(std::make_unique<juce::AudioParameterFloat>(
      recLevel, "REC LEVEL", juce::NormalisableRange<float>(0.0f, 2.0f, 0.01f),
      1.0f));

  // Scanning
  layout.add(std::make_unique<juce::AudioParameterFloat>(
      startPoint, "START/SPLICE",
      juce::NormalisableRange<float>(0.0f, 1.0f, 0.001f), 0.0f));
  layout.add(std::make_unique<juce::AudioParameterFloat>(
      endPoint, "END POINT", juce::NormalisableRange<float>(0.0f, 1.0f, 0.001f),
      1.0f));
  layout.add(std::make_unique<juce::AudioParameterFloat>(
      splicePoint, "SPLICE", juce::NormalisableRange<float>(0.0f, 1.0f, 0.001f),
      0.8f));
  layout.add(std::make_unique<juce::AudioParameterBool>(manualSplice,
                                                        "MANU. SPLICE", false));
  layout.add(std::make_unique<juce::AudioParameterInt>(
      scanMode, "SCAN MODE", 0, 2, 0)); // 0=OneShot, 1=Looping, 2=Alternating

  // LFO
  layout.add(std::make_unique<juce::AudioParameterFloat>(
      lfoSpeed, "LFO SPEED", juce::NormalisableRange<float>(0.0f, 1.0f, 0.01f),
      0.5f));
  layout.add(std::make_unique<juce::AudioParameterFloat>(
      lfoDepth, "LFO DEPTH", juce::NormalisableRange<float>(0.0f, 1.0f, 0.01f),
      0.0f));
  layout.add(std::make_unique<juce::AudioParameterFloat>(
      lfoDelay, "LFO DELAY", juce::NormalisableRange<float>(0.0f, 5.0f, 0.1f),
      0.0f));

  // Filter & Decay
  layout.add(std::make_unique<juce::AudioParameterFloat>(
      filter, "FILTER", juce::NormalisableRange<float>(0.0f, 1.0f, 0.01f),
      1.0f));
  layout.add(std::make_unique<juce::AudioParameterFloat>(
      filterType, "FILTER TYPE",
      juce::NormalisableRange<float>(0.0f, 3.0f, 1.0f),
      0.0f)); // 0=Moog,1=MS20,2=TB303,3=SEM
  layout.add(std::make_unique<juce::AudioParameterFloat>(
      filterResonance, "RESONANCE",
      juce::NormalisableRange<float>(0.0f, 1.0f, 0.001f), 0.0f));
  layout.add(std::make_unique<juce::AudioParameterFloat>(
      filterSweep, "FILTER SWEEP",
      juce::NormalisableRange<float>(0.0f, 1.0f, 0.001f), 0.0f));
  layout.add(std::make_unique<juce::AudioParameterFloat>(
      decay, "DECAY", juce::NormalisableRange<float>(0.0f, 1.0f, 0.01f), 0.5f));
  layout.add(std::make_unique<juce::AudioParameterFloat>(
      outputLevel, "LEVEL", juce::NormalisableRange<float>(0.0f, 1.0f, 0.01f),
      0.8f));
  layout.add(std::make_unique<juce::AudioParameterFloat>(
      monitorLevel, "MONITOR",
      juce::NormalisableRange<float>(0.0f, 1.0f, 0.01f), 0.8f));

  // Transpose & Tune
  layout.add(std::make_unique<juce::AudioParameterInt>(transpose, "TRANSPOSE",
                                                       -24, 24, 0));
  layout.add(std::make_unique<juce::AudioParameterFloat>(
      tune, "TUNE", juce::NormalisableRange<float>(-100.0f, 100.0f, 1.0f),
      0.0f));

  // MIDI
  layout.add(std::make_unique<juce::AudioParameterInt>(midiChannel, "MIDI CH",
                                                       0, 9, 0)); // 0=Omni
  layout.add(
      std::make_unique<juce::AudioParameterBool>(monoPoly, "MONO MODE", false));

  // Sample Rate / Frequency
  layout.add(std::make_unique<juce::AudioParameterInt>(
      recFreq, "REC FREQ", 0, 2, 0)); // 0=32k, 1=16k, 2=8k

  layout.add(std::make_unique<juce::AudioParameterBool>(midiLearn, "MIDI LEARN",
                                                        false));

  return layout;
}

void PluginProcessor::prepareToPlay(double sampleRate,
                                    int maximumExpectedSamplesPerBlock) {
  m_impl->engine.prepareToPlay(sampleRate, maximumExpectedSamplesPerBlock);
  m_impl->voiceManager.prepareToPlay(sampleRate,
                                     maximumExpectedSamplesPerBlock);
  m_impl->midiHandler.prepareToPlay(sampleRate, maximumExpectedSamplesPerBlock);

  // Pre-allocate sidechain buffer to avoid allocations in processBlock
  m_impl->sidechainBuffer.setSize(2, maximumExpectedSamplesPerBlock);
  m_impl->sidechainBuffer.clear();
}

void PluginProcessor::releaseResources() {
  m_impl->engine.releaseResources();
  m_impl->voiceManager.releaseResources();
}

bool PluginProcessor::isBusesLayoutSupported(const BusesLayout &layouts) const {
  // Accept any layout for now
  return true;
}

void PluginProcessor::processBlock(juce::AudioBuffer<float> &buffer,
                                   juce::MidiBuffer &midiMessages) {
  // Track MIDI activity
  if (!midiMessages.isEmpty()) {
    m_lastMidiTime = juce::Time::getCurrentTime().getMilliseconds();
  }

  int numSamples = buffer.getNumSamples();

  // Ensure sidechain buffer is cleared before use
  m_impl->sidechainBuffer.clear();

  // Get sidechain input (Bus 1) for sampling and monitoring
  auto sidechainBus = getBusBuffer(buffer, true, 1);

  if (sidechainBus.getNumChannels() > 0) {
    int numCh = juce::jmin(m_impl->sidechainBuffer.getNumChannels(),
                           sidechainBus.getNumChannels());
    for (int ch = 0; ch < numCh; ++ch) {
      if (sidechainBus.getReadPointer(ch) != nullptr)
        m_impl->sidechainBuffer.copyFrom(ch, 0, sidechainBus, ch, 0,
                                         numSamples);
      else
        m_impl->sidechainBuffer.clear(ch, 0, numSamples);
    }
  } else {
    // If no sidechain is connected, use main input as fallback
    int numCh = juce::jmin(m_impl->sidechainBuffer.getNumChannels(),
                           buffer.getNumChannels());
    for (int ch = 0; ch < numCh; ++ch) {
      m_impl->sidechainBuffer.copyFrom(ch, 0, buffer, ch, 0, numSamples);
    }
  }

  // Process MIDI
  m_impl->midiHandler.processBlock(midiMessages, numSamples);

  // Process audio with sidechain input
  m_impl->engine.processBlock(buffer, midiMessages, m_apvts,
                              m_impl->sidechainBuffer);
}

juce::AudioProcessorEditor *PluginProcessor::createEditor() {
  return new PluginEditor(*this);
}

void PluginProcessor::getStateInformation(juce::MemoryBlock &destData) {
  auto state = m_apvts.copyState();
  std::unique_ptr<juce::XmlElement> xml(state.createXml());
  copyXmlToBinary(*xml, destData);
}

void PluginProcessor::setStateInformation(const void *data, int sizeInBytes) {
  std::unique_ptr<juce::XmlElement> xmlState(
      getXmlFromBinary(data, sizeInBytes));
  if (xmlState && xmlState->hasTagName(m_apvts.state.getType())) {
    m_apvts.replaceState(juce::ValueTree::fromXml(*xmlState));
  }
}

float PluginProcessor::getInputLevel() const {
  return m_impl->engine.getInputLevel();
}

bool PluginProcessor::getMidiActivity() const {
  auto now = juce::Time::getCurrentTime().getMilliseconds();
  return (now - m_lastMidiTime) < 100;
}

S612Engine &PluginProcessor::getEngine() { return m_impl->engine; }

void PluginProcessor::setMidiChannel(int ch) {
  if (m_impl)
    m_impl->voiceManager.setMidiChannel(ch);
}

S612MidiHandler &PluginProcessor::getMidiHandler() {
  return m_impl->midiHandler;
}

} // namespace S612

// JUCE Plugin Entry Point
juce::AudioProcessor *createPluginFilter() {
  return new S612::PluginProcessor();
}
