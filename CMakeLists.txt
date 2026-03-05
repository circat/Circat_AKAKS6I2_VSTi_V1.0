# S612 Sampler VST Plugin
# Akai S612 (1985) Exact Emulation
# JUCE 7, C++17

cmake_minimum_required(VERSION 3.22)

project(S612Plugin VERSION 2.0.0)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# JUCE 7 via FetchContent
include(FetchContent)
FetchContent_Declare(
    juce
    GIT_REPOSITORY https://github.com/juce-framework/JUCE.git
    GIT_TAG 7.0.9
)
set(JUCE_BUILD_EXTRAS OFF CACHE BOOL "" FORCE)
set(JUCE_BUILD_EXAMPLES OFF CACHE BOOL "" FORCE)
FetchContent_MakeAvailable(juce)

# Plugin Metadata
set(PLUGIN_NAME "Circat AKAK S6I2 V2.0")
set(PLUGIN_MANUFACTURER "CIRCAT")
set(PLUGIN_MANUFACTURER_CODE "CIRC")
set(PLUGIN_CODE "S62A")
set(PLUGIN_VERSION "2.0.0")

# Audio Plugin Configuration
juce_add_plugin(${PROJECT_NAME}
    PRODUCT_NAME ${PLUGIN_NAME}
    FORMATS VST3
    MICROPHONE_PERMISSION_ENABLED FALSE
    VST3_CATEGORIES Instrument Synth Sampler
    IS_SYNTH TRUE
    NEEDS_MIDI_INPUT TRUE
)

juce_add_binary_data(S612PanelBg
    HEADER_NAME "S612PanelBg.h"
    NAMESPACE "S612BG"
    SOURCES
        Assets/panel_bg.png
        START.wav
)

target_sources(${PROJECT_NAME} PRIVATE
    Source/PluginProcessor.cpp
    Source/PluginEditor.cpp
    Source/S612Parameters.cpp
    Source/S612Engine.cpp
    Source/S612Voice.cpp
    Source/S612VoiceManager.cpp
    Source/S612Sound.cpp
    Source/S612Scanner.cpp
    Source/S612MidiHandler.cpp
    Source/S612InputStage.cpp
    Source/S612AnalogFilter.cpp
    Source/CircuitBentFilter.cpp
    Source/S612LFO.cpp
    Source/S612DSPCommon.cpp
    Source/UI/S612LookAndFeel.cpp
    Source/UI/S612Knob.cpp
    Source/UI/S612Fader.cpp
    Source/UI/S612SevenSegDisplay.cpp
    Source/UI/S612VoiceLEDs.cpp
    Source/UI/S612InputMeter.cpp
    Source/UI/S612MidiLed.cpp
    Source/UI/S612FilterPanel.cpp
)
target_link_libraries(${PROJECT_NAME} PRIVATE
    S612PanelBg
    juce::juce_audio_utils
    juce::juce_audio_processors
    juce::juce_audio_formats
    juce::juce_audio_basics
    juce::juce_gui_extra
    juce::juce_gui_basics
    juce::juce_graphics
    juce::juce_events
    juce::juce_core
    juce::juce_data_structures
)

target_include_directories(${PROJECT_NAME} PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/Source
    ${CMAKE_BINARY_DIR}/juce_binarydata_S612PanelBg/JuceLibraryCode
)

# Compile Definitions
target_compile_definitions(${PROJECT_NAME} PRIVATE
    JUCE_WEB_BROWSER=0
    JUCE_USE_CURL=0
    JUCE_VST3_CAN_REPLACE_VST2=0
    JUCE_DISPLAY_SPLASH_SCREEN=0
    JUCE_IS_SYNTH=1
)

# Compiler flags for JUCE
target_compile_options(${PROJECT_NAME} PRIVATE /EHsc)

# Windows specific
if(WIN32)
    add_compile_definitions(UNICODE _UNICODE)
endif()

# macOS specific
if(APPLE)
    set_target_properties(${PROJECT_NAME} PROPERTIES
        MACOSX_BUNDLE_MINIMUM_SYSTEM_VERSION "10.13"
    )
endif()
