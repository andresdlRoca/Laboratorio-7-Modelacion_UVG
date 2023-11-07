"""
Este código realiza una simulación Monte Carlo estratificada utilizando la distribución exponencial como base. 
La simulación estratificada es una técnica de reducción de varianza en la que se divide el dominio de la variable 
aleatoria en diferentes 'estratos' y se realiza una simulación independiente en cada uno de ellos.

El proceso es el siguiente:

1. Se establece el número de simulaciones y el parámetro lambda de la distribución exponencial.
2. Se divide el dominio de la distribución exponencial en tres estratos: [0, 1), [1, 3) y [3, ∞).
3. Se calculan las probabilidades de caer en cada estrato de acuerdo a la función de distribución acumulada de la 
   distribución exponencial.
4. Se asigna un número de simulaciones a cada estrato proporcional a su probabilidad.
5. Se generan variables aleatorias para cada estrato:
   - Para el primer estrato, se transforman variables uniformes en [0, 1) a exponenciales utilizando la transformada inversa.
   - Para el segundo estrato, se ajusta la generación de variables uniformes al rango de la CDF correspondiente 
     y luego se aplica la transformada inversa.
   - Para el tercer estrato, se utiliza el método de la transformada inversa con un ajuste para iniciar en el límite inferior del estrato.
6. Se calcula la media de las simulaciones en cada estrato y se pondera por su probabilidad para obtener el valor esperado estratificado.
7. Se combinan todas las simulaciones en un solo arreglo para visualización.
8. Se crea un histograma de las simulaciones y se superpone la función de densidad de probabilidad teórica de la 
   distribución exponencial para comparar.

"""


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# Parámetros de la simulación
n_simulaciones = 10000  # Número de simulaciones
lambda_valor = 1  # Parámetro de la distribución exponencial (Tasa de llegada)

# Generar variables aleatorias exponenciales para el primer estrato (0 a 1)
def generar_estratificado_primer_estrato(n, lambda_val):
    u = np.random.rand(n)  # Generar n números aleatorios uniformes en [0, 1]
    x = -np.log(1 - u) / lambda_val  # Transformada inversa
    return x

# Generar variables aleatorias exponenciales para el segundo estrato (1 a 3)
def generar_estratificado_segundo_estrato(n, lambda_val, lower_bound, upper_bound):
    cdf_lower = 1 - np.exp(-lambda_val * lower_bound)
    cdf_upper = 1 - np.exp(-lambda_val * upper_bound)
    u = cdf_lower + (cdf_upper - cdf_lower) * np.random.rand(n)
    x = -np.log(1 - u) / lambda_val
    return x

# Generar variables aleatorias exponenciales para el tercer estrato (3 a ∞)
def generar_estratificado_tercer_estrato(n, lambda_val, lower_bound):
    u = np.random.rand(n)
    x = -np.log(u) / lambda_val + lower_bound
    return x

# Calcular la cantidad de simulaciones para cada estrato basado en la probabilidad de cada intervalo
P1 = 1 - np.exp(-lambda_valor * 1)  # Probabilidad del primer estrato
P2 = np.exp(-lambda_valor * 1) - np.exp(-lambda_valor * 3)  # Probabilidad del segundo estrato
P3 = np.exp(-lambda_valor * 3)  # Probabilidad del tercer estrato

n1 = int(n_simulaciones * P1)
n2 = int(n_simulaciones * P2)
n3 = n_simulaciones - n1 - n2  # El resto para el tercer estrato

# Generar las simulaciones estratificadas
simulaciones_1 = generar_estratificado_primer_estrato(n1, lambda_valor)
simulaciones_2 = generar_estratificado_segundo_estrato(n2, lambda_valor, 1, 3)
simulaciones_3 = generar_estratificado_tercer_estrato(n3, lambda_valor, 3)

# Calcular el valor esperado en cada estrato
E1 = np.mean(simulaciones_1)
E2 = np.mean(simulaciones_2)
E3 = np.mean(simulaciones_3)

# Valor esperado estratificado
valor_esperado_estratificado = E1 * P1 + E2 * P2 + E3 * P3

print(valor_esperado_estratificado)



# Combina todas las simulaciones en un solo arreglo para el histograma
todas_simulaciones = np.concatenate((simulaciones_1, simulaciones_2, simulaciones_3))

# Crear el histograma de las simulaciones estratificadas
plt.hist(todas_simulaciones, bins=50, density=True, alpha=0.7, label='Simulaciones Estratificadas')

# Generar puntos para la distribución teórica exponencial
x_teorico = np.linspace(0, np.max(todas_simulaciones), 1000)
y_teorico = lambda_valor * np.exp(-lambda_valor * x_teorico)

# Graficar la distribución teórica exponencial
plt.plot(x_teorico, y_teorico, 'r', lw=2, label='Distribución Teórica Exponencial')

# Añadir títulos y leyendas
plt.title('Simulaciones Estratificadas vs. Distribución Teórica Exponencial')
plt.xlabel('Valor')
plt.ylabel('Densidad')
plt.legend()



# Crear un objeto PDF para guardar las graficas
pdf_pages = PdfPages('inciso3grafica.pdf')

# Guardar la figura en el archivo PDF
pdf_pages.savefig(plt.gcf())

# Cerrar el objeto PDF para guardar las graficas
pdf_pages.close()