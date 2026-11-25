from plato import Plato
from bebidas import Bebida
from combo import Combo
from cliente import Cliente
from restaurante import Restaurante
from local import Local
from para_llevar import ParaLlevar
from delivery import Delivery
from pago_efectivo import PagoEfectivo
from pago_tarjeta import PagoTarjeta
from pago_qr import PagoQR

DIAS = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]


def leer_texto(mensaje):
    while True:
        texto = input(mensaje).strip()
        if texto != "":
            return texto
        print("El dato no puede estar vacío.")


def leer_entero(mensaje):
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("Debe ingresar un número entero.")


def leer_decimal(mensaje):
    while True:
        try:
            valor = float(input(mensaje))
            if valor < 0:
                print("El valor no puede ser negativo.")
            else:
                return valor
        except ValueError:
            print("Debe ingresar un número válido.")


def normalizar_dia(texto):
    texto = texto.strip().lower()
    texto = texto.replace("á", "a").replace("é", "e").replace("í", "i")
    texto = texto.replace("ó", "o").replace("ú", "u")
    return texto


def leer_dia(mensaje):
    while True:
        dia = normalizar_dia(input(mensaje))
        if dia in DIAS:
            return dia
        print("Día no válido. Opciones: " + ", ".join(DIAS))


def elegir_de_lista(lista, mensaje):
    opcion = leer_entero(mensaje)
    if opcion >= 1 and opcion <= len(lista):
        return lista[opcion - 1]
    print("Opción no válida.")
    return None


def productos_disponibles(restaurante, dia):
    disponibles = []
    for producto in restaurante.productos:
        if producto.esta_disponible(dia):
            disponibles.append(producto)
    return disponibles


def mostrar_lista_productos(productos):
    for i in range(len(productos)):
        print(f"  {i + 1}. [{productos[i].tipo()}] {productos[i]}")



def cargar_datos_iniciales(restaurante):
    silpancho = Plato("Silpancho", 35, ["lunes", "miercoles", "viernes", "sabado"])
    pique = Plato("Pique macho", 45, ["viernes", "sabado", "domingo"])
    sopa = Plato("Sopa de maní", 20, list(DIAS))
    refresco = Bebida("Refresco de mocochinchi", 8, "vaso")
    chicharron = Plato("Chicharrón", 40, ["domingo"])
    gaseosa = Bebida("Gaseosa", 15, "vaso")
    jarra = Bebida("Jarra de mocochinchi", 8, "jarra")
    restaurante.registrar_producto(silpancho)
    restaurante.registrar_producto(pique)
    restaurante.registrar_producto(sopa)
    restaurante.registrar_producto(refresco)
    restaurante.registrar_producto(chicharron)
    restaurante.registrar_producto(gaseosa)
    restaurante.registrar_producto(jarra)
    combo_familiar = Combo("Combo Familiar")
    combo_familiar.agregar_producto(silpancho)
    combo_familiar.agregar_producto(sopa)
    combo_familiar.agregar_producto(refresco)
    restaurante.registrar_producto(combo_familiar)
    combo_pique = Combo("Combo Pique")
    combo_pique.agregar_producto(pique)
    combo_pique.agregar_producto(gaseosa)
    restaurante.registrar_producto(combo_pique)
    restaurante.registrar_cliente(Cliente("Ana Rojas", "71234567"))
    restaurante.registrar_cliente(Cliente("Luis Mamani", "68765432"))


