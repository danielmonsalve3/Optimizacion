# METODO BUSQUEDA ALEATORIA
import sympy as sp
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
# Axes3D para poder graficar en tres dimensiones.

# INGRESO DE DATOS
# Usa sympy para leer tu función de dos variables
x, y = sp.symbols('x y')

funcion_str = input("Ingrese la función f(x,y) (ej. x**2 + y**2 -2*x - 4*y +5): ")
tipo = input("¿Desea maximizar o minimizar? (max/min): ")
# lambdify para convertirla en una función de Python que recibe dos parámetros: f(X, Y).
f_sym = sp.sympify(funcion_str)
f = sp.lambdify((x, y), f_sym, 'numpy')
# En lugar de un solo intervalo, se pide definir un "rectángulo"
# o área de búsqueda ingresando los límites mínimos y máximos tanto para x (xl, xu) como para y (yl, yu).
# Rangos
xl = float(input("Ingrese x mínimo: "))  # 0.5  
xu = float(input("Ingrese x máximo: "))  # 1.5
yl = float(input("Ingrese y mínimo: "))  # 1.5
yu = float(input("Ingrese y máximo: "))  # 2.5
# n_iter significa exactamente cuántos puntos aleatorios se quiere probar.
n_iter = int(input("Número de iteraciones: "))

# BUSQUEDA ALEATORIA
# Para que sea funcional, a menudo requiere miles o decenas de miles de iteraciones.
tabla = []

if tipo == "max":
    mejor_valor = -1e9
else:
    mejor_valor = 1e9
# En cada paso, usa np.random.rand() para generar dos números al azar entre 0 y 1 (r1 y r2).
# Evalúa la función en esa coordenada aleatoria (f_val). 
# Si se busca maximizar y este nuevo valor es mayor que el mejor que se tenia (mejor_valor)
# se actualiza y guarda las coordenadas (mejor_x, mejor_y).
for i in range(n_iter):
    
    r1 = np.random.rand()
    r2 = np.random.rand()
    
    x_rand = xl + (xu - xl) * r1
    y_rand = yl + (yu - yl) * r2
    
    f_val = f(x_rand, y_rand)
    
    tabla.append([i, x_rand, y_rand, f_val])
    
    if tipo == "max":
        if f_val > mejor_valor:
            mejor_valor = f_val
            mejor_x = x_rand
            mejor_y = y_rand
    else:
        if f_val < mejor_valor:
            mejor_valor = f_val
            mejor_x = x_rand
            mejor_y = y_rand


# TABLA

df = pd.DataFrame(tabla, columns=["Iteración", "x", "y", "f(x,y)"])
print("\nTabla de Iteraciones:")
print(df)

print("\nMejor punto encontrado:")
print("x =", mejor_x)
print("y =", mejor_y)
print("f(x,y) =", mejor_valor)


# GRAFICA DE LA FUNCION

X = np.linspace(xl, xu, 100)
Y = np.linspace(yl, yu, 100)
X, Y = np.meshgrid(X, Y)
Z = f(X, Y)


plt.figure()
plt.axvline(mejor_x, color='cyan', linewidth=0.7, linestyle='--', alpha=0.5)
plt.axhline(mejor_y, color='cyan', linewidth=0.7, linestyle='--', alpha=0.5)
# Crea un mapa topográfico usando plt.contour. Las líneas representan alturas (valores de la función)
plt.contour(X, Y, Z)
plt.scatter(mejor_x, mejor_y)
plt.title(f'$f(x,y) = {sp.latex(f_sym)}$')
plt.xlabel("x")
plt.ylabel("y")

plt.scatter(mejor_x, mejor_y, color='red', s=120, zorder=5,
           edgecolors='black', linewidths=1.5,
           label=f'{"Máximo" if tipo=="max" else "Mínimo"}: ({mejor_x:.3f}, {mejor_y:.3f})\nf = {mejor_valor:.4f}')

plt.legend(loc='upper right', fontsize=9,
          framealpha=0.6, facecolor='black', labelcolor='white')
plt.grid(True, linestyle='--', linewidth=0.4, alpha=0.3)

plt.tight_layout()
plt.show()


X = np.linspace(xl, xu, 100)
Y = np.linspace(yl, yu, 100)
X, Y = np.meshgrid(X, Y)
Z = f(X, Y)

fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')
# se us plot_surface para dibujar el "terreno" tridimensional de la función.
ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.8)

ax.scatter(mejor_x, mejor_y, mejor_valor,
           color='red', s=80, zorder=5,
           label=f'{"Máximo" if tipo=="max" else "Mínimo"}: ({mejor_x:.3f}, {mejor_y:.3f})\nf = {mejor_valor:.4f}')

ax.set_title(f'$f(x,y) = {sp.latex(f_sym)}$')
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("f(x,y)")
ax.legend(fontsize=9)

plt.tight_layout()
plt.show()