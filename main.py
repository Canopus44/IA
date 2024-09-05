import tkinter as tk
from tkinter import messagebox

class Espacio:
    def __init__(self, id, tipo):
        self.id = id
        self.tipo = tipo
        self.ocupado = False

class Vehiculo:
    def __init__(self, matricula, tipo):
        self.matricula = matricula
        self.tipo = tipo

class Parqueadero:
    def __init__(self):
        self.espacios = []
        self.vehiculos = {}

    def agregar_espacio(self, espacio):
        self.espacios.append(espacio)

    def ingresar_vehiculo(self, vehiculo):
        if self.espacios_libres() > 0:
            for espacio in self.espacios:
                if not espacio.ocupado and (espacio.tipo == vehiculo.tipo or espacio.tipo == 'general'):
                    espacio.ocupado = True
                    self.vehiculos[vehiculo.matricula] = espacio.id
                    return f"Vehículo {vehiculo.matricula} ingresado en espacio {espacio.id}"
            return "No hay espacios disponibles para este tipo de vehículo"
        else:
            return "El parqueadero está lleno"

    def espacios_libres(self):
        return sum(1 for espacio in self.espacios if not espacio.ocupado)

    def salir_vehiculo(self, matricula):
        if matricula in self.vehiculos:
            espacio_id = self.vehiculos.pop(matricula)
            for espacio in self.espacios:
                if espacio.id == espacio_id:
                    espacio.ocupado = False
                    return f"Vehículo {matricula} ha salido del espacio {espacio_id}"
        else:
            return "El vehículo no está en el parqueadero"

class Interfaz:
    def __init__(self, master):
        self.master = master
        master.title("Control de Parqueadero")

        self.parqueadero = Parqueadero()
        self.parqueadero.agregar_espacio(Espacio(1, 'general'))
        self.parqueadero.agregar_espacio(Espacio(2, 'camión'))

        self.label_matricula = tk.Label(master, text="Matrícula:")
        self.label_matricula.pack()
        self.entry_matricula = tk.Entry(master)
        self.entry_matricula.pack()

        self.label_tipo = tk.Label(master, text="Tipo (general/camión):")
        self.label_tipo.pack()
        self.entry_tipo = tk.Entry(master)
        self.entry_tipo.pack()

        self.button_ingresar = tk.Button(master, text="Ingresar Vehículo", command=self.ingresar_vehiculo)
        self.button_ingresar.pack()

        self.button_salir = tk.Button(master, text="Salir Vehículo", command=self.salir_vehiculo)
        self.button_salir.pack()

    def ingresar_vehiculo(self):
        matricula = self.entry_matricula.get()
        tipo = self.entry_tipo.get()
        vehiculo = Vehiculo(matricula, tipo)
        mensaje = self.parqueadero.ingresar_vehiculo(vehiculo)
        messagebox.showinfo("Ingreso Vehículo", mensaje)

    def salir_vehiculo(self):
        matricula = self.entry_matricula.get()
        mensaje = self.parqueadero.salir_vehiculo(matricula)
        messagebox.showinfo("Salida Vehículo", mensaje)

root = tk.Tk()
interfaz = Interfaz(root)
root.mainloop()