def registrar_plato(restaurante):
    nombre = leer_texto("Nombre del plato: ")
    if restaurante.buscar_producto(nombre) is not None:
        print("Ya existe un producto con ese nombre.")
        return
    precio = leer_decimal("Precio (Bs): ")
    print("Días: " + ", ".join(DIAS))
    texto = leer_texto("Días disponibles separados por coma (o 'todos'): ")
    if normalizar_dia(texto) == "todos":
        dias = list(DIAS)
    else:
        dias = []
        for parte in texto.split(","):
            dia = normalizar_dia(parte)
            if dia not in DIAS:
                print(f"'{parte.strip()}' no es un día válido y se ignoró.")
            elif dia not in dias:
                dias.append(dia)
    if len(dias) == 0:
        print("Debe indicar al menos un día válido. No se registró el plato.")
        return
    try:
        restaurante.registrar_producto(Plato(nombre, precio, dias))
        print(f"Plato '{nombre}' registrado.")
    except ValueError as error:
        print(f"Error: {error}")


def registrar_bebida(restaurante):
    nombre = leer_texto("Nombre de la bebida: ")
    if restaurante.buscar_producto(nombre) is not None:
        print("Ya existe un producto con ese nombre.")
        return
    precio = leer_decimal("Precio por vaso (Bs): ")
    print("  1. Vaso")
    print("  2. Jarra (cuesta 3 veces el vaso)")
    opcion = leer_entero("Opción: ")
    tipo_bebida = "vaso"
    if opcion == 2:
        tipo_bebida = "jarra"
    try:
        bebida = Bebida(nombre, precio, tipo_bebida)
        restaurante.registrar_producto(bebida)
        print(f"Bebida '{nombre}' registrada: Bs {bebida.calcular_precio():.2f}")
    except ValueError as error:
        print(f"Error: {error}")


def armar_combo(restaurante):
    if len(restaurante.productos) < 2:
        print("Se necesitan al menos 2 productos registrados para armar un combo.")
        return
    nombre = leer_texto("Nombre del combo: ")
    if restaurante.buscar_producto(nombre) is not None:
        print("Ya existe un producto con ese nombre.")
        return
    combo = Combo(nombre)
    productos = list(restaurante.productos)
    cantidad = 0
    print("El combo tiene 15% de descuento solo si tiene 3 productos o más.")
    print("Productos registrados (también puede agregar otros combos):")
    mostrar_lista_productos(productos)
    while True:
        opcion = leer_entero("Número del producto a agregar (0 para terminar): ")
        if opcion == 0:
            break
        if opcion >= 1 and opcion <= len(productos):
            combo.agregar_producto(productos[opcion - 1])
            cantidad += 1
            print(f"Agregado: {productos[opcion - 1].nombre}")
        else:
            print("Opción no válida.")
    if cantidad < 2:
        print("Un combo debe tener al menos 2 productos. No se registró el combo.")
        return
    restaurante.registrar_producto(combo)
    if combo.aplica_descuento():
        print(f"Combo '{nombre}' registrado con 15% de descuento: Bs {combo.calcular_precio():.2f}")
    else:
        print(f"Combo '{nombre}' registrado sin descuento: Bs {combo.calcular_precio():.2f}")


def listar_menu_dia(restaurante):
    dia = leer_dia("Día a consultar: ")
    disponibles = productos_disponibles(restaurante, dia)
    print(f"\n--- Menú disponible el {dia} ---")
    if len(disponibles) == 0:
        print("No hay productos disponibles ese día.")
    else:
        mostrar_lista_productos(disponibles)


def menu_productos(restaurante):
    while True:
        print("\n--- PRODUCTOS Y COMBOS ---")
        print("1. Registrar plato")
        print("2. Registrar bebida")
        print("3. Armar combo")
        print("4. Listar menú disponible por día")
        print("0. Volver")
        opcion = leer_entero("Opción: ")
        if opcion == 1:
            registrar_plato(restaurante)
        elif opcion == 2:
            registrar_bebida(restaurante)
        elif opcion == 3:
            armar_combo(restaurante)
        elif opcion == 4:
            listar_menu_dia(restaurante)
        elif opcion == 0:
            return
        else:
            print("Opción no válida.")


