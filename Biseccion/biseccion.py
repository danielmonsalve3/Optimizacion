import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sympy import symbols, sympify, lambdify

# ── Ingreso interactivo de la función ────────────────────────────────
x = symbols('x')
while True:
    funcion_str = input("Ingresa f(x): ").strip()
    try:
        expr = sympify(funcion_str)
        f    = lambdify(x, expr, modules=['numpy', 'math'])
        _    = float(f(1))   # prueba de evaluación
        print(f"  → f(x) = {expr}")
        break
    except Exception as e:
        print(f"  ✗ Función inválida: {e}. Inténtalo de nuevo.")

# ── Método de bisección con tabla ────────────────────────────────────
def biseccion(f, xl, xu, tolerancia):

    if f(xl) * f(xu) > 0:
        print("No existe raíz en el intervalo dado")
        return None

    iteraciones = []
    xr_old = xl
    i = 0

    while True:
        xr    = (xl + xu) / 2
        error = abs((xr - xr_old) / xr) if i > 0 else None

        iteraciones.append([i, xl, xu, xr, f(xr), error])

        if f(xr) == 0 or (error is not None and error < tolerancia):
            break

        if f(xl) * f(xr) < 0:
            xu = xr
        else:
            xl = xr

        xr_old = xr
        i += 1

    tabla = pd.DataFrame(iteraciones,
                         columns=["Iteración", "xl", "xu", "xr", "f(xr)", "Error"])
    return xr, tabla

# ── Parámetros y ejecución ───────────────────────────────────────────
x_lower    = int(input("Ingrese el limite inferior: "))
x_upper    =  int(input("Ingrese el limite superior: "))
tolerancia =  0.000

raiz, tabla = biseccion(f, x_lower, x_upper, tolerancia)

print("Raíz aproximada:", raiz)
print(tabla)


#Gráfica 1: Función f(x) con la raíz encontrada

x_vals = np.linspace(x_lower - 5, x_upper + 5, 500)
y_vals = f(x_vals)

fig, ax = plt.subplots(figsize=(9, 5))

# Curva de la función
ax.plot(x_vals, y_vals, color='steelblue', linewidth=2.2, label=r'$f(x) = 3x^2 - 120x + 100$')

# Eje horizontal
ax.axhline(0, color='black', linewidth=0.8, linestyle='--')

# Intervalo inicial
ax.axvline(x_lower, color='orange', linewidth=1.5, linestyle=':', label=f'$x_l = {x_lower}$')
ax.axvline(x_upper, color='green',  linewidth=1.5, linestyle=':', label=f'$x_u = {x_upper}$')

# Raíz encontrada
ax.scatter([raiz], [f(raiz)], color='red', zorder=5, s=80, label=f'Raíz ≈ {raiz:.6f}')
ax.axvline(raiz, color='red', linewidth=1, linestyle='--', alpha=0.5)
ax.annotate(f'  xr ≈ {raiz:.4f}',
            xy=(raiz, 0), xytext=(raiz + 1.5, max(y_vals) * 0.3),
            arrowprops=dict(arrowstyle='->', color='red'),
            color='red', fontsize=10)

ax.set_title('Gráfica de $f(x)$ y raíz encontrada por bisección', fontsize=13, fontweight='bold')
ax.set_xlabel('$x$', fontsize=12)
ax.set_ylabel('$f(x)$', fontsize=12)
ax.legend(fontsize=10)
ax.grid(True, linestyle='--', alpha=0.4)
plt.tight_layout()
plt.show()

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

errores = tabla["Error"].dropna()

fig, ax = plt.subplots(figsize=(10, 5))

# Fondo
fig.patch.set_facecolor("#0f0f1a")
ax.set_facecolor("#0f0f1a")

# Línea principal con gradiente de color usando scatter
x = range(1, len(errores) + 1)
ax.plot(x, errores, color="#00c9ff", linewidth=2, zorder=3)
ax.fill_between(x, errores, alpha=0.15, color="#00c9ff")

# Puntos destacados
ax.scatter(x, errores, color="#ffffff", s=40, zorder=5, linewidths=1.2, edgecolors="#00c9ff")

# Rejilla sutil
ax.grid(True, linestyle="--", linewidth=0.5, color="#ffffff22", zorder=0)
ax.set_axisbelow(True)

# Ejes
ax.spines[["top", "right"]].set_visible(False)
ax.spines[["left", "bottom"]].set_color("#ffffff33")
ax.tick_params(colors="#aaaaaa", labelsize=10)

# Etiquetas y título
ax.set_title("Error vs Iteraciones", fontsize=15, fontweight="bold",
             color="#ffffff", pad=16)
ax.set_xlabel("Iteración", fontsize=11, color="#aaaaaa", labelpad=10)
ax.set_ylabel("Error relativo", fontsize=11, color="#aaaaaa", labelpad=10)

# Formato de eje Y en notación científica si los valores son muy pequeños
ax.yaxis.set_major_formatter(mticker.ScalarFormatter(useMathText=True))
ax.ticklabel_format(style="sci", axis="y", scilimits=(0, 0))
ax.yaxis.get_offset_text().set_color("#aaaaaa")

# Anotación del último error
ultimo_x = list(x)[-1]
ultimo_y = errores.iloc[-1]
ax.annotate(f"{ultimo_y:.2e}",
            xy=(ultimo_x, ultimo_y),
            xytext=(ultimo_x - len(x) * 0.08, ultimo_y * 1.3),
            fontsize=9, color="#00c9ff",
            arrowprops=dict(arrowstyle="->", color="#00c9ff", lw=1.2))

plt.tight_layout()
plt.show()