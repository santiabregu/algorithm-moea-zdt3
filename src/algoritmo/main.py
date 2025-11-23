import random
import math


def random_individual(n_vars=30):
    """Genera un individuo: lista de `n_vars` valores aleatorios en [0,1]."""
    return [random.random() for _ in range(n_vars)]


def zdt3(x):
    """Calcula los dos objetivos de la función de prueba ZDT3 para el vector `x`.

    Devuelve una tupla (f1, f2).
    """
    f1 = x[0]
    g = 1 + (9/29.0) * sum(x[1:])
    h = 1 - math.sqrt(f1 / g) - (f1 / g) * math.sin(10 * math.pi * f1)
    f2 = g * h
    return f1, f2


def inicializar_poblacion(N=100, n_vars=30):
    """Crea una población de `N` individuos aleatorios y calcula su fitness con ZDT3.

    Devuelve (poblacion, fitness) donde `poblacion` es lista de individuos y
    `fitness` es una lista de tuplas (f1, f2).
    """
    poblacion = [random_individual(n_vars) for _ in range(N)]
    fitness = [zdt3(ind) for ind in poblacion]
    return poblacion, fitness


def calcular_z_estrella(fitness):
    """Calcula el punto de referencia z* como los mínimos de f1 y f2 en la población.

    Devuelve una tupla (min_f1, min_f2).
    """
    f1_vals = [f[0] for f in fitness]
    f2_vals = [f[1] for f in fitness]
    return (min(f1_vals), min(f2_vals))


def generar_pesos(N):
    """Genera `N` pares de pesos (lambda1, lambda2) equiespaciados para descomposición.

    Cada par suma 1 y recorre el segmento [0,1].
    """
    lambdas = []
    for i in range(N):
        w1 = i / (N - 1)
        w2 = 1 - w1
        lambdas.append((w1, w2))
    return lambdas


def distancia(a, b):
    """Distancia euclidiana entre dos puntos 2D `a` y `b` (tuplas de dos valores)."""
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)


def vecindades(lambdas, T):
    N = len(lambdas)
    vecinos = []

    """Para cada lambda calcula los `T` índices de vecinos más cercanos por distancia.

    Devuelve una lista de listas de índices.
    """

    for i in range(N):
        distancias = []
        for j in range(N):
            d = distancia(lambdas[i], lambdas[j])
            distancias.append((d, j))

        distancias.sort(key=lambda x: x[0])
        indices = [j for _, j in distancias[:T]]
        vecinos.append(indices)

    return vecinos


def tchebycheff(f, lamb, z_ref):
    """Calcula el valor Tchebycheff ponderado para el vector objetivo `f`
    """
    return max([
        lamb[j] * abs(f[j] - z_ref[j])
        for j in range(2)
    ])

# ------------------------------------- operadores evolutivos ---------------------------------------------------------


def sbx_crossover(p1, p2, eta=20, pc=0.9):
    if random.random() > pc:
        return p1[:]

    child = []
    for x1, x2 in zip(p1, p2):
        if random.random() <= 0.5:
            if abs(x1 - x2) > 1e-14:
                x_min = min(x1, x2)
                x_max = max(x1, x2)

                rand = random.random()
                beta = 1.0 + (2.0 * (x_min - 0.0) / (x_max - x_min))
                alpha = 2.0 - beta ** -(eta + 1)

                if rand <= 1.0 / alpha:
                    betaq = (rand * alpha) ** (1.0 / (eta + 1))
                else:
                    betaq = (1.0 / (2.0 - rand * alpha)) ** (1.0 / (eta + 1))

                c = 0.5 * ((x1 + x2) - betaq * (x_max - x_min))
            else:
                c = x1
        else:
            c = x1

        # limitar a [0,1]
        c = max(0.0, min(1.0, c))
        child.append(c)

    return child


def polynomial_mutation(x, eta=20, pm=1/30):
    child = x[:]  # evitar tocar lista original
    for i in range(len(child)):
        if random.random() < pm:
            u = random.random()
            if u < 0.5:
                delta = (2*u)**(1/(eta+1)) - 1
            else:
                delta = 1 - (2*(1-u))**(1/(eta+1))
            child[i] += delta * (1.0 - 0.0)  
            child[i] = max(0.0, min(1.0, child[i]))
    return child

# -------------------------------------- moead ----------------------------------------------------------------------


def ejecutar_moead(N=40, T=15, generaciones=100, n_vars=30):

    poblacion, fitness = inicializar_poblacion(N, n_vars)
    z_ref = calcular_z_estrella(fitness)
    lambdas = generar_pesos(N)
    vecinos = vecindades(lambdas, T)

    historial = []

    for gen in range(generaciones):

        # Copiar población antes de actualizarla
        poblacion_original = [ind[:] for ind in poblacion]
        fitness_original = fitness[:]

        nuevos_fitness = []   # <<< CAMBIO >>> almacenará fitness de todos los hijos generados
        
        for i in range(N):

            Bi = vecinos[i]

            p1 = random.choice(Bi)
            p2 = random.choice(Bi)
            while p2 == p1:
                p2 = random.choice(Bi)

            # Padres de la población original
            padre1 = poblacion_original[p1][:]
            padre2 = poblacion_original[p2][:]

            # Variación
            hijo = sbx_crossover(padre1, padre2)
            hijo = polynomial_mutation(hijo)

            f_hijo = zdt3(hijo)

            nuevos_fitness.append(f_hijo)   # <<< CAMBIO >>>

            # Reemplazo local (sin actualizar z_ref aún)
            for m in Bi:
                g_hijo = tchebycheff(f_hijo, lambdas[m], z_ref)
                g_padre = tchebycheff(fitness_original[m], lambdas[m], z_ref)

                if g_hijo <= g_padre:
                    poblacion[m] = hijo[:]
                    fitness[m] = f_hijo

        # === Actualizar z* al final de la generación ===
        # <<< CAMBIO IMPORTANTE >>>
        for f_hijo in nuevos_fitness:
            z_ref = (
                min(z_ref[0], f_hijo[0]),
                min(z_ref[1], f_hijo[1])
            )

        historial.append(list(fitness))

    return poblacion, fitness, z_ref, historial



# --------------------------------------- generar archivos de resultados ------------------------------------------------

def guardar_final_pop(fitness, ruta="v2_final_pop.out"):
    with open(ruta, "w") as f:
        for f1, f2 in fitness:
            f.write(f"{f1:.6f}\t{f2:.6f}\n")

def guardar_all_pop(historial, ruta="v2_all_pop.out"):
    """
    historial: lista de listas de fitness por generación.
               Ej: historial[gen][i] = (f1, f2)
    """
    with open(ruta, "w") as f:
        for gen, pop_fitness in enumerate(historial):
            f.write(f"# gen = {gen}\n")
            for f1, f2 in pop_fitness:
                f.write(f"{f1:.6f}\t{f2:.6f}\n")
            f.write("\n")

def guardar_all_popm(historial, ruta="v2_all_popm.out"):
    with open(ruta, "w") as f:
        for pop_fitness in historial:
            for f1, f2 in pop_fitness:
                f.write(f"{f1:.6e}\t{f2:.6e}\t0.000000e+00\n")



if __name__ == "__main__":
    print("\n=== Ejecutando MOEA/D  ===")
    pop, fit, z, historial = ejecutar_moead(N=40, T=10, generaciones=100)

    guardar_final_pop(fit)
    guardar_all_pop(historial)
    guardar_all_popm(historial)

    print("Archivos generados:")
    print(" - final_pop.out")
    print(" - all_pop.out")
    print(" - all_popm.out")
