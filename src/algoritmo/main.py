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


def inicializar_poblacion(N=100, n_vars=30):
    """(Duplicada) Igual que la otra `inicializar_poblacion`: crear población y calcular fitness."""
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
    """Calcula el valor Tchebycheff ponderado para el vector objetivo `f`.

    Usa pesos `lamb` y referencia `z_ref` (z*).
    """
    return max([
        lamb[j] * abs(f[j] - z_ref[j])
        for j in range(2)
    ])

# ------------------------------------- operadores evolutivos ---------------------------------------------------------

def crossover(p1, p2, pc=0.9):
    if random.random() > pc:
        return p1[:]  # sin cruce

    alpha = random.random()  # mezcla aleatoria
    hijo = [alpha*p1[i] + (1-alpha)*p2[i] for i in range(len(p1))]
    return hijo

def mutate(x, pm=0.1, sigma=0.1):
    for i in range(len(x)):
        if random.random() < pm:
            x[i] += random.gauss(0, sigma)
            x[i] = min(1.0, max(0.0, x[i]))  # asegurar rango [0,1]
    return x

# -------------------------------------- moead ----------------------------------------------------------------------

def ejecutar_moead(N=40, T=10, generaciones=100, n_vars=30):
    poblacion, fitness = inicializar_poblacion(N, n_vars)
    z_ref = calcular_z_estrella(fitness)
    lambdas = generar_pesos(N)
    vecinos = vecindades(lambdas, T)

    historial = []  # <-- NUEVO

    for gen in range(generaciones):
        for i in range(N):

            Bi = vecinos[i]
            p1 = random.choice(Bi)
            p2 = random.choice(Bi)

            padre1 = poblacion[p1]
            padre2 = poblacion[p2]

            hijo = crossover(padre1, padre2)
            hijo = mutate(hijo)

            f_hijo = zdt3(hijo)

            z_ref = (min(z_ref[0], f_hijo[0]),
                     min(z_ref[1], f_hijo[1]))

            for m in Bi:
                if tchebycheff(f_hijo, lambdas[m], z_ref) <= tchebycheff(fitness[m], lambdas[m], z_ref):
                    poblacion[m] = hijo
                    fitness[m] = f_hijo

        # GUARDAR FITNESS EN EL HISTORIAL
        historial.append(list(fitness))

        if gen % 10 == 0:
            print(f"Generación {gen} completada.")

    return poblacion, fitness, z_ref, historial

# --------------------------------------- generar archivos de resultados ------------------------------------------------

def guardar_final_pop(fitness, ruta="final_pop.out"):
    with open(ruta, "w") as f:
        for f1, f2 in fitness:
            f.write(f"{f1:.6f}\t{f2:.6f}\n")

def guardar_all_pop(historial, ruta="all_pop.out"):
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

def guardar_all_popm(historial, ruta="all_popm.out"):
    with open(ruta, "w") as f:
        for pop_fitness in historial:
            for f1, f2 in pop_fitness:
                f.write(f"{f1:.6f}\t{f2:.6f}\n")


if __name__ == "__main__":
    print("\n=== Ejecutando MOEA/D pequeño de prueba ===")
    pop, fit, z, historial = ejecutar_moead(N=100, T=10, generaciones=200)

    guardar_final_pop(fit)
    guardar_all_pop(historial)
    guardar_all_popm(historial)

    print("Archivos generados:")
    print(" - final_pop.out")
    print(" - all_pop.out")
    print(" - all_popm.out")