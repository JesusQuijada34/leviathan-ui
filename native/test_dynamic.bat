@echo off
setlocal EnableExtensions
cd /d "%~dp0\.."
cl /nologo /std:c11 /O2 /W4 /MD /Fobuild\windows-test\test_dynamic_windows.obj native\tests\test_dynamic_windows.c /link /OUT:build\windows-test\test_dynamic_windows.exe
if errorlevel 1 exit /b %errorlevel%
build\windows-test\test_dynamic_windows.exe
if errorlevel 1 exit /b %errorlevel%
