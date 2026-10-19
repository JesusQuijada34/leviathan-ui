# Leviathan-UI Native SDK for Windows

Este directorio inicia la migración del framework a DLL con ABI C estable. Está orientado a Windows x64 y a llamadas FFI desde C, C++, Rust, C#, Python `ctypes`, .NET P/Invoke y otros lenguajes capaces de invocar funciones C. El contrato se define en `include/levth.h`; los módulos comparten `LEVTH_ABI_VERSION` y se registran en el puente de `liblevthcore.dll` mediante `levth_module_register`.

## Estado y alcance

Esta rama todavía es una **migración parcial**, no una sustitución completa del producto Python. Ya están implementados y probados el registro/llamada entre módulos, la validación de opciones del instalador, la máquina de estados del asistente, el modelo de barra de progreso y un adaptador Win32/DWM para efectos básicos. El instalador visual, los servicios/notch ejecutables y las equivalencias de todos los widgets, parser y herramientas del proyecto aún no están portados. Las fuentes Python originales se conservan mientras no se demuestre equivalencia funcional y visual.

No se afirma compatibilidad de UI con cualquier toolkit/lenguaje: la ABI usa handles `HWND` para efectos de ventana en Windows; los consumidores FFI deben respetar el ciclo de vida del hilo UI de Win32.

## Build y pruebas

En Windows, abre **Developer Command Prompt for Visual Studio 2022** y ejecuta:

```bat
build.bat
package.bat
```

Los DLL se escriben en `build\windows-x64`; el ZIP de SDK queda en `dist\`. El archivo de recursos de Windows incorpora `app\app-icon.ico` y metadatos de versión/producto/editor en cada DLL. `build.sh` puede crear DLL Windows si hay MinGW-w64 y `windres`; sin esa toolchain solo ejecuta las pruebas portables C, no genera binarios Windows. También se puede usar CMake desde `native/`.

```sh
make -C native test
```

## Firma Authenticode

Por defecto los builds son unsigned. Para firmar, configura `LEVTH_SIGN_CERT_SHA1` con el thumbprint de un certificado de firma de código corporativo real, instalado con su clave privada en el almacén de certificados de Windows; `signtool` aplica SHA-256 y sello de tiempo. El proyecto no crea una identidad, certificado autofirmado ni una cadena de confianza. Un certificado autofirmado no da confianza pública en Windows.

El workflow que publica tags requiere los secretos de Actions `LEVTH_SIGNING_PFX_BASE64` y `LEVTH_SIGNING_PFX_PASSWORD`. Verifica que el certificado importado tenga clave privada, que el subject identifique a `influent` y que incluya el EKU de Code Signing antes de firmar y verificar cada DLL. Sin esos secretos no se publica una release etiquetada. El workflow de CI de la rama puede generar artefactos de prueba sin firma; esos artefactos no deben distribuirse como releases confiables.

## Opciones de instalación

`LevthInstallOptions` aplica una regla explícita: si `install_notch` es falso, `notch_style` debe ser `LEVTH_NOTCH_DISABLED` y no puede activarse el inicio de notch; si es verdadero, el estilo debe ser isla dinámica o recorte completo. La API actual solo valida y transmite estas preferencias: todavía no instala un servicio, no escribe en PATH/registro y no modifica componentes del sistema.

Las DLL nativas no deben registrarse con `regsvr32`: no son servidores COM. La integración futura se hará mediante carga dinámica/ABI y opciones explícitas, con instalación por usuario por defecto.
