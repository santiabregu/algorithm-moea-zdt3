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