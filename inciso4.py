"""
Este código realiza una simulación Monte Carlo para estimar la probabilidad conjunta P(XY <= 3) donde X e Y son 
variables aleatorias independientes con distribuciones exponenciales. La particularidad de Y es que su parámetro 
lambda depende del valor de X, siendo este 1/X.

El proceso se realiza de la siguiente manera:

1. Se define el número total de simulaciones y el parámetro lambda para la distribución exponencial de X.
2. Se genera una muestra de variables aleatorias para X utilizando la transformada inversa de la distribución 
   exponencial.
3. Para cada valor simulado de X, se genera una variable aleatoria Y, cuyo parámetro lambda es 1/X, 
   representando así una distribución exponencial condicionada al valor de X.
4. Se calcula la proporción de las simulaciones donde el producto XY es menor o igual a 3, lo que sirve como 
   estimación de la probabilidad buscada.
5. Se grafica un histograma del producto XY para visualizar la distribución de los resultados de la simulación.
6. Se añade una línea vertical en el valor 3 para marcar el umbral de interés en el histograma.

Se utiliza la librería NumPy para el cálculo y manejo de las simulaciones y Matplotlib para la creación de 
gráficas. La función 'generar_exponencial_condicional' itera a través de cada muestra de X para generar 
correspondientes muestras de Y, respetando la condicionalidad del parámetro lambda de Y dado X.

El resultado impreso es una estimación de la probabilidad P(XY <= 3) basada en el método de Monte Carlo, 
y el histograma proporciona una visualización de la distribución del producto XY en relación con este umbral.
"""


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# Parámetros de la simulación
n_simulaciones = 10000  # Número de simulaciones
lambda_valor_X = 1  # Parámetro de la distribución exponencial para X

# Función para generar variables aleatorias exponenciales para X
def generar_exponencial(n, lambda_val):
    u = np.random.rand(n)  # Generar n números aleatorios uniformes en [0, 1]
    x = -np.log(1 - u) / lambda_val  # Transformada inversa para obtener exponenciales
    return x

# Función para generar variables aleatorias exponenciales para Y dado X
def generar_exponencial_condicional(n, x_values):
    y_samples = np.empty(n)
    for i in range(n):
        lambda_val_Y = 1 / x_values[i]  # La tasa de Y es la inversa del valor de X
        u = np.random.rand()  # Un único número aleatorio uniforme
        y_samples[i] = -np.log(1 - u) / lambda_val_Y  # Transformada inversa para Y
    return y_samples

# Generar muestras para X y Y
X_samples = generar_exponencial(n_simulaciones, lambda_valor_X)
Y_samples = generar_exponencial_condicional(n_simulaciones, X_samples)

# Calcular la proporción de veces que XY <= 3
P_XY_leq_3 = np.mean(X_samples * Y_samples <= 3)

# Imprimir la estimación de la probabilidad
print(f"Estimación de P(XY <= 3): {P_XY_leq_3}")

# Producto de X y Y para identificar dónde caen respecto al umbral de 3
producto_XY = X_samples * Y_samples

# Crear el histograma del producto XY
plt.hist(producto_XY, bins=50, density=True, alpha=0.7, label='Producto XY')

# Añadir una línea vertical en x=3 para indicar el umbral de interés
plt.axvline(x=3, color='r', linestyle='dashed', linewidth=2, label='XY=3')

# Añadir títulos y leyendas
plt.title('Histograma del Producto XY')
plt.xlabel('Producto XY')
plt.ylabel('Densidad')
plt.legend()

# Crear un objeto PDF para guardar las graficas
pdf_pages = PdfPages('inciso4grafica.pdf')

# Guardar la figura en el archivo PDF
pdf_pages.savefig(plt.gcf())

# Cerrar el objeto PDF para guardar las graficas
pdf_pages.close()