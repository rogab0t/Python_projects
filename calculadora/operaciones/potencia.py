print("...............................")
print(".    >>>función potencia<<<   .")
print("...............................")

num1 = float(input("Ingresa el número a elevar: "))
num2 = float(input("Ingresa la potencia a la que se elevará: "))
print("...............................")

def potencia(a, b):
    resultado = pow(a, b)
    return resultado

print("El resultado es:", potencia(num1, num2))
print("...............................")
