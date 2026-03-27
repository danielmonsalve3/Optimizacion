
# METODO RAZON DORADA
import math
import matplotlib.pyplot as plt
import sys


# EVALUACIÓN DE FUNCIÓN

def evaluar_funcion(expr, x):
    entorno = {
        "x": x,
        "sin": math.sin, "cos": math.cos, "tan": math.tan,
        "exp": math.exp, "log": math.log,
        "sqrt": math.sqrt, "pi": math.pi, "e": math.e
    }
    try:
        # Toma el texto ingresado por el usuario y lo ejecuta como una operación matemática real
        return eval(expr, {"__builtins__": None}, entorno)
    except Exception as ex:
        print(f"Error al evaluar la función: {ex}")
        return None


# MÉTODO SECCIÓN DORADA

def seccion_dorada(func_str, xl, xu, tipo_optimizacion, maxit=50, es=0.01):
    R = (math.sqrt(5) - 1) / 2   # = 0.61803

    historial = []                # guarda datos de cada iteración

    iteracion = 1
    d  = R * (xu - xl)
    x1 = xl + d
    x2 = xu - d
    f1 = evaluar_funcion(func_str, x1)
    f2 = evaluar_funcion(func_str, x2)

    # Óptimo inicial
    if tipo_optimizacion == 'max':
        xopt, fx = (x1, f1) if f1 > f2 else (x2, f2)
    else:
        xopt, fx = (x1, f1) if f1 < f2 else (x2, f2)
    # El ciclo while se detiene cuando el error aproximado (ea) es menor al deseado (es) o se alcanza el máximo de iteraciones.
    while True:
        d = R * d

        condicion = (f1 > f2) if tipo_optimizacion == 'max' else (f1 < f2)

        if condicion:
            xl = x2;  x2 = x1;  x1 = xl + d
            f2 = f1;  f1 = evaluar_funcion(func_str, x1)
        else:
            xu = x1;  x1 = x2;  x2 = xu - d
            f1 = f2;  f2 = evaluar_funcion(func_str, x2)

        iteracion += 1

        if tipo_optimizacion == 'max':
            xopt, fx = (x1, f1) if f1 > f2 else (x2, f2)
        else:
            xopt, fx = (x1, f1) if f1 < f2 else (x2, f2)

        # Error aproximado
        ea = (1.0 - R) * abs((xu - xl) / xopt) * 100.0 if xopt != 0 else 0.0

        # Registrar fila del historial
        historial.append({
            "iter": iteracion,
            "xl":   round(xl,   6),
            "xu":   round(xu,   6),
            "x1":   round(x1,   6),
            "x2":   round(x2,   6),
            "f1":   round(f1,   6),
            "f2":   round(f2,   6),
            "xopt": round(xopt, 6),
            "fx":   round(fx,   6),
            "ea":   round(ea,   6),
        })

        if ea <= es or iteracion >= maxit:
            break

    return xopt, fx, ea, iteracion, historial


# TABLA DE ITERACIONES
# Genera una tabla organizada en la consola que muestra cómo cambian los límites (xl, xu) y el error en cada paso.
def imprimir_tabla(historial):
    encabezado = (
        f"{'Iter':>4} | {'xl':>10} | {'xu':>10} | "
        f"{'x1':>10} | {'x2':>10} | "
        f"{'f(x1)':>10} | {'f(x2)':>10} | "
        f"{'xopt':>10} | {'f(xopt)':>10} | {'ea (%)':>10}"
    )
    separador = "-" * len(encabezado)
    print("\n" + separador)
    print("TABLA DE ITERACIONES")
    print(separador)
    print(encabezado)
    print(separador)
    for fila in historial:
        print(
            f"{fila['iter']:>4} | {fila['xl']:>10.6f} | {fila['xu']:>10.6f} | "
            f"{fila['x1']:>10.6f} | {fila['x2']:>10.6f} | "
            f"{fila['f1']:>10.6f} | {fila['f2']:>10.6f} | "
            f"{fila['xopt']:>10.6f} | {fila['fx']:>10.6f} | {fila['ea']:>10.6f}"
        )
    print(separador)


# GRÁFICA DE LA FUNCIÓN
# Usa matplotlib para dibujar la curva de la función y marca con un punto rojo el valor óptimo encontrado.
def graficar_funcion(func_str, xl_orig, xu_orig, xopt, fx):
    margen = (xu_orig - xl_orig) * 0.1
    xs = []
    ys = []
    n_puntos = 400
    paso = (xu_orig - xl_orig + 2 * margen) / n_puntos
    x = xl_orig - margen
    for _ in range(n_puntos + 1):
        y = evaluar_funcion(func_str, x)
        if y is not None:
            xs.append(x)
            ys.append(y)
        x += paso

    plt.figure(figsize=(8, 5))
    plt.plot(xs, ys, color='royalblue', linewidth=2, label=f"f(x) = {func_str}")
    plt.axvline(xopt, color='crimson', linestyle='--', linewidth=1.2, label=f"x_optimo = {xopt:.4f}")
    plt.scatter([xopt], [fx], color='crimson', zorder=5, s=80, label=f"f(x_optimo) = {fx:.4f}")
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.title("Gráfica de la función")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()



# GRÁFICA DE ERROR vs ITERACIONES
# Muestra una curva del error descendiente
def graficar_error(historial):
    iters  = [fila["iter"] for fila in historial]
    errores = [fila["ea"]  for fila in historial]

    plt.figure(figsize=(8, 5))
    plt.plot(iters, errores, marker='o', color='darkorange',
             linewidth=2, markersize=5, label="Error aproximado (%)")
    plt.xlabel("Iteración")
    plt.ylabel("Error aproximado (%)")
    plt.title("Error aproximado vs. Iteraciones")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()
    



# PROGRAMA PRINCIPAL
# Pide al usuario la función, si quiere maximizar o minimizar, los límites y el error permitido.

print("─" * 50)
print("  MÉTODO DE BÚSQUEDA DE LA SECCIÓN DORADA")
print("─" * 50)
print("Usa 'x' como variable. Ejemplo: 2*sin(x) - (x**2/10)\n")

func_str = input("Función f(x): ")

tipo = input("¿Maximizar (max) o minimizar (min)? ").strip().lower()
while tipo not in ['max', 'min']:
    tipo = input("  Escribe 'max' o 'min': ").strip().lower()

try:
    xl    = float(input("Límite inferior (xl): "))
    xu    = float(input("Límite superior (xu): "))
    if xl >= xu:
        print("Error: xl debe ser menor que xu.")
        sys.exit()
    es    = float(input("Error esperado (%) [ej. 0.01]: "))
    maxit = int(input("Máx. iteraciones [ej. 100]: "))
except ValueError:
    print("Error: introduce valores numéricos válidos.")
    sys.exit()

# Guardar límites originales para la gráfica
xl_orig, xu_orig = xl, xu

print()
xopt, fx, ea, iteraciones, historial = seccion_dorada(
    func_str, xl, xu, tipo, maxit, es
)

# ── Resultado final ──
print("\n" + "─" * 40)
print(f"Resultado ({tipo}):")
print(f"  x óptimo   = {xopt:.6f}")
print(f"  f(xopt)    = {fx:.6f}")
print(f"  Error (ea) = {ea:.6f} %")
print(f"  Iteraciones = {iteraciones}")
print("─" * 40)

# ── Tabla ──
imprimir_tabla(historial)

# ── Gráficas ──
graficar_funcion(func_str, xl_orig, xu_orig, xopt, fx)
graficar_error(historial)