def registrar_cliente(restaurante):
    print("\n--- REGISTRAR CLIENTE ---")
    nombre = leer_texto("Nombre del cliente: ")
    telefono = leer_texto("Teléfono (8 dígitos, empieza en 6 o 7): ")
    try:
        restaurante.registrar_cliente(Cliente(nombre, telefono))
        print(f"Cliente '{nombre}' registrado.")
    except ValueError as error:
        print(f"Error: {error}")


def elegir_cliente(restaurante):
    clientes = restaurante.clientes
    if len(clientes) == 0:
        print("No hay clientes registrados. Use la opción 2 primero.")
        return None
    print("Clientes:")
    for i in range(len(clientes)):
        print(f"  {i + 1}. {clientes[i].nombre}")
    return elegir_de_lista(clientes, "Elija el cliente: ")


def elegir_pedido(restaurante):
    if len(restaurante.pedidos) == 0:
        print("No hay pedidos registrados.")
        return None
    print("Pedidos:")
    for pedido in restaurante.pedidos:
        pago = "sin pagar"
        if pedido.esta_pagado():
            pago = "pagado"
        print(f"  #{pedido.numero} - {pedido.tipo()} - {pedido.cliente.nombre} - {pedido.estado} - {pago}")
    numero = leer_entero("Número de pedido: ")
    pedido = restaurante.buscar_pedido(numero)
    if pedido is None:
        print("No existe un pedido con ese número.")
    return pedido


def mostrar_productos_pedido(pedido):
    if len(pedido.productos_pedidos) == 0:
        print("  (sin productos)")
    for detalle in pedido.productos_pedidos:
        print(f"  - {detalle}")


def agregar_al_pedido(pedido, restaurante, dia_actual):
    disponibles = productos_disponibles(restaurante, dia_actual)
    if len(disponibles) == 0:
        print("No hay productos disponibles hoy.")
        return
    print(f"Menú de hoy ({dia_actual}):")
    mostrar_lista_productos(disponibles)
    producto = elegir_de_lista(disponibles, "Número del producto: ")
    if producto is not None:
        try:
            pedido.agregar_producto(producto)
            print(f"Agregado: {producto.nombre}")
        except ValueError as error:
            print(f"Error: {error}")


def quitar_del_pedido(pedido):
    detalles = pedido.productos_pedidos
    if len(detalles) == 0:
        print("El pedido no tiene productos.")
        return
    for i in range(len(detalles)):
        print(f"  {i + 1}. {detalles[i]}")
    detalle = elegir_de_lista(detalles, "Número del producto a quitar: ")
    if detalle is not None:
        pedido.quitar_producto(detalle.producto)
        print(f"Quitado: {detalle.producto.nombre}")


def modificar_productos(pedido, restaurante, dia_actual):
    while True:
        if not pedido.puede_modificarse():
            print("Solo se modifican productos de un pedido REGISTRADO y sin pagar.")
            return
        print(f"\n--- Productos del pedido #{pedido.numero} ---")
        mostrar_productos_pedido(pedido)
        print("1. Agregar producto")
        print("2. Quitar producto")
        print("0. Terminar")
        opcion = leer_entero("Opción: ")
        if opcion == 1:
            agregar_al_pedido(pedido, restaurante, dia_actual)
        elif opcion == 2:
            quitar_del_pedido(pedido)
        elif opcion == 0:
            return
        else:
            print("Opción no válida.")


