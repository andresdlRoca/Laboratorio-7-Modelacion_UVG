'''
Objetivo de las variables de control:

El objetivo principal de las variables de control es reducir la varianza en 
las estimaciones de parámetros estadísticos, como la media o el valor esperado.

Variable de Control:

Una "variable de control" es una variable adicional que se introduce en una 
simulación o experimento para ayudar a estimar un parámetro de interés de manera 
más precisa. Esta variable debe estar relacionada de alguna manera con la variable de interés.

Efecto de la Variable de Control:

La variable de control se elige de tal manera que su media (o valor esperado) 
sea conocida o fácil de estimar con alta precisión.
La variable de control se utiliza para ajustar las observaciones de la variable de
interés con el objetivo de reducir la varianza en la estimación.
Ajuste de Observaciones:

En un enfoque de variables de control, se ajustan las observaciones de la variable 
de interés utilizando la información de la variable de control.
El ajuste se basa en la diferencia entre el valor esperado real de 
la variable de interés y el valor esperado de la variable de control.
Beneficios:

Al introducir una variable de control y utilizarla para ajustar las observaciones, 
se puede reducir la variabilidad en las estimaciones del parámetro de interés.
Esto puede llevar a estimaciones más precisas y reducir el error estándar de la 
estimación, lo que a su vez puede requerir un número menor de observaciones o simulaciones 
para obtener resultados confiables.
Ejemplo Aplicado:

Un ejemplo común de variable de control es cuando se realiza una simulación para estimar el tiempo promedio 
que un cliente pasa en una tienda. Si la tasa de llegada de los clientes es conocida, se puede utilizar como 
variable de control. El tiempo que pasa un cliente en la tienda se ajusta utilizando la tasa de llegada como 
variable de control para mejorar la estimación del tiempo promedio.
'''

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


# Parámetros de la simulación
n_simulaciones = 10000  # Número de simulaciones (Mientras mas mejor sera la estimacion del valor esperado)
lambda_valor = 1  # Parámetro de la distribución exponencial (Tasa de llegada)

# Función para generar variables aleatorias exponenciales usando el método de transformada inversa
def generar_exponencial(n, lambda_val):
    u = np.random.rand(n)  # Generar n números aleatorios uniformes en [0, 1]
    x = -np.log(1 - u) / lambda_val  # Aplicar transformada inversa para obtener exponenciales
    return x

# Generar variables aleatorias exponenciales
simulaciones = generar_exponencial(n_simulaciones, lambda_valor)

# Calcular el valor esperado utilizando variables de control
mu_real = 1 / lambda_valor  # Valor esperado real de la exponencial

# Definir una variable de control, por ejemplo, una exponencial con otro parámetro
control_variable = generar_exponencial(n_simulaciones, lambda_valor * 2)

# Calcular el valor esperado con el método de variables de control
mu_control = np.mean(simulaciones + (mu_real - np.mean(control_variable)))

# Imprimir resultados
print(f"Valor esperado real: {mu_real}")
print(f"Valor esperado estimado con variables de control: {mu_control}")

pdf_pages = PdfPages('inciso2grafica.pdf')

# Graficar el histograma de las simulaciones
plt.hist(simulaciones, bins=30, density=True, alpha=0.5, color='blue', label='Simulaciones')
plt.hist(control_variable, bins=30, density=True, alpha=0.5, color='red', label='Variable de control')
plt.legend()
plt.xlabel('Valor')
plt.ylabel('Densidad')
plt.title('Histograma de Simulaciones y Variable de Control')
plt.show()

# Guardar la figura en el archivo PDF
pdf_pages.savefig(plt.gcf())

# Cerrar el objeto PDF para guardar las graficas
pdf_pages.close()