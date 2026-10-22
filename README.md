# FileGuard HMAC

Proyecto educativo en Python para aprender a detectar cambios en un archivo usando HMAC-SHA-256. El programa está en desarrollo y permite practicar la generación de una clave local, el cálculo del HMAC y la comparación con una referencia JSON.

## Objetivos de aprendizaje

- Crear una clave aleatoria con `secrets`.
- Calcular un HMAC con `hmac` y `hashlib`.
- Guardar y leer datos de referencia con `json`.
- Comparar valores HMAC con `hmac.compare_digest()`.
- Practicar validación de archivos, manejo de errores y organización de funciones.

## Archivos

- `fileguard.py`: menú y funciones de creación y verificación.
- `documento.txt`: ejemplo local para practicar la verificación.
- `.gitignore`: excluye la clave y la referencia generadas localmente.

`clave.key`, `referencia.json` y la documentación de aprendizaje para Joplin se mantienen fuera de los archivos versionados. No deben subirse al repositorio.

## Requisitos

Python 3. El código utiliza módulos de la biblioteca estándar; no requiere instalar paquetes con `pip`.

## Iniciar el programa

Desde la carpeta del proyecto, ejecuta:

```text
python fileguard.py
```

El menú ofrece inicializar la referencia, verificar el documento o salir. La creación/verificación todavía está en desarrollo; revisa los pendientes antes de confiar en sus resultados.

## Estado actual y pendientes

Este es un proyecto de aprendizaje, no una herramienta lista para proteger archivos importantes. Queda por completar y comprobar, entre otros, estos puntos:

- Asegurar que las funciones de creación usen una sola vez el resultado de cada llamada y detengan el flujo cuando la persona cancela.
- Completar el caso en que falta la clave para que la creación de la referencia reciba la clave correcta.
- Separar claramente inicialización y verificación para que verificar no inicialice datos accidentalmente.
- Manejar una referencia JSON inválida o con campos y tipos inesperados.
- Definir cómo se confirma una actualización de una referencia existente.
- Probar rutas cuando el programa se inicia desde otra carpeta y configurar permisos locales adecuados para la clave en Windows.

## Seguridad y limitaciones

La clave y la referencia deben mantenerse protegidas. Si una persona puede leer la clave y reemplazar la referencia, puede generar un HMAC válido para un documento modificado. `.gitignore` evita añadir esos archivos localmente a Git, pero no protege su contenido en el equipo. No uses este ejercicio para datos importantes o sensibles.