def crear_pedido(restaurante, dia_actual):
    cliente = elegir_cliente(restaurante)
    if cliente is None:
        return
    print("Tipo de pedido:")
    print("  1. Local (mesa 1 a 15, 5% de descuento desde 6 platos)")
    print("  2. Para llevar (Bs 2 de envase por plato)")
    print("  3. Delivery (envío por zona, pedido mínimo Bs 60, solo efectivo o QR)")
    opcion = leer_entero("Opción: ")
    numero = len(restaurante.pedidos) + 1
    try:
        if opcion == 1:
            mesa = leer_entero("Número de mesa (1 a 15): ")
            pedido = Local(numero, cliente, mesa)
        elif opcion == 2:
            pedido = ParaLlevar(numero, cliente)
        elif opcion == 3:
            zonas = ["Cercado", "Quillacollo", "Sacaba", "Vinto"]
            print("Zonas: 1. Cercado (Bs 8)  2. Quillacollo (Bs 15)  3. Sacaba (Bs 15)  4. Vinto (Bs 20)")
            zona = elegir_de_lista(zonas, "Zona: ")
            if zona is None:
                return
            pedido = Delivery(numero, cliente, zona)
        else:
            print("Tipo de pedido no válido.")
            return
        restaurante.registrar_pedido(pedido)
    except ValueError as error:
        print(f"Error: {error}")
        return
    print(f"Pedido #{numero} ({pedido.tipo()}) creado en estado '{pedido.estado}'.")
    modificar_productos(pedido, restaurante, dia_actual)


def menu_pedidos(restaurante, dia_actual):
    while True:
        print("\n--- PEDIDOS ---")
        print("1. Crear nuevo pedido")
        print("2. Agregar o quitar productos de un pedido")
        print("0. Volver")
        opcion = leer_entero("Opción: ")
        if opcion == 1:
            crear_pedido(restaurante, dia_actual)
        elif opcion == 2:
            pedido = elegir_pedido(restaurante)
            if pedido is not None:
                modificar_productos(pedido, restaurante, dia_actual)
        elif opcion == 0:
            return
        else:
            print("Opción no válida.")


def mostrar_detalle(restaurante):
    pedido = elegir_pedido(restaurante)
    if pedido is None:
        return
    print("\n========== DETALLE DEL PEDIDO ==========")
    print(pedido.resumen())
    print("========================================")


def cambiar_estado(restaurante):
    pedido = elegir_pedido(restaurante)
    if pedido is None:
        return
    print(f"Estado actual: {pedido.estado}")
    siguientes = pedido.estados_siguientes()
    if len(siguientes) == 0:
        print("Este pedido ya no puede cambiar de estado.")
        return
    print("Estados a los que puede pasar:")
    for i in range(len(siguientes)):
        print(f"  {i + 1}. {siguientes[i]}")
    nuevo_estado = elegir_de_lista(siguientes, "Nuevo estado: ")
    if nuevo_estado is None:
        return
    if nuevo_estado == "CANCELADO":
        confirmacion = input("¿Seguro que desea cancelar el pedido? (s/n): ").strip().lower()
        if confirmacion != "s":
            print("No se canceló el pedido.")
            return
    try:
        pedido.cambiar_estado(nuevo_estado)
        print(f"El pedido #{pedido.numero} ahora está en estado {pedido.estado}.")
    except ValueError as error:
        print(f"Error: {error}")


def elegir_metodo_pago():
    print("Método de pago:")
    print("  1. Efectivo")
    print("  2. Tarjeta (3% de comisión, no válida para delivery)")
    print("  3. QR")
    opcion = leer_entero("Opción: ")
    if opcion == 1:
        monto = leer_decimal("Monto recibido (Bs): ")
        return PagoEfectivo(monto)
    if opcion == 2:
        return PagoTarjeta()
    if opcion == 3:
        codigo = leer_texto("Código de transacción QR (10 dígitos): ")
        return PagoQR(codigo)
    print("Método de pago no válido.")
    return None


def mostrar_comprobante(restaurante, pedido, metodo, resultado):
    print("\n========== COMPROBANTE DE PAGO ==========")
    print(f"Restaurante: {restaurante.nombre}")
    print(pedido.resumen())
    print(f"Método de pago: {metodo.nombre()}")
    for linea in metodo.lineas_comprobante(pedido.costo, resultado):
        print(linea)
    print("=========================================")


