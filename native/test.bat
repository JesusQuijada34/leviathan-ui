@echo off
setlocal EnableExtensions
cd /d "%~dp0\.."
if not exist build\windows-test mkdir build\windows-test
cl /nologo /std:c11 /O2 /W4 /MD /DLEVTH_CORE_BUILD /DLEVTH_MODULE_BUILD /I native\include ^
  native\tests\test_native.c native\src\liblevthcore.c native\src\liblevthsetup.c ^
  native\src\liblevthprogressbar.c native\src\liblevthwindow.c /Fobuild\windows-test\ ^
  /link /OUT:build\windows-test\test_native.exe dwmapi.lib user32.lib
if errorlevel 1 exit /b %errorlevel%
build\windows-test\test_native.exe
if errorlevel 1 exit /b %errorlevel%
