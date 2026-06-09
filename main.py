# main.py

from datos import usuarios, soluciones, tickets


def mostrar_encabezado():                                                                   # Muestra el encabezado inicial del chatbot.
    
    print("=" * 60)
    print("CHATBOT DE SOPORTE TÉCNICO NIVEL 1")
    print("Mesa de ayuda interna - Organización G&H")
    print("=" * 60)


def validar_usuario(legajo):                                                                # Valida si el legajo existe y si el usuario está activo.
    
    usuario = usuarios.get(legajo)

    if usuario is None:
        return None, "no_encontrado"

    if usuario["estado"] != "activo":
        return usuario, "inactivo"

    return usuario, "activo"


def mostrar_menu_problemas():                                                               # Muestra las categorías de problemas disponibles.
    
    print("\nSeleccioná el tipo de problema:")
    print("1. Internet")
    print("2. Login")
    print("3. Impresora")
    print("4. Correo")
    print("5. Software")
    print("6. Hardware")
    print("7. Otro")


def pedir_opcion_menu():                                                                    # Solicita una opción válida del menú.
    
    while True:
        opcion = input("\nIngresá una opción del 1 al 7: ").strip()

        if opcion in soluciones:
            return opcion

        print("Opción inválida. Por favor, ingresá un número del 1 al 7.")


def pedir_confirmacion():                                                                   # Pregunta si la solución resolvió el problema.
    
    while True:
        respuesta = input("\n¿La solución resolvió el problema? (si/no): ").strip().lower()

        if respuesta in ["si", "sí", "s"]:
            return True

        if respuesta in ["no", "n"]:
            return False

        print("Respuesta inválida. Por favor, respondé 'si' o 'no'.")


def pedir_email():                                                                          # Solicita un correo válido para seguimiento.
    
    while True:
        email = input("\nIngresá un correo electrónico para seguimiento: ").strip()

        if "@" in email and "." in email:
            return email

        print("Correo inválido. Por favor, ingresá un correo válido.")


def generar_ticket(legajo, categoria, estado, email_contacto=None):                         # Genera un ticket simulado y lo guarda en la lista de tickets.
    
    ticket = {
        "id_ticket": len(tickets) + 1,
        "legajo": legajo,
        "categoria": categoria,
        "estado": estado,
        "email_contacto": email_contacto
    }

    tickets.append(ticket)
    return ticket


def informar_ticket(ticket):                                                                # Muestra el estado final del ticket.
    
    print("\n" + "-" * 60)
    print(f"Ticket N°: {ticket['id_ticket']}")
    print(f"Categoría: {ticket['categoria']}")
    print(f"Estado final: {ticket['estado']}")

    if ticket["email_contacto"]:
        print(f"Correo de seguimiento: {ticket['email_contacto']}")

    print("-" * 60)


def procesar_problema(legajo, opcion):                                                      # Procesa el problema seleccionado y define si se cierra o deriva.
    
    datos_problema = soluciones[opcion]
    categoria = datos_problema["categoria"]

    print(f"\nCategoría seleccionada: {categoria}")

    if datos_problema["deriva_directo"]:
        print("\nEste caso requiere revisión manual del área de soporte.")
        email = pedir_email()
        ticket = generar_ticket(legajo, categoria, "Derivado a soporte", email)
        informar_ticket(ticket)
        return

    print("\nSolución sugerida:")
    print(datos_problema["solucion"])

    soluciono = pedir_confirmacion()

    if soluciono:
        ticket = generar_ticket(legajo, categoria, "Cerrado correctamente")
        informar_ticket(ticket)
    else:
        print("\nEl caso será derivado a soporte técnico.")
        email = pedir_email()
        ticket = generar_ticket(legajo, categoria, "Derivado a soporte", email)
        informar_ticket(ticket)


def iniciar_chatbot():                                                                      # Ejecuta el flujo principal del chatbot.
    
    mostrar_encabezado()

    print("\nBienvenido al sistema de soporte técnico.")
    legajo = input("Ingresá tu legajo: ").strip()

    usuario, estado = validar_usuario(legajo)

    if estado == "no_encontrado":
        print("\nEl legajo ingresado no corresponde a un usuario registrado.")
        print("No se puede continuar con la solicitud.")
        return

    if estado == "inactivo":
        print(f"\nEl usuario {usuario['nombre']} existe, pero se encuentra inactivo.")
        print("No se puede continuar con la solicitud.")
        return

    print(f"\nUsuario validado correctamente.")
    print(f"Nombre: {usuario['nombre']}")
    print(f"Departamento: {usuario['departamento']}")

    mostrar_menu_problemas()
    opcion = pedir_opcion_menu()
    procesar_problema(legajo, opcion)

    print("\nGracias por utilizar el chatbot de soporte técnico.")


if __name__ == "__main__":
    iniciar_chatbot()