def cobrar_pedido(restaurante):
    pedido = elegir_pedido(restaurante)
    if pedido is None:
        return
    try:
        pedido.validar_pago()
    except ValueError as error:
        print(f"No se puede cobrar: {error}")
        return
    print(f"Total a pagar: Bs {pedido.calcular_total():.2f}")
    metodo = elegir_metodo_pago()
    if metodo is None:
        return
    try:
        resultado = pedido.pagar(metodo)
    except ValueError as error:
        print(f"No se pudo cobrar: {error}")
        return
    mostrar_comprobante(restaurante, pedido, metodo, resultado)


def mostrar_reporte(restaurante, dia_actual):
    cantidad_por_tipo = {}
    total_por_tipo = {}
    ventas_por_producto = {}
    cancelados = 0
    for pedido in restaurante.pedidos:
        if pedido.estado == "CANCELADO":
            cancelados += 1
        if pedido.esta_pagado():
            tipo = pedido.tipo()
            if tipo not in cantidad_por_tipo:
                cantidad_por_tipo[tipo] = 0
                total_por_tipo[tipo] = 0.0
            cantidad_por_tipo[tipo] += 1
            total_por_tipo[tipo] += pedido.calcular_total()
            for detalle in pedido.productos_pedidos:
                nombre = detalle.producto.nombre
                if nombre in ventas_por_producto:
                    ventas_por_producto[nombre] += detalle.cantidad
                else:
                    ventas_por_producto[nombre] = detalle.cantidad
    print(f"\n========== REPORTE DE VENTAS ({dia_actual}) ==========")
    total_general = 0.0
    if len(cantidad_por_tipo) == 0:
        print("Aún no hay pedidos pagados.")
    for tipo in cantidad_por_tipo:
        print(f"{tipo}: {cantidad_por_tipo[tipo]} pedido(s) - Bs {total_por_tipo[tipo]:.2f}")
        total_general += total_por_tipo[tipo]
    print(f"TOTAL VENDIDO: Bs {total_general:.2f}")
    print(f"Pedidos cancelados: {cancelados}")
    print("\nTop 3 productos más vendidos:")
    ranking = []
    for nombre in ventas_por_producto:
        ranking.append([ventas_por_producto[nombre], nombre])
    ranking.sort(reverse=True)
    if len(ranking) == 0:
        print("  Aún no hay ventas.")
    for i in range(min(3, len(ranking))):
        print(f"  {i + 1}. {ranking[i][1]} - {ranking[i][0]} unidad(es)")
    print("=================================================")


def mostrar_menu_principal(restaurante, dia_actual):
    print(f"\n===== {restaurante.nombre.upper()} - Hoy es {dia_actual} =====")
    print("1. Productos y combos / menú del día")
    print("2. Registrar cliente")
    print("3. Registrar pedido / agregar o quitar productos")
    print("4. Mostrar detalle de un pedido")
    print("5. Cambiar estado de un pedido")
    print("6. Cobrar pedido")
    print("7. Reporte de ventas del día")
    print("0. Salir")


def main():
    restaurante = Restaurante("Sabor Valluno")
    cargar_datos_iniciales(restaurante)
    print(f"Bienvenido al sistema de {restaurante.nombre}")
    dia_actual = leer_dia("¿Qué día de la semana es hoy?: ")
    while True:
        mostrar_menu_principal(restaurante, dia_actual)
        opcion = leer_entero("Elija una opción: ")
        if opcion == 1:
            menu_productos(restaurante)
        elif opcion == 2:
            registrar_cliente(restaurante)
        elif opcion == 3:
            menu_pedidos(restaurante, dia_actual)
        elif opcion == 4:
            mostrar_detalle(restaurante)
        elif opcion == 5:
            cambiar_estado(restaurante)
        elif opcion == 6:
            cobrar_pedido(restaurante)
        elif opcion == 7:
            mostrar_reporte(restaurante, dia_actual)
        elif opcion == 0:
            print("¡Hasta pronto!")
            break
        else:
            print("Opción no válida.")


if __name__ == "__main__":
    main()