print("...............................")
print(".Escribe 1 para suma          .")
print(".Escribe 2 para resta         .")
print(".Escribe 3 para multiplicación.")
print(".Escribe 4 para división      .")
print(".Escribe 5 para potencia      .")
print("...............................")
from operaciones import *
def calcular():
    operacion = int(input("Ingresa que operación quieres iniciar: "))
    print("...............................")
    
    if operacion == 1:
        camb = input("!Elegiste SUMA, quieres cambiar? si/no: ")
        print("...............................")
        if camb == "si":
            calcular()
        elif camb == "no":
            import operaciones.suma
        else:
            print("!No ingresaste una respuesta¡")
            print("...............................")
            calcular()
    elif operacion == 2:
        camb = input("!Elegiste RESTA, quieres cambiar? si/no: ")
        print("...............................")
        if camb == "si":
            calcular()
        elif camb == "no":
            import operaciones.resta
        else:
            print("!No ingresaste una respuesta¡")
            print("...............................")
            calcular()
    elif operacion == 3:
        camb = input("!Elegiste MULTIPLICACIÓN, quieres cambiar? si/no: ")
        print("...............................")
        if camb == "si":
            calcular()
        elif camb == "no":
            import operaciones.multiplicacion
        else:
            print("!No ingresaste una respuesta¡")
            print("...............................")
            calcular()
    elif operacion == 4:
        camb = input("!Elegiste DIVISION, quieres cambiar? si/no: ")
        print("...............................")
        if camb == "si":
            calcular()
        elif camb == "no":
            import operaciones.division
        else:
            print("!No ingresaste una respuesta¡")
            print("...............................")
            calcular()
    elif operacion == 5:
        camb = input("!Elegiste POTENCIA, quieres cambiar? si/no: ")
        print("...............................")
        if camb == "si":
            calcular()
        elif camb == "no":
            import operaciones.potencia
        else:
            print("!No ingresaste una respuesta¡")
            print("...............................")
            calcular()
    else:
        print("!No ingresaste ninguna operación¡")
        print("...............................")
        calcular()

calcular()
