@echo off
cd /d F:\S612VSTi
call "C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvarsall.bat" x64
set WindowsSDKDir=C:\Program Files (x86)\Windows Kits\10
rmdir /s /q build 2>nul
mkdir build
"C:\Program Files\CMake\bin\cmake.exe" -G "Visual Studio 17 2022" -A x64 -S . -B build
cd build
"C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\MSBuild\Current\Bin\amd64\MSBuild.exe" S612Plugin.sln /p:Configuration=Release /p:Platform=x64 /v:minimal
pause
