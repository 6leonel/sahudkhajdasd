def generarEscenario() -> list:
    return [i for i in range(1, 101)]

def generarRegistroVentas() -> None:
    global ventas
    ventas = [[0 for _ in range(3)] for _ in range(2)]

def borrarPantalla() -> None:
    so = __import__("os")
    so.system("cls" if OSError.name == "nt" else "clear")

def mostrarEscenario(escenario: list) -> None:
    for i, asiento in enumerate(escenario, start=1):
        print(str(asiento).center(3), end=" ")
        if i % 10 == 0:
            print()

def validarRut(rut: str) -> bool:
    return rut.isnumeric() and len(rut) == 8

def comprarEntradas(escenario: list, registro: dict) -> None:
    borrarPantalla()
    try:
        cant_entradas = int(input("> Indique cuántas entradas va a comprar: "))
        assert 0 < cant_entradas <= 3 
    except (AssertionError, ValueError):
        print("[!] Solo puede comprar entre 1 a 3 entradas o se ha ingresado un valor no numérico.")
        return
    
    rut = ""
    while not validarRut(rut):
        rut = input("> Ingrese su RUT sin puntos ni dígito verificador: ")
        if len(rut) == 7:
            rut = "0" + rut
        if not validarRut(rut):
            print("[!] El rut ingresado no es válido")

    if rut not in registro:
        ubicaciones = []
        for _ in range(cant_entradas):
            while len(ubicaciones) < cant_entradas:
                borrarPantalla()
                mostrarEscenario(escenario)
                print(f"\n- RUT REGISTRADO: {rut}")
                print("\n[Valores para entradas]")
                print("""\r* Platinum: $120.000 (Asientos del 1 al 20)
                        \r* Gold: $80.000 (Asientos del 21 al 50)
                        \r* Silver: $50.000 (Asientos del 51 al 100)""")
                try:
                    ubicacion = int(input("> Seleccione su ubicación: "))
                except ValueError:
                    print("[!] Se ha ingresado un valor no numérico")
                else:
                    if ubicacion in escenario:
                        escenario[escenario.index(ubicacion)] = "X"
                        ubicaciones.append(ubicacion)
                        registroPrecioAPagar(ubicacion)
                    else:
                        if 0 < ubicacion <= len(escenario):
                            print("\n[!] La ubicación seleccionada ya fue vendida.")
                            input("[Pulse enter para reintentar]")
                        else:
                            print("\n[!] La ubicación seleccionada no existe.")
                            input("[Pulse enter para reintentar]")
        registro[rut] = tuple(ubicaciones)
        borrarPantalla()
        print("\n¡Compra finalizada exitosamente!")
    else:
        print("[!] Este RUT ya se encuentra registrado y ya realizó compras.")

def verListaAsistentes(registro: dict) -> None:
    borrarPantalla()
    if registro:
        print("Rut Asistente \t Ubicaciones")
        for rut, ubicaciones in sorted(registro.items()):
            print(f"{rut} \t {ubicaciones}")
        input("[Pulse enter para volver al menú]")
        borrarPantalla()
    else:
        print("No hay ningún asistente hasta el momento.")
        input("[Pulse enter para volver al menú]")

def registroPrecioAPagar(entrada: int) -> None:
    if 0 < entrada <= 20:
        ventas[0][0] += 1
        ventas[1][0] += 120_000
    elif 20 < entrada <= 50:
        ventas[0][1] += 1
        ventas[1][1] += 80_000
    elif 50 < entrada <= 100:
        ventas[0][2] += 1
        ventas[1][2] += 50_000

def mostrarGanancias() -> None:
    borrarPantalla()
    tipo_entradas = ["Platinum ($120.000)", "Gold ($80.000)", "Silver ($50.000)"]
    print("Tipo Entrada".center(20), "\t", "Cantidad".center(10), "\t", "Total".center(10))
    for i in range(3):
        print(f"{tipo_entradas[i].center(20)} \t {str(ventas[0][i]).center(10)} \t {str(ventas[1][i]).center(10)}")
    print("TOTAL".center(20), "\t", str(sum(ventas[0])).center(10), "\t", str(sum(ventas[1])).center(10))
    input("[Pulse enter para volver al menú]")
    borrarPantalla()

if __name__ == "__main__":
    escenario = generarEscenario()
    generarRegistroVentas()
    asistentes = {}

    while True:
        print("[Opciones]")
        print("""
            1. Comprar entradas
            2. Mostrar ubicaciones disponibles
            3. Ver listado de asistentes
            4. Mostrar ganancias totales
            5. Salir""")
        try:
            opcion = int(input("> Seleccione una opcion: "))
        except ValueError:
            print("[!] Se ha ingresado un valor no numérico")
            continue

        if opcion == 1:
            comprarEntradas(escenario, asistentes)
        elif opcion == 2:
            borrarPantalla()
            mostrarEscenario(escenario)
            input("[Pulse enter para volver al menú]")
            borrarPantalla()
        elif opcion == 3:
            verListaAsistentes(asistentes)
        elif opcion == 4:
            mostrarGanancias()
        elif opcion == 5:
            print("\n[CERRADO]")
            break
        else:
            print("[!] La opción seleccionada es inválida")
