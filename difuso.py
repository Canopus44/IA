import tkinter as tk
from tkinter import ttk
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Definir las variables de entrada y salida
ocupacion = ctrl.Antecedent(np.arange(0, 101, 1), 'ocupacion')
hora = ctrl.Antecedent(np.arange(0, 24, 1), 'hora')
accion = ctrl.Consequent(np.arange(0, 11, 1), 'accion')

ocupacion['baja'] = fuzz.trimf(ocupacion.universe, [0, 0, 50])
ocupacion['media'] = fuzz.trimf(ocupacion.universe, [25, 50, 75])
ocupacion['alta'] = fuzz.trimf(ocupacion.universe, [50, 100, 100])

hora['temprano'] = fuzz.trimf(hora.universe, [0, 0, 12])
hora['medio'] = fuzz.trimf(hora.universe, [6, 12, 18])
hora['tarde'] = fuzz.trimf(hora.universe, [12, 24, 24])

accion['rechazar'] = fuzz.trimf(accion.universe, [0, 0, 5])
accion['aceptar'] = fuzz.trimf(accion.universe, [5, 10, 10])

regla1 = ctrl.Rule(ocupacion['alta'] & hora['temprano'], accion['rechazar'])
regla2 = ctrl.Rule(ocupacion['baja'] & hora['tarde'], accion['aceptar'])
regla3 = ctrl.Rule(ocupacion['media'] & hora['medio'], accion['aceptar'])

sistema_ctrl = ctrl.ControlSystem([regla1, regla2, regla3])
sistema = ctrl.ControlSystemSimulation(sistema_ctrl)

# Función para actualizar la acción recomendada
def calcular_accion():
    ocupacion_valor = float(ocupacion_entry.get())
    hora_valor = float(hora_entry.get())

    sistema.input['ocupacion'] = ocupacion_valor
    sistema.input['hora'] = hora_valor
    sistema.compute()

    resultado_label.config(text=f'Acción recomendada: {sistema.output["accion"]:.2f}')

# Crear la ventana principal
root = tk.Tk()
root.title("Sistema Difuso de Parqueadero")

# Crear y ubicar los widgets
ttk.Label(root, text="Ocupación del parqueadero (%)").grid(column=0, row=0, padx=10, pady=10)
ocupacion_entry = ttk.Entry(root)
ocupacion_entry.grid(column=1, row=0, padx=10, pady=10)

ttk.Label(root, text="Hora del día (0-23)").grid(column=0, row=1, padx=10, pady=10)
hora_entry = ttk.Entry(root)
hora_entry.grid(column=1, row=1, padx=10, pady=10)

calcular_button = ttk.Button(root, text="Calcular Acción", command=calcular_accion)
calcular_button.grid(column=0, row=2, columnspan=2, padx=10, pady=10)

resultado_label = ttk.Label(root, text="Acción recomendada: ")
resultado_label.grid(column=0, row=3, columnspan=2, padx=10, pady=10)

# Iniciar el bucle principal
root.mainloop()
