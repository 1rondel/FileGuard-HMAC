# FileGuard HMAC

Proyecto educativo en Python para aprender a detectar cambios en un archivo mediante un HMAC. El programa calcula un HMAC-SHA-256 para `documento.txt`, guarda una referencia en JSON y permite compararla más adelante.

## Qué demuestra

- Generar una clave de 32 bytes con `secrets`.
- Calcular un HMAC con `hmac` y `hashlib`.
- Guardar y cargar metadatos de referencia con `json`.
- Comparar los HMAC con `hmac.compare_digest()`.

## Archivos

- `fileguard.py`: menú, inicialización y verificación.
- `documento.txt`: archivo de muestra que se protege.
- `Documentacion-Joplin-FileGuard-HMAC.md`: nota de aprendizaje para Joplin; se conserva aparte del repositorio.

La clave local (`clave.key`) y la referencia generada (`referencia.json`) se crean o usan en tu equipo y se excluyen del repositorio.

## Requisitos y uso

Se necesita Python 3. El proyecto usa módulos incluidos en Python, por lo que no requiere paquetes externos.

Desde la carpeta `FileGuard-HMAC`:

```text
python fileguard.py
```

1. Elige **1** y confirma para inicializar la referencia del contenido actual.
2. Elige **2** para verificar el documento.
3. Para practicar, cambia una letra de `documento.txt` y vuelve a verificar; el HMAC debería dejar de coincidir.

La opción de verificación no actualiza la referencia. Para aceptar un cambio legítimo, inicialízala de nuevo conscientemente.

## Bibliotecas

`hmac`, `hashlib`, `secrets`, `json` y `pathlib` forman parte de la biblioteca estándar de Python.

## Estado y siguientes pasos

La lectura estática del código muestra que el flujo principal está conectado. Aún conviene comprobarlo ejecutando los casos de inicialización, verificación sin cambios y verificación después de modificar el documento. También faltan mensajes claros para JSON dañado o una clave vacía y configurar permisos restrictivos para `clave.key` en Windows.

## Limitaciones

Este es un ejercicio de aprendizaje, no una herramienta lista para producción. La clave y la referencia deben permanecer protegidas. Si alguien puede leer la clave y reemplazar la referencia, puede crear un HMAC que coincida con un documento modificado. El código actual tampoco restringe por sí mismo los permisos de la clave en Windows.
