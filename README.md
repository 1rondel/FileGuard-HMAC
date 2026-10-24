# FileGuard HMAC

Proyecto educativo en Python para aprender a detectar cambios en un archivo mediante HMAC-SHA-256.

## Qué hace

- Crea una clave secreta local de 32 bytes cuando se inicializa el proyecto y la persona acepta crearla.
- Calcula un HMAC-SHA-256 para el contenido de `documento.txt`.
- Guarda el nombre del archivo, el algoritmo y el HMAC en `referencia.json`.
- Comprueba el documento comparando el HMAC actual con el guardado mediante `hmac.compare_digest()`.
- Valida campos, tipos, algoritmo, longitud y caracteres hexadecimales de la referencia.
- Maneja errores habituales al leer o guardar los archivos.

## Archivos

- `fileguard.py`: menú y funciones de creación, cálculo y verificación.
- `documento.txt`: archivo de ejemplo que se verifica.
- `.gitignore`: excluye la clave y la referencia generadas localmente.

`clave.key` y `referencia.json` se generan en la misma carpeta que `fileguard.py` y no deben subirse al repositorio. La documentación completa de la sesión para Joplin se mantiene en el archivo local `Documentacion-Joplin-FileGuard-HMAC.md`, excluido de Git.

## Requisitos y ejecución

Se requiere Python 3. El programa usa únicamente módulos de la biblioteca estándar, por lo que no necesita paquetes de `pip`.

Desde una terminal:

```text
python fileguard.py
```

El programa puede iniciarse desde otra carpeta: las rutas de los archivos se construyen a partir de la ubicación de `fileguard.py`.

En el menú, elige:

1. Inicializar o actualizar la referencia.
2. Verificar el archivo.
3. Salir.

Al crear o actualizar la referencia, el programa solicita confirmación. Al verificar, requiere que ya existan el documento, la clave y la referencia; no crea esos archivos automáticamente.

## Estado del proyecto

FileGuard es un ejercicio educativo en desarrollo. Ya incluye creación de clave, creación o actualización confirmada de referencia, verificación del HMAC, validación básica de los datos y manejo de errores de lectura y escritura. La ejecución manual comprobó que encuentra sus archivos al iniciarse desde fuera de la carpeta del proyecto.

Quedan mejoras por practicar: separar la lógica de la interfaz de consola, añadir pruebas automatizadas para los casos válidos y errores, mejorar los mensajes y revisar la protección de la clave según el sistema operativo. No se ha probado exhaustivamente cada posible entrada o fallo del sistema.

## Seguridad y limitaciones

El HMAC permite comprobar la integridad del contenido cuando la clave secreta es confiable. Si alguien puede modificar tanto `clave.key` como `referencia.json`, puede crear una referencia válida para un archivo modificado. `.gitignore` evita que Git incluya esos archivos por defecto, pero no cifra ni protege los archivos en el equipo.

Al actualizar la referencia se acepta el estado actual del documento como nueva base de comparación. No uses este proyecto de aprendizaje para proteger información importante o sensible.
