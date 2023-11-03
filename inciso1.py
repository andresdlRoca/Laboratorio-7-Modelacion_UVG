'''
La tecnica de variables antiteticas es un metodo de reduccion de varianza en simulaciones Monte Carlo. 
Este metodo aprovecha el hecho de que para ciertas distribuciones de probabilidad, se pueden generar pares 
de numeros aleatorios que, cuando se promedian, ofrecen una estimacion mas precisa del valor esperado de la 
distribucion.

Para una variable aleatoria exponencial con parametro lambda (λ), la funcion de densidad de probabilidad es:

f(x) = λ * e^(-λx), para x >= 0

y el valor esperado es E[X] = 1/λ. Para λ = 1, la funcion de densidad se simplifica a:

f(x) = e^(-x), y el valor esperado es E[X] = 1.

La funcion de distribucion acumulativa (CDF) para la distribucion exponencial es:

F(x) = 1 - e^(-λx), para x >= 0

Para generar una variable aleatoria exponencial utilizando el metodo de inversion, aplicamos:

X = -ln(1 - U)/λ

donde U es un numero aleatorio uniformemente distribuido en el intervalo [0, 1]. La variable antitetica correspondiente 
se obtiene como:

Y = -ln(U)/λ

En el caso de λ = 1, las expresiones se simplifican a:

X = -ln(1 - U)
Y = -ln(U)

Al promediar X y Y, obtenemos un estimado del valor esperado que tiene una varianza menor que si solo utilizaramos 
variables aleatorias independientes.

El valor esperado estimado se calcula como el promedio de los valores antiteticos:

E_estimado = (X + Y) / 2

Al promediar E_estimado para una gran cantidad de pares de variables (X, Y), obtenemos una estimacion precisa del 
valor esperado de la distribucion exponencial.

'''
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# Definir diferentes tamanos de muestra para realizar la simulacion
tamanosMuestra = [100, 1000, 10000, 100000]

# Diccionario para almacenar los valores esperados estimados para cada tamano de muestra
valoresEsperados = {}

for nMuestras in tamanosMuestra:
    # Generar numeros aleatorios uniformes entre 0 y 1
    numerosUniformes = np.random.uniform(low=0.0, high=1.0, size=nMuestras)

    # Generar variables aleatorias exponenciales utilizando el metodo de transformacion inversa
    variablesExponenciales = -np.log(1 - numerosUniformes)
    variablesAntiteticas = -np.log(numerosUniformes)

    # Calcular las medias de las variables antiteticas
    mediasAntiteticas = (variablesExponenciales + variablesAntiteticas) / 2

    # Estimar el valor esperado tomando la media de las medias antiteticas
    estimadoValorEsperado = np.mean(mediasAntiteticas)

    # Almacenar el resultado
    valoresEsperados[nMuestras] = estimadoValorEsperado

# Imprimir los valores esperados estimados para cada tamano de muestra de forma ordenada
for tamano, valor in valoresEsperados.items():
    print(f'Tamano de Muestra: {tamano}, Valor Esperado Estimado: {valor}')


'''
En teoria, sabemos que el valor esperado real para esta distribucion es exactamente 1. 
Matematicamente, el valor esperado E[X] para una distribucion exponencial se calcula como 1/λ​, por lo que si λ=1, entonces E[X]=1.
Los resultados de la simulacion deberian aproximarse a este valor a medida que el tamano de la muestra aumenta, debido a la Ley de los Grandes Numeros.
El output muestra estimaciones del valor esperado de una variable aleatoria exponencial con λ=1 para distintos tamanos de muestra.
- Con 100 muestras, el valor estimado es ~1.0078, cercano a 1, pero con variabilidad debido al tamano reducido de la muestra.
- Con 1,000 muestras, el valor estimado es ~1.0168, demostrando variabilidad en la estimacion con tamanos de muestra moderados.
- Con 10,000 muestras, la estimacion se acerca mucho al valor teorico con un valor de ~0.9991.
- Con 100,000 muestras, el valor estimado es ~0.9993, mostrando una excelente aproximacion al valor teorico.
A medida que el tamano de la muestra aumenta, las estimaciones tienden a converger hacia el valor teorico de 1, conforme a la Ley de los Grandes Numeros.
'''

# Crear un objeto PDF para guardar las graficas
pdf_pages = PdfPages('inciso1grafica.pdf')

# Crear una grafica para mostrar la convergencia del valor esperado estimado
plt.figure(figsize=(10, 6))
plt.plot(tamanosMuestra, list(valoresEsperados.values()),
         marker='o', linestyle='-', color='blue')
plt.axhline(y=1, color='red', linestyle='--',
            label='Valor Esperado Teorico (1)')
plt.xscale('log')  # Escala logaritmica para los tamanos de muestra
plt.xlabel('Tamano de Muestra (Escala Logaritmica)')
plt.ylabel('Valor Esperado Estimado')
plt.title('Convergencia del Valor Esperado con Variables Antiteticas')
plt.legend()
plt.grid(True)

# Guardar la figura en el archivo PDF
pdf_pages.savefig(plt.gcf())

# Cerrar el objeto PDF para guardar las graficas
pdf_pages.close()
