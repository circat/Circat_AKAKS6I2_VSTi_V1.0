@echo off
setlocal
cd /d "%~dp0"
call "C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvarsall.bat" x64
set "WindowsSDKDir=C:\Program Files (x86)\Windows Kits\10"
if exist build rmdir /s /q build
mkdir build
"C:\Program Files\CMake\bin\cmake.exe" -G "Visual Studio 17 2022" -A x64 -S . -B build
if %errorlevel% neq 0 exit /b %errorlevel%
cd build
"C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\MSBuild\Current\Bin\amd64\MSBuild.exe" S612Plugin.sln /p:Configuration=Release /p:Platform=x64 /v:minimal
if %errorlevel% neq 0 exit /b %errorlevel%
echo Build Successful!
