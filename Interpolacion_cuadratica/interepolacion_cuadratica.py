import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


# INGRESO DE DATOS
x = sp.symbols('x')

funcion_str = input("Ingrese la función f(x): ")
tipo = input("¿Desea maximizar o minimizar? (max/min): ")

f_sym = sp.sympify(funcion_str)
f = sp.lambdify(x, f_sym, 'numpy')

# Puntos iniciales
x0 = float(input("Ingrese x0: "))
x1 = float(input("Ingrese x1: "))
x2 = float(input("Ingrese x2: "))

tol = float(input("Tolerancia: "))
max_iter = int(input("Máximo número de iteraciones: "))

# Si es maximización se multiplica por -1
if tipo == "max":
    def f_eval(x):
        return -f(x)
else:
    def f_eval(x):
        return f(x)


# METODO INTERPOLACION PARABOLICA

tabla = []
errores = []

for i in range(max_iter):
    
    f0 = f_eval(x0)
    f1 = f_eval(x1)
    f2 = f_eval(x2)

    # Formula interpolación parabólica
    numerador = (f0*(x1**2 - x2**2) +
                 f1*(x2**2 - x0**2) +
                 f2*(x0**2 - x1**2))

    denominador = (2*f0*(x1 - x2) +
                   2*f1*(x2 - x0) +
                   2*f2*(x0 - x1))

    x3 = numerador / denominador

    error = abs(x3 - x2)
    errores.append(error)

    tabla.append([i, x0, x1, x2, x3, error])

    if error < tol:
        break

    # Actualizar puntos
    x0, x1, x2 = x1, x2, x3


# TABLA DE ITERACIONES

df = pd.DataFrame(tabla, columns=["Iter", "x0", "x1", "x2", "x3", "Error"])
print("\nTabla de Iteraciones:")
print(df)

# Resultado final
if tipo == "max":
    resultado = x3
    valor = f(resultado)
    print("\nMáximo en x =", resultado)
    print("f(x) =", valor)
else:
    resultado = x3
    valor = f(resultado)
    print("\nMínimo en x =", resultado)
    print("f(x) =", valor)


# GRAFICA ERROR VS ITERACIONES

plt.figure(figsize=(8, 4))
plt.plot(range(1, len(errores) + 1), errores, color='orange',
         linewidth=1.8, marker='o', markersize=4, label='Error aproximado')

# Línea horizontal en el error final (criterio de parada)
plt.axhline(y=errores[-1], color='gray', linestyle=':', linewidth=1,
            label=f'Error final: {errores[-1]:.4f}%')

# Anotar el último punto
plt.annotate(f'{errores[-1]:.4f}%',
             xy=(len(errores), errores[-1]),
             xytext=(len(errores) - 1.5, errores[-1] + max(errores) * 0.05),
             fontsize=8, color='steelblue')

plt.xlabel("Iteración")
plt.ylabel("Error aproximado (%)")
plt.title("Convergencia del error")
plt.legend(fontsize=8)
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()


# GRAFICA DE LA FUNCION

x_vals = np.linspace(resultado - 5, resultado + 5, 400)
y_vals = f(x_vals)
y_opt  = f(resultado)

plt.figure(figsize=(8, 5))
plt.plot(x_vals, y_vals, color='purple', linewidth=2, label='f(x)')

# Líneas punteadas desde los ejes hasta el punto óptimo
plt.axvline(resultado, color='gray', linestyle=':', linewidth=1)
plt.axhline(y_opt,     color='gray', linestyle=':', linewidth=1)

# Punto óptimo destacado
plt.scatter(resultado, y_opt, color='crimson', zorder=5, s=70,
            label=f'xopt = {resultado:.4f}\nf(xopt) = {y_opt:.4f}')

# Etiqueta junto al punto
plt.annotate(f'  ({resultado:.3f}, {y_opt:.3f})',
             xy=(resultado, y_opt),
             xytext=(resultado + 0.3, y_opt + (max(y_vals) - min(y_vals)) * 0.05),
             fontsize=8, color='crimson')

plt.xlabel("x")
plt.ylabel("f(x)")
plt.title("Función y punto óptimo")
plt.legend(fontsize=8)
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()