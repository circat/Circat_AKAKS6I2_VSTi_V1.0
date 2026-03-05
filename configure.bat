@echo off
call "C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvarsall.bat" x64
"C:\Program Files\CMake\bin\cmake.exe" -G "Visual Studio 17 2022" -A x64 -S . -B build
