@echo off
chcp 65001 >nul
cls
echo ==========================================
echo  Leviathan-UI Release Script v1.0.4
echo ==========================================
echo.

REM Verificar que estamos en el directorio correcto
if not exist "pyproject.toml" (
    echo ERROR: No se encuentra pyproject.toml
    echo Asegurate de ejecutar este script desde la raiz de leviathan-ui
    pause
    exit /b 1
)

echo [1/6] Verificando archivos...
if not exist "dist\leviathan_ui-1.0.4-py3-none-any.whl" (
    echo ERROR: No se encuentra la rueda compilada
    echo Ejecuta primero: python -m build --wheel
    pause
    exit /b 1
)

echo [2/6] Agregando cambios a git...
git add -A
if errorlevel 1 (
    echo ERROR: Fallo al agregar archivos
    pause
    exit /b 1
)

echo [3/6] Creando commit...
git commit -m "Release v1.0.4: Instalador profesional estilo NSIS, PyQt6 fixes, docs"
if errorlevel 1 (
    echo ERROR: Fallo al crear commit
    pause
    exit /b 1
)

echo [4/6] Subiendo a GitHub...
git push origin main
if errorlevel 1 (
    echo ERROR: Fallo al subir a GitHub
    pause
    exit /b 1
)

echo [5/6] Creando release en GitHub...
gh release create v1.0.4 --title "Leviathan-UI v1.0.4 - Instalador Profesional" --notes-file CHANGELOG.md dist/leviathan_ui-1.0.4-py3-none-any.whl
if errorlevel 1 (
    echo ERROR: Fallo al crear release
    echo Intenta crear el release manualmente desde: https://github.com/JesusQuijada34/leviathan-ui/releases
    pause
    exit /b 1
)

echo [6/6] Subiendo a PyPI...
echo Usando credenciales de .pypirc...
python -m twine upload dist/leviathan_ui-1.0.4-py3-none-any.whl
if errorlevel 1 (
    echo ERROR: Fallo al subir a PyPI
    pause
    exit /b 1
)

echo.
echo ==========================================
echo  Release v1.0.4 COMPLETADO EXITOSAMENTE
echo ==========================================
echo.
echo - Codigo subido a GitHub
echo - Release creado con rueda adjunta
echo - Paquete subido a PyPI
echo.
pause
