import numpy as np
from PIL import Image, ImageTk
import random as rd
import tkinter as tk
from tkinter import ttk
from io import BytesIO
import requests

# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Evolución de Imagen por Algoritmo Genético")
root.geometry("800x600")

# Imagen de referencia (reducimos el tamaño para hacer la evolución más rápida)
url = "https://photoshop-kopona.com/uploads/posts/2019-01/1546709726_butterfly_081.jpg"
rta = requests.get(url)
imagen_ref = Image.open(BytesIO(rta.content))
imagen_ref = imagen_ref.resize((75, 75))  # Reducción del tamaño
imgArrayOriginal = np.array(imagen_ref)

# Dimensiones de la imagen
img_height, img_width, _ = imgArrayOriginal.shape

# Inicialización de la población
def crear_poblacion(poblacion_size):
    return [np.random.randint(0, 256, (img_height, img_width, 3), dtype=np.uint8) for _ in range(poblacion_size)]

# Función de aptitud (fitness)
def calcular_fitness(img_individuo):
    return np.sum(np.abs(imgArrayOriginal - img_individuo))

# Selección de los mejores individuos
def seleccion(poblacion, fitness_scores, num_seleccion):
    seleccionados = np.argsort(fitness_scores)[:num_seleccion]
    return [poblacion[i] for i in seleccionados]

# Cruce entre dos individuos con orientación hacia la referencia
def cruce(padre1, padre2):
    hijo = np.copy(padre1)
    for i in range(img_height):
        for j in range(img_width):
            if np.random.rand() > 0.5:
                hijo[i][j] = padre2[i][j]
    return hijo

# Mutación más controlada (hacia la imagen de referencia)
def mutar(img_individuo, tasa_mutacion=0.01):
    for i in range(img_height):
        for j in range(img_width):
            if np.random.rand() < tasa_mutacion:
                # Mutación más controlada: modificar en dirección a la imagen de referencia
                img_individuo[i][j] += np.sign(imgArrayOriginal[i][j] - img_individuo[i][j]) * np.random.randint(1, 5)
                img_individuo[i][j] = np.clip(img_individuo[i][j], 0, 255)  # Aseguramos que se mantenga en rango
    return img_individuo

# Evolución de la población
def evolucionar(poblacion, num_generaciones, tasa_seleccion, tasa_mutacion, tasa_enfriamiento=0.99):
    for generacion in range(num_generaciones):
        # Calcular aptitud
        fitness_scores = [calcular_fitness(img) for img in poblacion]
        
        # Selección
        poblacion_seleccionada = seleccion(poblacion, fitness_scores, int(len(poblacion) * tasa_seleccion))
        
        # Reproducción y mutación
        nueva_poblacion = []
        while len(nueva_poblacion) < len(poblacion):
            padre1, padre2 = rd.sample(poblacion_seleccionada, 2)
            hijo = cruce(padre1, padre2)
            hijo = mutar(hijo, tasa_mutacion)
            nueva_poblacion.append(hijo)
        
        # Actualizar la población
        poblacion = nueva_poblacion
        
        # Mostrar progreso en la interfaz
        mostrar_img(poblacion[0], f"Generación {generacion + 1}")
        
        # Enfriamiento gradual (reducimos la tasa de mutación con el tiempo)
        tasa_mutacion *= tasa_enfriamiento
        
        root.update()

# Función para mostrar una imagen en la interfaz
def mostrar_img(img_array, titulo="Imagen"):
    img = Image.fromarray(img_array)
    img_tk = ImageTk.PhotoImage(img)
    panel.config(image=img_tk)
    panel.image = img_tk
    label_titulo.config(text=titulo)

# Interfaz gráfica
panel = tk.Label(root)
panel.pack(pady=20)

label_titulo = ttk.Label(root, text="Imagen inicial", font=("Helvetica", 16))
label_titulo.pack()

# Botón para iniciar la evolución
def iniciar_evolucion():
    poblacion = crear_poblacion(20)
    evolucionar(poblacion, num_generaciones=10000000, tasa_seleccion=0.5, tasa_mutacion=0.05)

btn_iniciar = ttk.Button(root, text="Iniciar Evolución", command=iniciar_evolucion)
btn_iniciar.pack(pady=20)

root.mainloop()
