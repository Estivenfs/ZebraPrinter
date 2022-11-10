from zebra import Zebra
def getZebra():
    z = Zebra()
    impresoras = z.getqueues()
    for printer in impresoras:
        print(printer)

getZebra()
key = input("Presione alguna tecla")