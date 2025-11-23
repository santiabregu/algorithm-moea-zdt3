# Proyecto MOEA/D – ZDT3  
### Versión 1 del código (resumen técnico)

---

## 1. Estructura del código

La primera versión del código implementa una versión funcional y simplificada de MOEA/D.  
Todo está implementado en `main.py`, incluyendo:

- Inicialización de población
- Evaluación con el problema ZDT3
- Vectores de pesos y vecindarios
- Agregación Tchebycheff
- Operadores evolutivos (SBX + Mutación polinómica)
- Bucle evolutivo principal
- Generación de archivos de resultados compatibles con las métricas del profesor

```
src/
└── algoritmo/
    └── main.py
```

---

## 2. Representación de individuos

Cada solución se representa como:

```
x = (x₁, x₂, …, x₃₀),   xᵢ ∈ [0,1]
```

La población inicial consta de **40 individuos** (versión 1).

---

## 3. Problema ZDT3

Formulación incluida en el código:

```
f₁(x) = x₁
g(x) = 1 + (9/29)(Σ xᵢ de i=2 a 30)
h(x) = 1 - sqrt(f₁(x) / g(x)) - (f₁(x)/g(x)) * sin(10π f₁(x))
f₂(x) = g(x) * h(x)
```

El código calcula `f1` y `f2` para cada individuo.

---

## 4. Descomposición MOEA/D

### 4.1 Vectores de pesos

Generados equiespaciados:
```
λ₁⁽ⁱ⁾ = i / (N-1)
λ₂⁽ⁱ⁾ = 1 - λ₁⁽ⁱ⁾
```

### 4.2 Vecindarios

Se calcula distancias entre λ⁽ⁱ⁾ y λ⁽ʲ⁾ y se seleccionan los **10 vecinos más cercanos**.

---

## 5. Función de agregación Tchebycheff

```
g_te = max( λ₁|f₁ − z₁*| , λ₂|f₂ − z₂*| )
```

donde `z*` se actualiza dinámicamente con los mínimos observados.

---

## 6. Operadores evolutivos implementados

### 6.1 SBX (Simulated Binary Crossover)

Versión estándar, η = 20  
Probabilidad de cruce: `pc = 0.9`

### 6.2 Mutación polinómica

Probabilidad: `pm = 1/30`  
Parámetro: η = 20

---

## 7. Bucle evolutivo principal

Parámetros de esta versión:

- **N = 40** individuos  
- **T = 10** vecinos  
- **100 generaciones**

Cada generación:
1. Se seleccionan dos vecinos
2. Se genera un hijo
3. Se evalúa
4. Se compara mediante Tchebycheff
5. Se actualiza la población en los subproblemas donde mejore

---

## 8. Ficheros generados (versión 1)

El algoritmo produce:

### `final_pop.out`
Solo las soluciones finales.

### `all_pop.out`
Todas las generaciones con comentarios `# gen =`.

### `all_popm.out`
Todas las soluciones formato métrico:

```
f1    f2    0.000000e+00
```

Este archivo es el que se usa en **METRICS** del profesor.

---

## 9. Estado actual (versión 1 del código)

- MOEA/D completamente funcional  
- Evaluación ZDT3 correcta  
- Operadores de variación implementados  
- Descomposición + vecindarios implementados  
- Archivos compatibles para métricas generados  
- Listo para comparar con NSGA-II

Pendiente para versión 2:
- Gráficas de evolución
- Métricas Hypervolume, Spacing, Coverage
- Comparación NSGA-II vs MOEA/D
- Ajuste de parámetros

** V1 Descripción técnica del gráfico de Hypervolume **

La figura muestra la evolución del hypervolume (HV) obtenido por el MOEA/D durante 100 generaciones.

Aunque la tendencia general es ascendente —lo cual indica que el algoritmo mejora progresivamente su aproximación al frente de Pareto— la curva presenta varios tramos donde el HV permanece prácticamente constante e incluso pequeños retrocesos locales alrededor de las generaciones 35–45 y 55–60.

Estas irregularidades sugieren que el algoritmo experimenta dificultades temporales para mejorar determinadas regiones del frente, lo que es coherente con la naturaleza discontinua del frente ZDT3 y la sensibilidad del MOEA/D a la elección de vecindarios y pesos.

A partir de la generación 70, el incremento en HV se vuelve muy lento, lo que indica que el algoritmo ha alcanzado una zona de cuasi-estancamiento: todavía mejora, pero de forma marginal. Este comportamiento es habitual en implementaciones básicas de MOEA/D debido a la falta de mecanismos explícitos de diversidad global.

En conjunto, el gráfico confirma que la convergencia es razonablemente buena, pero el proceso no es uniforme ni completamente estable, evidenciando margen de mejora en la exploración del espacio de soluciones.

** V1 Descripción técnica del gráfico de Spacing **

La figura registra la evolución del Spacing, métrica que evalúa la uniformidad en la distribución de las soluciones sobre el frente.

En las primeras ~30 generaciones el valor del Spacing muestra picos muy pronunciados (incluyendo valores alrededor de 0.4), lo que refleja una fuerte irregularidad en la dispersión de las soluciones. Esto indica que, en esta fase inicial, el algoritmo genera clusters y zonas vacías en el frente, un comportamiento no deseado pero frecuente antes de que el proceso evolutivo se estabilice.

Tras esa fase inicial, el Spacing disminuye y se mantiene en valores más bajos, aunque sigue presentando oscilaciones notables en lugar de estabilizarse por completo. Esto evidencia que el algoritmo no logra producir una distribución perfectamente uniforme, probablemente debido a:

la estructura fija de vecindarios del MOEA/D,

la falta de un operador de diversidad explícito,

la complejidad del frente discontinuo de ZDT3.

Aunque la tendencia general es positiva (menor Spacing → mejor uniformidad), la fluctuación persistente indica que la uniformidad no es totalmente estable y depende fuertemente de las variaciones locales de los subproblemas.

# Razones porque podria no ser uniforme :
La no-uniformidad de tu algoritmo se debe principalmente a:

(1) Pesos lineales insuficientes para un frente discontinuo → el problema principal.
(2) Vecindarios demasiado pequeños → surgen clusters.
(3) Operadores evolutivos demasiado conservadores → poca exploración.
(4) Reemplazo local del MOEA/D básico → sin diversidad global.
(5) Población pequeña → no alcanza todas las zonas del frente. 