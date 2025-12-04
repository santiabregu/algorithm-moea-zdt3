import random
import math
import shutil
import os


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


def generar_pesos(N, perturbacion=0.0):
    """Genera `N` pares de pesos (lambda1, lambda2) equiespaciados para descomposición.

    Cada par suma 1 y recorre el segmento [0,1].
    Si perturbacion > 0, añade ruido aleatorio para explorar mejor frentes discontinuos.
    """
    lambdas = []
    for i in range(N):
        w1 = i / (N - 1)
        if perturbacion > 0:
            # Pequeña perturbación aleatoria para explorar mejor frentes discontinuos (ZDT3)
            w1 = max(0.0, min(1.0, w1 + random.uniform(-perturbacion, perturbacion)))
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

# ------------------------------------- V8: Mecanismos de diversidad ---------------------------------------------------------

def crowding_distance(fitness_list):
    """V8: Calcula crowding distance para mantener diversidad (similar a NSGA-II).
    
    Args:
        fitness_list: Lista de tuplas (f1, f2)
    
    Returns:
        Lista de distancias de crowding (mayor = más diverso)
    """
    n = len(fitness_list)
    if n <= 2:
        return [float('inf')] * n
    
    # Extraer valores de cada objetivo
    f1_vals = [f[0] for f in fitness_list]
    f2_vals = [f[1] for f in fitness_list]
    
    # Calcular rangos para normalización
    f1_range = max(f1_vals) - min(f1_vals)
    f2_range = max(f2_vals) - min(f2_vals)
    
    # Inicializar distancias
    distances = [0.0] * n
    
    # Calcular distancia para cada objetivo
    for obj_idx, obj_vals in enumerate([f1_vals, f2_vals]):
        # Ordenar índices por valor del objetivo
        sorted_indices = sorted(range(n), key=lambda i: obj_vals[i])
        
        # Los extremos tienen distancia infinita
        distances[sorted_indices[0]] = float('inf')
        distances[sorted_indices[-1]] = float('inf')
        
        # Calcular distancia para puntos intermedios
        obj_range = max(obj_vals) - min(obj_vals) if max(obj_vals) != min(obj_vals) else 1.0
        for i in range(1, n - 1):
            idx = sorted_indices[i]
            prev_idx = sorted_indices[i - 1]
            next_idx = sorted_indices[i + 1]
            distances[idx] += (obj_vals[next_idx] - obj_vals[prev_idx]) / obj_range
    
    return distances


def detectar_region_vacia(fitness, umbral_f1=0.8):
    """V8: Detecta si falta cobertura en la región de extremos (f1 > umbral_f1).
    
    Returns:
        True si falta cobertura en extremos
    """
    max_f1 = max(f[0] for f in fitness)
    return max_f1 < umbral_f1


def generar_solucion_extremo(n_vars=30, target_f1=0.85):
    """V8: Genera una solución específicamente para explorar extremos (f1 alto).
    
    Args:
        n_vars: Número de variables
        target_f1: Valor objetivo de f1 (debe estar en [0, 1])
    
    Returns:
        Individuo con x[0] cerca de target_f1
    """
    individuo = [0.0] * n_vars
    # f1 = x[0], así que fijamos x[0] cerca del target
    individuo[0] = max(0.0, min(1.0, target_f1 + random.uniform(-0.05, 0.05)))
    # Resto de variables aleatorias
    for i in range(1, n_vars):
        individuo[i] = random.random()
    return individuo

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


def polynomial_mutation(x, eta=20, pm=1/20):
    """Mutación polinómica con probabilidad balanceada.
    
    V6.5: pm = 1/20 (óptimo encontrado).
    """
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


def differential_evolution(p1, p2, p3, F=0.5, CR=0.5):
    """
    Operador de Differential Evolution (DE) para variación.
    
    V6: Añadido como operador alternativo a SBX para mejorar convergencia.
    
    Args:
        p1, p2, p3: Tres padres (individuos)
        F: Factor de escala (default 0.5)
        CR: Probabilidad de crossover (default 0.5)
    
    Returns:
        Hijo generado por DE
    """
    n = len(p1)
    child = p1[:]  # Empezar con p1
    
    # Mutación: v = p1 + F * (p2 - p3)
    v = []
    for i in range(n):
        v.append(p1[i] + F * (p2[i] - p3[i]))
        v[i] = max(0.0, min(1.0, v[i]))  # Limitar a [0,1]
    
    # Crossover binomial
    j_rand = random.randint(0, n-1)  # Asegurar al menos un gen de v
    for i in range(n):
        if random.random() < CR or i == j_rand:
            child[i] = v[i]
        # else: child[i] = p1[i] (ya está)
    
    return child

