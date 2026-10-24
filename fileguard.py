import hmac  # Permite calcular HMAC y comparar sus resultados de forma segura.
import hashlib  # Proporciona SHA-256, usado como función hash del HMAC.
import secrets  # Genera bytes aleatorios para la clave secreta.
import json  # Lee y escribe la referencia en formato JSON.
import pathlib  # Representa las rutas de los archivos del proyecto.

carpeta_programa = pathlib.Path(__file__).resolve().parent

# Archivo cuyo contenido se comprobará.
Pr_Fi = carpeta_programa / "documento.txt"
SKey = carpeta_programa / "clave.key"
reference = carpeta_programa / "referencia.json"


def k_creator():
    # Lee la clave existente o pregunta si debe crear una nueva.
    try:
        if SKey.exists():
        # Devuelve el contenido binario de la clave.
            clave = SKey.read_bytes()
            if len(clave) != 32:
                print("La clave no tiene el tamaño esperado")
                return None
            return clave
    except OSError:
        print("No se pudo leer la clave")
        return None
    if not SKey.exists():
        # Solicita permiso antes de generar y guardar una clave nueva.
            
            keypreg = input("desea crear una s/n?").strip().lower()
            if keypreg == "s":
                try:
            # Genera una clave aleatoria de 32 bytes y la guarda localmente.
                    clave = secrets.token_bytes(32)
                    SKey.write_bytes(clave)
                except OSError:
                    print("No se pudo guardar la clave")
                    return None
            # Devuelve la clave guardada para que quien llamó pueda usarla.
                return clave
            else:
            # None representa que la persona canceló la creación.
                return None

def r_creator():
    # Comprueba que exista el documento antes de pedir crear una clave.
    if not Pr_Fi.exists():
        print("Documento no encontrado")
        return

    # Pide confirmación según exista o no una referencia.
    if reference.exists():
        ver = input("La referencia existe, desea actualizarla s/n?").lower().strip()
        if ver != "s":
            print("No se actualizo la referencia.")
            return reference
    else:
        print("La referencia no fue encontrada")
        refpreg = input("Deseas crear una s/n?").lower().strip()
        if refpreg != "s":
            print("No se creó la referencia.")
            return None

    # Obtiene la clave una sola vez, después de confirmar la operación.
    clave = k_creator()
    if clave is None:
        print("Se cancelo la creacion de la clave, no se puede proseguir")
        return

    # Lee el documento protegido y maneja por separado los errores de lectura.
    try:
        with open(Pr_Fi, "rb") as co:
            content = co.read()
    except OSError:
        print("No se pudo leer el documento")
        return

    # Calcula el HMAC y prepara los metadatos de la referencia.
    hmac_cal = calcular_hmac(clave, content)
    data_ref = {
        "nombre del archivo": Pr_Fi.name,
        "algoritmo": "HMAC-SHA-256",
        "hmac": hmac_cal,
    }

    # Guarda la referencia y maneja por separado los errores de escritura.
    try:
        with open(reference, "w", encoding="utf-8") as ref:
            json.dump(data_ref, ref, indent=4)
    except OSError:
        print("No se pudo guardar la referencia")
        return

    return reference

def calcular_hmac(clave, content):
    # Calcula y devuelve el HMAC-SHA-256 del contenido usando la clave recibida.
    return hmac.new(clave, content, hashlib.sha256).hexdigest()

def inicializar():   
    # Delega la creación o actualización de la referencia a r_creator.
    r_creator()
    
    
    
            
def verificar():
    # La verificación requiere el documento, la clave y la referencia ya existentes.
    if not Pr_Fi.exists():
        print("falta el documento, crea uno o define bien la ruta")
        return
    if not SKey.exists():
        print("falta la clave")
        return
    if not reference.exists():
        print("falta la referencia")
        return
        
    # Abre y carga los metadatos de referencia desde el archivo JSON.
    try:
        clave = SKey.read_bytes()
    except OSError:
        print("No se pudo leer la clave")
        return
    try:
        with open(reference, "r", encoding="utf-8") as ref:
            data_ref = json.load(ref)
    except OSError:
        print("No se pudo leer el archivo de referencia")
        return
    except UnicodeDecodeError:
        print("la codificacion de la referencia es invalida")
        return
    except json.JSONDecodeError:
        # Este caso cubre JSON mal formado; otros errores de archivo aún requieren manejo.
        print("referencia invalida")
        return

    if not isinstance(data_ref, dict):
        print("La informacion en referencia no esta en el formato correcto")
        return
   

    # Comprueba que el campo del HMAC esté presente antes de acceder a él.
    if "hmac" not in data_ref:
            print("la referencia no tiene el hmac de referencia, no se puede proseguir")
            return
    # Comprueba que la referencia incluya el nombre del archivo.
    if "nombre del archivo" not in data_ref:
        print("la referencia no contiene el nombre del archivo o esta en un formato distinto, no se puede proseguir")
        return
    if "algoritmo" not in data_ref:
        print("Algoritmo faltante")
        return
    if not isinstance(data_ref["algoritmo"], str):
        print("El algoritmo no esta en el tipo de dato correcto")
        return
    if data_ref["algoritmo"] != "HMAC-SHA-256":
        print("EL algoritmo no es el correspondiente")
        return
    if not isinstance(data_ref["hmac"], str):
        print("La referencia hmac no esta en el tipo de dato correcto")
        return
    if not isinstance(data_ref["nombre del archivo"], str):
        print("El nombre del archivo no esta en el tipo de dato correcto")
        return
    if data_ref["nombre del archivo"] != Pr_Fi.name:
        print("EL nombre del archivo guardado en la referencia no es el mismo al archivo que se esta verificando")
        return
    # Extrae el HMAC guardado y vuelve a calcularlo con el contenido actual.
    hmac_guardado = data_ref["hmac"]
    if not len(hmac_guardado) == 64:
            print("el hmac guardado no tiene la cantidad de caracteres necesarios")
            return
    if not all(caracter in "0123456789abcdefABCDEF" for caracter in hmac_guardado ):
            print("El HMAC guardado contiene caracteres invalidos")
            return
    if len(clave) != 32:
        print("la cantidad de bytes en la clave es incorrecta")
        return
    try:
        content = Pr_Fi.read_bytes()
    except OSError:
        print("No se logro leer el archivo")
        return
    hmac_actual = calcular_hmac(clave, content)
    
    
    # Compara ambos valores para decidir si el contenido coincide con la referencia.
    if hmac.compare_digest(hmac_actual, hmac_guardado):
            print("EL archivo no tiene cambios")
    else:
            print("el archivo ha cambiado")

def menu():
    # Mantiene el menú activo hasta que se elige salir.
    while True:
        print("ELIGE UNA OPCION DEL 1 AL 3")
        print("1. Inicializar o actualizar la referencia")
        print("2. Verificar el archivo")
        print("3. Salir")

        opcion = input("Elija: ").strip()

        if opcion == "1":
            
            print("Inicializando....")
            inicializar()
        elif opcion == "2":
            # Ejecuta la comprobación del documento protegido.
            print("Verificando...")
            verificar()
        elif opcion == "3":
            # Termina el programa cuando se elige la opción de salida.
            print("Saliendo....")
            raise SystemExit
        else:
            # Informa si la opción ingresada no corresponde al menú.
            print("seleccione una opcion valida")


# Evita mostrar el menú si este archivo se importa desde otro módulo.
if __name__ == "__main__":
    menu()