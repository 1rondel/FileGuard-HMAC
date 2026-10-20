import hmac, hashlib, secrets, json, pathlib, os


#protected file
Pr_Fi = pathlib.Path("documento.txt")

SKey = pathlib.Path("clave.key")

reference = pathlib.Path("referencia.json")

def calcular_hmac(Skey, content):
    return  hmac.new(Skey, content, hashlib.sha256).hexdigest()

def inicializar():
    if not Pr_Fi.exists():
        print("Archivo no encontrado o inexistente")
        return
    
    if SKey.exists():
        clave = SKey.read_bytes()
    
    else:
        clave = secrets.token_bytes(32)
        SKey.write_bytes(clave)
        
    content = Pr_Fi.read_bytes()
    hmac_cal = calcular_hmac(clave, content)
    data_ref = {
            "nombre del archivo":Pr_Fi.name,
            "algoritmo":"HMAC-SHA-256",
            "hmac":hmac_cal
        }
    with open(reference, "w", encoding="utf-8") as ref:
            json.dump(data_ref, ref, indent=4)
            
def verificar():
    if not Pr_Fi.exists():
        print("falta el documento")
        return
    if not SKey.exists():
        print("falta la llave")
        return
    if not reference.exists():
        print("falta la referencia")
        return

    clave = SKey.read_bytes()
    
    with open(reference, "r", encoding="utf-8") as ref:
        data_ref = json.load(ref)
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
                inicializar()
        elif opcion == "2":
            verificar()
        elif opcion == "3":
            raise SystemExit
        else:
            print("seleccione una opcion valida")


menu()
