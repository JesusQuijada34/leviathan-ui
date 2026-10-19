@echo off
setlocal EnableExtensions
cd /d "%~dp0"

where cl >nul 2>nul || (echo ERROR: abre este script desde Developer Command Prompt de Visual Studio 2022.& exit /b 2)
where rc >nul 2>nul || (echo ERROR: no se encontro Resource Compiler (rc.exe).& exit /b 2)

set "OUT=build\windows-x64"
if not exist "%OUT%" mkdir "%OUT%"

call :resource "%OUT%\version.res" || exit /b 3
call :compile_core || exit /b 4
call :compile_module setup || exit /b 5
call :compile_module window || exit /b 6
call :compile_module progressbar || exit /b 7

if defined LEVTH_SIGN_CERT_SHA1 (
  where signtool >nul 2>nul || (echo ERROR: hay certificado configurado pero no se encontro signtool.exe.& exit /b 8)
  for %%F in ("%OUT%\*.dll") do (
    signtool sign /fd SHA256 /sha1 "%LEVTH_SIGN_CERT_SHA1%" /tr https://timestamp.digicert.com /td SHA256 /d "Leviathan-UI Native Framework" "%%~fF" || exit /b 9
    signtool verify /pa /all "%%~fF" || exit /b 10
  )
  echo Firmas Authenticode aplicadas usando el certificado indicado por el propietario.
) else (
  echo AVISO: binarios sin firma. Define LEVTH_SIGN_CERT_SHA1 para usar un certificado corporativo valido con clave privada.
)

echo Build completado: %OUT%
exit /b 0

:resource
rc /nologo /fo "%~1" native\resources\levth_version.rc
if errorlevel 1 exit /b 1
exit /b 0

:compile_core
cl /nologo /std:c11 /O2 /W4 /MD /DLEVTH_CORE_BUILD /I native\include /Fo:"%OUT%\liblevthcore.obj" /LD native\src\liblevthcore.c "%OUT%\version.res" /link /INCREMENTAL:NO /DYNAMICBASE /NXCOMPAT /VERSION:1.0 /OUT:"%OUT%\liblevthcore.dll" /IMPLIB:"%OUT%\liblevthcore.lib"
if errorlevel 1 exit /b 1
exit /b 0

:compile_module
cl /nologo /std:c11 /O2 /W4 /MD /DLEVTH_MODULE_BUILD /I native\include /Fo:"%OUT%\liblevth%~1.obj" /LD native\src\liblevth%~1.c "%OUT%\version.res" "%OUT%\liblevthcore.lib" /link /INCREMENTAL:NO /DYNAMICBASE /NXCOMPAT /VERSION:1.0 /OUT:"%OUT%\liblevth%~1.dll" /IMPLIB:"%OUT%\liblevth%~1.lib" dwmapi.lib user32.lib
if errorlevel 1 exit /b 1
exit /b 0
