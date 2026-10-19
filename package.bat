@echo off
setlocal EnableExtensions
cd /d "%~dp0"
call build.bat
if errorlevel 1 exit /b %errorlevel%
set "OUT=build\windows-x64"
if not exist dist mkdir dist
if exist dist\Leviathan-UI-Native-SDK-1.0.5-win-x64.zip del /q dist\Leviathan-UI-Native-SDK-1.0.5-win-x64.zip
powershell -NoProfile -ExecutionPolicy Bypass -Command "$stage='build\sdk-package'; if(Test-Path $stage){Remove-Item -Recurse -Force $stage}; New-Item -ItemType Directory -Force $stage,($stage+'\include'),($stage+'\bin') | Out-Null; Copy-Item 'native\include\levth.h' ($stage+'\include\'); Copy-Item 'app\app-icon.ico' ($stage+'\'); Copy-Item 'native\README.md' ($stage+'\'); Copy-Item 'build\windows-x64\*.dll' ($stage+'\bin\'); Compress-Archive -Path ($stage+'\*') -DestinationPath 'dist\Leviathan-UI-Native-SDK-1.0.5-win-x64.zip' -Force"
if errorlevel 1 exit /b 10
echo Package ready: dist\Leviathan-UI-Native-SDK-1.0.5-win-x64.zip