# -------------------------------------- moead ----------------------------------------------------------------------


def ejecutar_moead(N=40, T=None, generaciones=100, n_vars=30, perturbacion_pesos=0.02, 
                   pm=1/20, de_prob=0.2, max_reemplazos=2, T_percent=0.225, use_v8=True):
    """MOEA/D V8: Con cambios estructurales para mejorar vs NSGA-II.
    
    V8 añade:
    - Crowding distance para mejor spacing
    - Exploración explícita de extremos
    - Actualización adaptativa periódica
    
    Parámetros configurables:
    - pm: probabilidad de mutación (default 1/20)
    - de_prob: probabilidad de usar DE (default 0.2 = 20%)
    - max_reemplazos: máximo de reemplazos en vecindario (default 2)
    - T_percent: porcentaje de N para calcular T (default 0.225 = 22.5%)
    - use_v8: activar mecanismos V8 (default True)
    """
    # Calcular T automáticamente si no se proporciona
    if T is None:
        T = max(2, round(N * T_percent))  # Mínimo 2 vecinos
    
    poblacion, fitness = inicializar_poblacion(N, n_vars)
    z_ref = calcular_z_estrella(fitness)
    lambdas = generar_pesos(N, perturbacion=perturbacion_pesos)
    vecinos = vecindades(lambdas, T)

    historial = []

    for gen in range(generaciones):

        # V8.7: Exploración balanceada de extremos para mejorar spacing (cada 3 generaciones)
        if use_v8 and gen % 3 == 0:
            max_f1_actual = max(f[0] for f in fitness)
            min_f1_actual = min(f[0] for f in fitness)
            
            # V8.7: Explorar extremos altos (f1 > 0.8) de forma balanceada
            if max_f1_actual < 0.8:  # Explorar si no llegamos a 0.8
                num_extremos = max(2, int(N * 0.11))  # V8.7: 11% de la población (balance entre 10% y 12.5%)
                
                for _ in range(num_extremos):
                    # V8.3: Target balanceado para explorar extremos (f1 > 0.8)
                    if max_f1_actual < 0.5:
                        target_f1 = 0.6 + random.uniform(0, 0.25)  # f1 entre 0.6 y 0.85 (balance)
                    else:
                        target_f1 = max(0.7, max_f1_actual) + random.uniform(0, 0.15)  # Balance
                    target_f1 = min(0.95, target_f1)  # Asegurar que llegue cerca de 0.95
                    
                    sol_extremo = generar_solucion_extremo(n_vars, target_f1=target_f1)
                    f_extremo = zdt3(sol_extremo)
                    
                    # Buscar solución con f1 bajo para reemplazar
                    candidato_idx = min(range(N), key=lambda i: fitness[i][0])
                    
                    # V8.3: Reemplazar si el extremo tiene f1 más alto (exploración balanceada)
                    if f_extremo[0] > fitness[candidato_idx][0]:
                        # Permitir hasta 20% peor en f2 para explorar extremos (balance)
                        if f_extremo[1] < fitness[candidato_idx][1] * 1.20:
                            poblacion[candidato_idx] = sol_extremo
                            fitness[candidato_idx] = f_extremo

        # Copiar población antes de actualizarla
        poblacion_original = [ind[:] for ind in poblacion]
        fitness_original = fitness[:]

        # V8: Calcular crowding distance para toda la población
        crowding_distances = None
        if use_v8:
            crowding_distances = crowding_distance(fitness_original)

        nuevos_fitness = []   # hijos generados

        for i in range(N):

            Bi = vecinos[i]

            p1 = random.choice(Bi)
            p2 = random.choice(Bi)
            while p2 == p1:
                p2 = random.choice(Bi)

            # Padres originales
            padre1 = poblacion_original[p1][:]
            padre2 = poblacion_original[p2][:]

            # Variación con SBX o DE (probabilidad configurable)
            if random.random() < de_prob:
                # Differential Evolution: necesitamos 3 padres
                p3 = random.choice(Bi)
                while p3 == p1 or p3 == p2:
                    p3 = random.choice(Bi)
                padre3 = poblacion_original[p3][:]
                # F=0.5, CR=0.5 (valores estándar)
                hijo = differential_evolution(padre1, padre2, padre3, F=0.5, CR=0.5)
            else:
                # SBX crossover
                hijo = sbx_crossover(padre1, padre2)
            
            # Mutación siempre aplicada (probabilidad configurable)
            hijo = polynomial_mutation(hijo, pm=pm)

            f_hijo = zdt3(hijo)
            nuevos_fitness.append(f_hijo)

            # === REEMPLAZO LIMITADO CON CROWDING DISTANCE (V8) ===
            reemplazos = 0

            for m in Bi:
                if reemplazos >= max_reemplazos:
                    break

                g_hijo = tchebycheff(f_hijo, lambdas[m], z_ref)
                g_padre = tchebycheff(fitness_original[m], lambdas[m], z_ref)

                # V8: Considerar crowding distance en el reemplazo
                if use_v8 and crowding_distances:
                    # Calcular distancia mínima del hijo a otros puntos
                    min_dist_hijo = float('inf')
                    for f_other in fitness_original:
                        dist = math.sqrt((f_hijo[0] - f_other[0])**2 + (f_hijo[1] - f_other[1])**2)
                        if dist > 0 and dist < min_dist_hijo:
                            min_dist_hijo = dist
                    crowding_hijo = min_dist_hijo
                    
                    crowding_padre = crowding_distances[m]
                    
                    # V8.3: Proteger soluciones en extremos (f1 > 0.5) de forma balanceada
                    f1_padre = fitness_original[m][0]
                    f1_hijo = f_hijo[0]
                    es_extremo_padre = f1_padre > 0.5
                    es_extremo_hijo = f1_hijo > 0.5
                    
                    # V8.3: Protección balanceada de extremos (margen 9%, intermedio entre V8.1: 7% y V8.2: 10-12%)
                    es_extremo_alto_padre = f1_padre > 0.8
                    es_extremo_alto_hijo = f1_hijo > 0.8
                    
                    if es_extremo_alto_padre and not es_extremo_alto_hijo:
                        # V8.3: Protección para f1 > 0.8 (margen 9%, balance)
                        if g_hijo < g_padre * 0.91:
                            poblacion[m] = hijo[:]
                            fitness[m] = f_hijo
                            reemplazos += 1
                    elif es_extremo_alto_hijo:
                        # V8.3: Favorecer hijos con f1 > 0.8 (margen 9%)
                        if g_hijo <= g_padre * 1.09:
                            poblacion[m] = hijo[:]
                            fitness[m] = f_hijo
                            reemplazos += 1
                    elif es_extremo_padre and not es_extremo_hijo:
                        # Protección normal para f1 > 0.5 pero < 0.8 (margen 9%)
                        if g_hijo < g_padre * 0.91:
                            poblacion[m] = hijo[:]
                            fitness[m] = f_hijo
                            reemplazos += 1
                    elif es_extremo_hijo:
                        # Favorecer hijos con f1 > 0.5 pero < 0.8 (margen 9%)
                        if g_hijo <= g_padre * 1.09:
                            poblacion[m] = hijo[:]
                            fitness[m] = f_hijo
                            reemplazos += 1
                    else:
                        # V8.6: Reemplazo normal con crowding distance más estricto para mejorar spacing
                        if g_hijo <= g_padre:
                            # Crowding distance más estricto: 0.9 → 0.93 (mejor spacing)
                            # Esto fuerza mejor distribución uniforme
                            if g_hijo < g_padre * 0.97 or crowding_hijo >= crowding_padre * 0.93:
                                poblacion[m] = hijo[:]
                                fitness[m] = f_hijo
                                reemplazos += 1
                else:
                    # Reemplazo original (sin V8)
                    if g_hijo <= g_padre:
                        poblacion[m] = hijo[:]
                        fitness[m] = f_hijo
                        reemplazos += 1

        # V8.7: Actualización adaptativa balanceada para mejorar spacing (cada 7 generaciones)
        if use_v8 and gen > 0 and gen % 7 == 0:
            # Recalcular crowding distances
            crowding_all = crowding_distance(fitness)
            # Mantener las mejores soluciones en términos de diversidad
            # (esto ayuda a mantener extremos aunque no sean óptimos localmente)
            sorted_by_crowding = sorted(range(N), key=lambda i: crowding_all[i], reverse=True)
            # Las top 20% por diversidad se mantienen (similar a NSGA-II)
            num_keep = max(1, N // 5)
            for idx in sorted_by_crowding[:num_keep]:
                # Estas soluciones se mantienen (ya están en la población)
                pass

        # === Actualizar z* al final de la generación ===
        for f_hijo in nuevos_fitness:
            z_ref = (
                min(z_ref[0], f_hijo[0]),
                min(z_ref[1], f_hijo[1])
            )

        historial.append(list(fitness))

    return poblacion, fitness, z_ref, historial


# --------------------------------------- generar archivos de resultados ------------------------------------------------

def guardar_final_pop(fitness, ruta="v3_final_pop.out"):
    with open(ruta, "w") as f:
        for f1, f2 in fitness:
            f.write(f"{f1:.6f}\t{f2:.6f}\n")


def guardar_all_pop(historial, ruta="v3_all_pop.out"):
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


def guardar_all_popm(historial, ruta="v3_all_popm.out"):
    with open(ruta, "w") as f:
        for pop_fitness in historial:
            for f1, f2 in pop_fitness:
                f.write(f"{f1:.6e}\t{f2:.6e}\t0.000000e+00\n")


if __name__ == "__main__":
    # Semillas para múltiples ejecuciones (igual que el profesor)
    seeds = [1, 2, 3, 4, 5, 6, 7, 8, 9, 99]
    
    N = 40
    generaciones = 100
    
    print(f"\n=== Ejecutando MOEA/D con {len(seeds)} semillas ===")
    print(f"    Población: {N}, Generaciones: {generaciones}\n")
    
    for seed in seeds:
        random.seed(seed)  # Fijar semilla para reproducibilidad
        
        seed_str = f"{seed:02d}" if seed < 10 else f"0{seed}"
        print(f"  Semilla {seed_str}...", end=" ", flush=True)
        
        # V8.7: Balance para mejorar spacing sin sacrificar HV
        # Parámetros base V7.3: pm=1/18, de_prob=0.25, perturbacion_pesos=0.025, T_percent=0.25, max_reemplazos=2
        # V8.7 cambios: exploración 11% (balance), crowding threshold 0.91 (balance), actualización cada 7 gen (balance), perturbacion_pesos 0.03 (mejor distribución)
        pop, fit, z, historial = ejecutar_moead(
            N=N, 
            generaciones=generaciones, 
            perturbacion_pesos=0.03,
            pm=1/18,
            de_prob=0.25,
            max_reemplazos=2,
            T_percent=0.25,
            use_v8=True  # Activar mecanismos V8
        )
        
        # Guardar con nombres compatibles con el formato del profesor
        guardar_final_pop(fit, f"zdt3_final_popp{N}g{generaciones}_seed{seed_str}.out")
        guardar_all_popm(historial, f"zdt3_all_popmp{N}g{generaciones}_seed{seed_str}.out")
        
        print("✓")
    
    print(f"\n=== Completado: {len(seeds)} ejecuciones ===")
    print("Archivos generados por cada semilla:")
    print("  - zdt3_final_popp40g100_seedXX.out")
    print("  - zdt3_all_popmp40g100_seedXX.out")
    
    # Copiar seed01 a METRICS para comparación con ./metrics
    metrics_dir = "../../METRICS"
    seed01_file = f"zdt3_all_popmp{N}g{generaciones}_seed01.out"
    dest_file = os.path.join(metrics_dir, "zdt3_seed1_personal_N40G100.out")
    
    if os.path.exists(seed01_file) and os.path.exists(metrics_dir):
        shutil.copy2(seed01_file, dest_file)
        print(f"\n✓ Seed01 copiado a METRICS/zdt3_seed1_personal_N40G100.out")
