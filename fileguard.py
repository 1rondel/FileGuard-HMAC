import hmac
import hashlib
import secrets
import json
import pathlib


# File to be protected by HMAC verification
Pr_Fi = pathlib.Path("documento.txt")

SKey = pathlib.Path("clave.key")

reference = pathlib.Path("referencia.json")


def k_creator():
    #Load the HMAC key, creating and saving one if it does not exist
    if SKey.exists():
        clave = SKey.read_bytes()
        return clave
    else:
        print('la clave no existe')
        keypreg = input("desea crear una s/n").strip().lower()
        if keypreg == "s":
            clave = secrets.token_bytes(32)
            SKey.write_bytes(clave)
            clave = SKey.read_bytes()
            return clave
        else:
            return None

def r_creator ():
    if reference.exists():
        return reference

    else:
        if Pr_Fi.exists():
            if SKey.exists():
                clave = k_creator()
                print('la referencia no fue encontrada ')
                refpreg = input('deseas crear una s/n').lower().strip()
                hmac_cal = None
                if refpreg == "s":
                    with open(Pr_Fi, "rb") as co:
                        content = co.read()
                        hmac_cal = calcular_hmac(clave, content)
                    data_ref = {
                    "nombre del archivo":Pr_Fi.name,
                    "algoritmo":"HMAC-SHA-256",
                    "hmac":hmac_cal}
                    with open(reference, "w", encoding="utf-8") as ref:
                        json.dump(data_ref, ref, indent=4)
                        return reference
                else:
                    print("No se creó la referencia.")
                    return None
            else:
                print("La key no existe")
                k_creator()
                if k_creator() == None:
                    print("key faltante no se puede crear la referencia")
        else:
            print("Documento faltante, no se pudo crear la referencia")


def calcular_hmac(clave, content):
    return hmac.new(clave, content, hashlib.sha256).hexdigest()

def inicializar():
    
    
    
    if not Pr_Fi.exists():
        print("Archivo no encontrado o inexistente")
        return
    
    r_creator()
    
    
    
            
def verificar():
    
    if not Pr_Fi.exists():
        print("falta el documento, crea uno o define bien la ruta")
        return
    if not SKey.exists():
        print("falta la llave")
        k_creator()
        if k_creator() == None:
            return
    if not reference.exists():
        r_creator()
        if r_creator() == None:
            return
        
        
    clave = k_creator()
    if clave is None:
        print("se cancelo")

    try:
        with open(reference, "r", encoding="utf-8") as ref:
            data_ref = json.load(ref)
    except json.JSONDecodeError:
        print("referencia invalida")
        return
    if "hmac" not in data_ref:
        print("la referencia no tiene el hmac de referenci, no se puede proseguir")
        return
    if "nombre del archivo" not in data_ref:
        print("la referencia no contiene el nombre del archivo, no se puede proseguir")
        return
    
    hmac_guardado = data_ref["hmac"]
    content = Pr_Fi.read_bytes()
    hmac_actual = calcular_hmac(clave, content)
    
    
    if hmac.compare_digest(hmac_actual, hmac_guardado):
        print("EL archivo no tiene cambios")
    else:
        print("el archivo ha cambiado")

def menu():
    while True:
        print("ELIGE UNA OPCION DEL 1 AL 3")
        print("1. Inicializar o actualizar la referencia")
        print("2. Verificar el archivo")
        print("3. Salir")

        opcion = input("Elija: ").strip()

        if opcion == "1":
            confirmacion = input("desea inicializar s/n? ").strip().lower()
            if confirmacion == "s":
                print("Inicializando....")
                inicializar()
        elif opcion == "2":
            print("Verificando...")
            verificar()
        elif opcion == "3":
            print("Saliendo....")
            raise SystemExit
        else:
            print("seleccione una opcion valida")


if __name__ == "__main__":
    menu()
        