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

# Razones por las que mi MOEA/D no distribuye uniformemente los puntos

La distribución no uniforme de los puntos en el frente obtenido por mi implementación de MOEA/D se explica por varios factores relacionados con la configuración del algoritmo y con la naturaleza del problema ZDT3.

## 1. Pesos lineales poco adecuados para un frente discontinuo

El algoritmo genera pesos equiespaciados del tipo:

λᵢ = ( i/(N−1), 1 − i/(N−1) )

Este esquema funciona bien en frentes convexos y continuos, pero ZDT3 tiene 5 segmentos separados.  
Por eso, algunas regiones quedan sin representación y el algoritmo no explora los huecos del frente.

## 2. Vecindarios demasiado cerrados (T = 10)

Los vecindarios se definen como los T pesos más cercanos.  
Con N = 40 y T = 10, cada subproblema solo se mezcla con un grupo pequeño.

Esto causa:

- aparición de clusters de soluciones,
- áreas sin cubrir,
- falta de diversidad global.

## 3. Baja variación genética

- SBX usa η = 20, generando hijos muy similares a los padres,
- Mutación polinómica tiene una probabilidad reducida pm = 1/30.

Consecuencia directa:

La exploración del espacio de búsqueda es limitada y las soluciones tienden a concentrarse.

## 4. Reemplazo únicamente local

MOEA/D reemplaza soluciones solo dentro del vecindario:

si g_hijo ≤ g_padre ⇒ hijo reemplaza padre

Este mecanismo fomenta convergencia, pero no protege la diversidad global del frente.  
De ahí que el hypervolume mejore pero el spacing permanezca irregular.

## 5. Tamaño poblacional insuficiente para ZDT3

El frente ZDT3 requiere muchos puntos para cubrir bien sus múltiples segmentos.  
Con solo N = 40:

No hay suficientes subproblemas para formar una muestra uniforme del frente completo.

## Conclusión

Mi MOEA/D converge correctamente hacia el frente (lo confirma el hipervolumen), pero no logra una distribución uniforme debido a:

- pesos lineales en un frente discontinuo,
- vecindarios demasiado estrechos,
- operadores poco exploratorios,
- reemplazo local sin mecanismos globales de diversidad,
- población pequeña.


------------------------------------------------------------------------------------------------------------------------------

# *Version de codigo 2*

Cambiar el vecindario a T=15 no arregla el problema.
De hecho, lo empeora:

Convergencia más lenta,

Diversidad casi inexistente,

## Cambio 1

En la versión previa del algoritmo (v1), el punto de referencia 
𝑧
∗
z
∗
 —que representa los mínimos conocidos de cada objetivo— se actualizaba dentro del bucle de reemplazo local, es decir, cada vez que un hijo era evaluado. Esta estrategia introduce un problema:
a medida que se recorren los vecinos, el valor de 
𝑧
∗
z
∗
 cambia durante la misma generación, lo que provoca criterios de comparación inconsistentes entre diferentes soluciones de la misma iteración. El resultado es un comportamiento inestable, pérdida de diversidad y oscilaciones en métricas como spacing e hypervolume.

En la versión actual (v2), 
𝑧
∗
z
∗
 se actualiza únicamente una vez por generación, después de evaluar a los nuevos hijos, manteniendo un criterio homogéneo durante toda la iteración. Con esto se consigue un proceso de selección más estable y una evolución más suave del frente de Pareto.

imagenes despues de cambio z* 

El algoritmo ha mejorado notablemente respecto a la versión anterior: el spacing muestra una distribución mucho más estable y uniforme, similar a la del profesor, lo que indica que la diversidad local ahora se gestiona correctamente. Sin embargo, el hypervolume aún crece de forma menos suave y alcanza valores claramente inferiores, señal de que el algoritmo no está cubriendo adecuadamente toda la extensión del frente de Pareto, especialmente en las zonas extremas. En conjunto, la distribución ya es razonable, pero la convergencia global sigue siendo insuficiente, y el algoritmo aún no consigue aproximarse al mismo nivel de calidad que el de referencia:

Reference point for hypervolume calculation
ref[1]=0.9715823000
ref[2]=4.1410760000 -> Los valores del hipervolumen y su referencia dicen cosas importantes sobre el algoritmo.
En mi caso indican que:

Mi algoritmo no explora suficientemente las zonas extremas del frente, especialmente valores grandes de f2.
Por eso el punto de referencia automático es más pequeño.
Y por ello mi hypervolume alcanza valores más modestos.
El algoritmo del profesor cubre un rango mucho más amplio, lo que indica una mejor exploración del espacio de búsqueda.
Tambien: Tu gráfico final está mal porque la última generación ha perdido la diversidad completamente, de modo que aunque tienes una población de 40, solo aparecen 4 soluciones únicas. Esto no es normal en MOEA/D y confirma que todavía quedan problemas en los operadores evolutivos y/o en la política de reemplazo.
Otro problema importante: En la última generación de mi MOEA/D se observa un fenómeno indeseado: solo aparecen unos pocos puntos en el frente final, mientras que en el algoritmo del profesor la población final mantiene los 40 individuos bien distribuidos en todo el frente de Pareto. Esto indica que el algoritmo no está conservando diversidad al final del proceso, y que durante las últimas iteraciones muchos individuos están colapsando hacia unas pocas zonas del frente.

Este comportamiento suele deberse a una o varias de las siguientes causas:

Actualización de vecinos demasiado agresiva
Al reemplazar muchos vecinos por el mismo hijo, toda la población puede converger hacia solo unas pocas soluciones, destruyendo la diversidad.

Operadores de variación poco exploratorios
Una mutación demasiado baja o un crossover demasiado conservador puede hacer que las soluciones se vuelvan casi idénticas.

Referencia z* que se actualiza demasiado, empujando todas las soluciones hacia un único extremo del frente.

Número de vecinos T demasiado grande
Cuanto mayor es T, más individuos se reemplazan por el mismo hijo ⇒ más rápido colapsa la diversidad.

Falta de elitismo real
El algoritmo no garantiza que los mejores puntos diversos se mantengan; algunos subproblemas dejan de tener representantes válidos.

En resumen:
Mi algoritmo converge, pero pierde diversidad, mientras que el del profesor mantiene una representación uniforme del frente. Solucionar esto implica actuar sobre la presión de reemplazo, la mutación y la vecindad.

-------------------------------------------------------------------------------------------------------

# *Version 3*

Cambios principales a implementar en la Versión 3
1. Reducir el tamaño de vecindario (T)

Cambio: bajar T de 15 a valores recomendados (8).

Razón: con T demasiado grande, un solo hijo reemplaza demasiados subproblemas, provocando pérdida severa de diversidad y que la población colapse en pocas zonas del frente (pocos puntos en la última generación).

2. Ajustar el reemplazo para que no sea tan agresivo

Cambio: limitar cuántos vecinos puede reemplazar un hijo, o aumentar los criterios para sustituir.

Razón: el reemplazo actual permite que un hijo sustituya hasta el 40% de la población, lo cual destruye rápidamente la diversidad y produce un frente final incompleto.

3. Revisar la generación de pesos (lambdas)

Cambio: usar una distribución de pesos mejor adaptada a funciones no convexas (como ZDT3), o aumentar el número de pesos.

Razón: los pesos lineales uniformes no cubren bien las zonas disjuntas y curvas del frente de ZDT3, causando huecos y mala exploración.

1) 
En esta versión se introdujeron dos ajustes clave en la dinámica interna de MOEA/D.
Primero, se modificó el parámetro de vecindad T, fijándolo en 8, lo que corresponde al 20 % de los vectores de peso. Este cambio reduce el tamaño de cada vecindario, haciendo que cada subproblema interactúe con un grupo más pequeño y coherente de vecinos. La motivación es que un T más grande puede provocar que las actualizaciones se propaguen demasiado rápido por toda la población, reduciendo diversidad y haciendo que distintos subproblemas terminen explorando regiones similares del espacio objetivo. Con T=8 se buscó equilibrar convergencia y diversidad, limitando la presión de reemplazo entre regiones del frente.

En segundo lugar, se modificó el criterio de reemplazo, retrasando la actualización del punto de referencia 
𝑧
\*
z
\*
 hasta el final de cada generación. En versiones anteriores, 
𝑧
\*
z
\*
 se actualizaba inmediatamente tras evaluar cada hijo, lo que hacía el reemplazo excesivamente agresivo: los subproblemas tendían a reemplazar a los individuos actuales con hijos generados en la misma zona, provocando la pérdida de diversidad y, en las últimas generaciones, la desaparición de una parte importante del frente final. Al actualizar 
𝑧
\*
z
\*
 solo una vez por generación, el reemplazo se vuelve más estable y menos reactivo, evitando cambios bruscos durante la generación.

Los resultados reflejan claramente el efecto positivo de estos dos ajustes.
El hipervolumen muestra una curva mucho más progresiva y estable, alcanzando valores significativamente superiores a los obtenidos en versiones anteriores. Del mismo modo, el spacing presenta oscilaciones más suaves y valores promedio más bajos, lo que indica una mejor distribución de los puntos en el frente Pareto. Finalmente, la generación final ya no colapsa: en lugar de producir solo unas pocas soluciones, ahora devuelve un conjunto amplio de puntos a lo largo de varios segmentos del frente ZDT3, manteniendo diversidad y estructura.


-------------------------------------------------------------------------------------------------------

# *Version 4*

Ahora se generan 10 ficheros para N = 40 y generaciones = 100, con diferentes semillas aleatorias (seed01-seed09, seed099) para obtener resultados estadísticamente significativos.

## Metodología de cálculo de métricas

Todas las métricas se calculan usando el software `./metrics` proporcionado por el profesor. El flujo es:

```
./metrics (software del profesor)
    ↓
hypervol.out, spacing.out, cs.out, extent.out, etc.
    ↓
Script Python (solo automatiza y promedia resultados de ./metrics)
    ↓
moead_hv_avg.out, nsga2_hv_avg.out
    ↓
Gnuplot (visualización)
```

El script `METRICS/utils/hypervolume_avg_metrics.py`:
1. Lee TODOS los archivos de ambos algoritmos
2. Calcula el punto de referencia común (peor f1 y f2 de todos)
3. Ejecuta `./metrics` para cada archivo con ese punto de referencia
4. Promedia los resultados por generación

**Importante:** El script Python NO implementa su propio cálculo de hipervolumen. Solo automatiza la ejecución de `./metrics` y promedia los resultados.

## Comparación con NSGA-II del profesor

Para una comparación justa, se calculó un **punto de referencia común** usando el peor f1 y f2 de TODOS los archivos (tanto MOEA/D como NSGA-II):

```
Punto de referencia común:
ref_x = 1.0095808500
ref_y = 6.2944785700
```

### Resultados de Hipervolumen (promedio de 10 semillas)

| Generación | MOEA/D | NSGA-II | Ganador |
|------------|--------|---------|---------|
| Gen 1      | 3.462  | 2.931   | MOEA/D  |
| Gen 100    | 6.261  | 6.234   | MOEA/D  |

**Diferencia final: +0.027 a favor de MOEA/D**

### Comparación detallada para una semilla (seed01)

| Métrica | MOEA/D | NSGA-II | Interpretación |
|---------|--------|---------|----------------|
| **Hypervolume (Gen 100)** | 6.385 | 6.257 | MOEA/D +2.0% mejor |
| **Spacing (Gen 100)** | 0.0431 | 0.0114 | NSGA-II mejor distribución |
| **Extent (f1)** | 0.752 | 0.798 | NSGA-II cubre más rango |
| **CS (cobertura)** | 0.00 | 0.875 | Mixto |

### Observaciones del frente de Pareto

Al visualizar la animación comparativa de ambos algoritmos, se observa que:

1. **MOEA/D (puntos azules)** no genera soluciones después de f1 ≈ 0.8
2. **NSGA-II (puntos rojos)** sí alcanza valores de f1 hasta ≈ 0.85

El frente de Pareto de ZDT3 tiene **5 segmentos discontinuos**. El último segmento está aproximadamente en f1 ∈ [0.82, 1.0]. Mi algoritmo MOEA/D no está encontrando bien ese último segmento.

### Análisis de la limitación

Esta limitación se debe a los **pesos lineales equiespaciados**:

```
λᵢ = (i/(N−1), 1 − i/(N−1))
```

Este esquema no cubre adecuadamente los 5 segmentos discontinuos de ZDT3, especialmente el último segmento donde f1 > 0.8.

### Conclusión V4

| ✅ Mejoras logradas | ⚠️ Limitación pendiente |
|---------------------|------------------------|
| Hypervolume superior a NSGA-II | Falta explorar f1 > 0.8 |
| Spacing más estable | Último segmento ZDT3 vacío |
| 40 puntos en frente final | Extent menor que NSGA-II |
| Ejecución con 10 semillas | |

**Mi MOEA/D converge mejor en las regiones que cubre, pero NSGA-II explora mejor los extremos del frente.**

El algoritmo es competitivo con NSGA-II en términos de hipervolumen global, pero para mejorar la cobertura del último segmento sería necesario:
- Usar una distribución de pesos adaptada a frentes discontinuos
- Aumentar el tamaño de la población
- Implementar mecanismos de exploración adicionales

----------------------------------------------------------------------------------------------------------
V5


## Objetivo

Mejorar las métricas donde MOEA/D perdía frente a NSGA-II:
- **Coverage Set**: 87.5% de MOEA/D era dominado por NSGA-II
- **Spacing**: 0.043 vs 0.011 (NSGA-II mejor)
- **Extent**: No cubría f1 > 0.8

## Cambios implementados

### 1. Aumento de la probabilidad de mutación

```python
# V4: pm = 1/30 ≈ 0.033
# V5: pm = 1/15 ≈ 0.067 (el doble)
def polynomial_mutation(x, eta=20, pm=1/15):
```

**Razón:** Una mutación más frecuente aumenta la exploración del espacio de búsqueda, permitiendo escapar de óptimos locales y explorar regiones no cubiertas del frente.

### 2. Perturbación de pesos para frentes discontinuos

```python
def generar_pesos(N, perturbacion=0.05):
    for i in range(N):
        w1 = i / (N - 1)
        # Añadir ruido ±5% para explorar mejor
        w1 = max(0.0, min(1.0, w1 + random.uniform(-0.05, 0.05)))
        w2 = 1 - w1
        lambdas.append((w1, w2))
```

**Razón:** Los pesos lineales uniformes no cubren bien los 5 segmentos discontinuos de ZDT3. La perturbación permite que algunos subproblemas exploren las zonas entre segmentos y los extremos (f1 > 0.8).

### 3. Vecindario más grande

```python
# V4: T = 10 (25% de N)
# V5: T = 12 (30% de N)
ejecutar_moead(N=40, T=12, ...)
```

**Razón:** Un vecindario más grande permite mayor intercambio de información entre subproblemas, mejorando la diversidad global sin sacrificar demasiada convergencia.

## Resumen de parámetros V5

| Parámetro | V4 | V5 | Justificación |
|-----------|----|----|---------------|
| **pm** | 1/30 | 1/15 | Mayor exploración |
| **T** | 10 | 12 | Mejor diversidad |
| **Perturbación pesos** | 0 | 0.05 | Cubrir frentes discontinuos |
| **max_reemplazos** | 2 | 2 | Sin cambio |
| **η (SBX y mutación)** | 20 | 20 | Sin cambio |

## Resultados obtenidos V5 (parámetros originales)

### Comparación V5 vs NSGA-II (promedio 10 seeds, Gen 100)

| Métrica | MOEA/D V5 | NSGA-II | Resultado |
|---------|-----------|---------|-----------|
| **Hypervolume** | 6.234 | 6.234 | ✅ Igual (diferencia +0.0009) |
| **Spacing** | 0.0412 | 0.0114 | ⚠️ NSGA-II mejor (3.6x mejor) |
| **CS2 (% V5 dom por NSGA-II)** | 50-80% | - | ❌ **MUY MALO** |

### Problemas detectados

1. **Coverage Set crítico**: Entre 50-80% de las soluciones de MOEA/D están siendo dominadas por NSGA-II durante toda la ejecución. Esto indica que el algoritmo no está convergiendo adecuadamente en muchas zonas del frente.

2. **Spacing con picos**: Aunque el spacing promedio mejoró ligeramente (0.0412 vs 0.0431 en V4), presenta picos pronunciados en generaciones 5-8 y 47-50 (valores de 0.09-0.098), indicando pérdida temporal de uniformidad.

3. **Hypervolume igual**: El HV final es prácticamente idéntico a NSGA-II, pero esto no compensa el mal Coverage Set.

### Análisis de las causas

Los parámetros de V5 original eran demasiado agresivos en exploración:

- **T=12 (vecindario grande)**: Aumenta la presión de reemplazo, permitiendo que un solo hijo reemplace muchos subproblemas, reduciendo diversidad y convergencia.
- **Perturbación=0.05**: Demasiado ruido en los pesos causa inestabilidad en la convergencia de algunos subproblemas.
- **max_reemplazos=2**: Permite reemplazos múltiples que pueden propagar soluciones no óptimas.

**Resultado**: El algoritmo explora más pero converge peor, permitiendo que NSGA-II domine muchas soluciones.

## V5 Ajustado (corrección de parámetros)

### Cambios realizados

| Parámetro | V5 original | V5 ajustado | Razón |
|-----------|-------------|-------------|-------|
| **T (vecindario)** | 12 | **10** | Reducir presión de reemplazo |
| **Perturbación pesos** | 0.05 | **0.02** | Menos ruido = convergencia más estable |
| **max_reemplazos** | 2 | **1** | Menos reemplazos agresivos = mejor convergencia |
| **pm (mutación)** | 1/15 | 1/15 | Mantener (exploración necesaria) |

### Objetivo de los ajustes

- **Mejorar Coverage Set**: Reducir el porcentaje de soluciones dominadas por NSGA-II (objetivo: <50%)
- **Reducir picos en Spacing**: Convergencia más estable sin pérdidas temporales de uniformidad
- **Mantener HV competitivo**: No sacrificar el hipervolumen logrado

**Estrategia**: Balance entre exploración (mutación alta) y convergencia (vecindario y perturbación menores).

## Resultados obtenidos V5 Ajustado

### Comparación V5 Ajustado vs V5 Original vs NSGA-II (Gen 100, seed01)

| Métrica | V5 Original | V5 Ajustado | NSGA-II | Mejor |
|---------|-------------|-------------|---------|-------|
| **Hypervolume** | 6.234 | **6.386** | 6.257 | ✅ V5 Ajustado |
| **Spacing** | 0.0412 | **0.0208** | 0.0114 | ✅ V5 Ajustado |
| **CS2 (dom por NSGA-II)** | 80.0% | 92.5% | - | ❌ Empeoró |

### Análisis de resultados

- ✅ **Hypervolume mejoró significativamente**: 6.234 → 6.386 (+2.4%)
- ✅ **Spacing mejoró mucho**: 0.0412 → 0.0208 (sin picos altos)
- ❌ **Coverage Set empeoró**: 80% → 92.5% (más soluciones dominadas)

**Observación importante**: El CS2 muestra una mejora temporal (baja a 35-47% en generaciones 6-10) pero luego sube a 90%+ en las últimas generaciones. Esto sugiere que el algoritmo converge bien inicialmente pero pierde diversidad/convergencia en zonas específicas del frente.

**Conclusión V5 Ajustado**: Los ajustes mejoraron la convergencia global (HV) y la distribución (Spacing), pero el problema de dominancia persiste. La mutación alta (pm=1/15) puede estar generando soluciones que no convergen adecuadamente en algunas regiones del frente.

-------------------------------------------------------------------------------------------------------

# *Version 6*

## Objetivo

Mejorar el Coverage Set que sigue siendo el punto débil del algoritmo, manteniendo las mejoras logradas en Hypervolume y Spacing.

## Cambios planificados

1. **Ajustar probabilidad de mutación**: Reducir de 1/15 a un valor intermedio (1/20 o 1/25) para balancear exploración y convergencia.

2. **Ajustar parámetros SBX**: Modificar η (distribution index) para controlar la exploración del crossover.

3. **Añadir operador adicional**: Implementar un operador de **Differential Evolution (DE)** como alternativa al SBX, que puede mejorar la convergencia en zonas específicas del frente.

## Justificación

El problema principal es que muchas soluciones de MOEA/D son dominadas por NSGA-II (92.5%), lo que indica falta de convergencia en ciertas regiones. Los operadores actuales (SBX + mutación polinómica) pueden no ser suficientes para explorar y converger en todas las zonas del frente discontinuo de ZDT3.

El operador DE puede ayudar porque:
- Genera soluciones más diversas
- Mejora la convergencia en zonas específicas
- Es complementario a SBX (puede usarse alternativamente)

## Cambios implementados V6

### 1. Ajuste de probabilidad de mutación

```python
# V5: pm = 1/15 ≈ 0.067
# V6: pm = 1/20 ≈ 0.05
def polynomial_mutation(x, eta=20, pm=1/20):
```

**Razón**: Balance entre exploración y convergencia. La mutación muy alta (1/15) puede generar soluciones que no convergen bien.

### 2. Operador Differential Evolution (DE)

Nuevo operador añadido como alternativa a SBX:

```python
def differential_evolution(p1, p2, p3, F=0.5, CR=0.5):
    # Mutación: v = p1 + F * (p2 - p3)
    # Crossover binomial con probabilidad CR
```

**Uso**: 30% probabilidad de usar DE, 70% SBX.

**Parámetros**:
- **F = 0.5**: Factor de escala (controla la magnitud de la diferencia)
- **CR = 0.5**: Probabilidad de crossover (controla cuántos genes se toman del vector mutado)

### 3. Resumen de parámetros V6

| Parámetro | V5 Ajustado | V6 | Cambio |
|-----------|-------------|----|--------|
| **pm** | 1/15 | **1/20** | Reducido para mejor convergencia |
| **T** | 10 | 10 | Sin cambio |
| **Perturbación pesos** | 0.02 | 0.02 | Sin cambio |
| **max_reemplazos** | 1 | 1 | Sin cambio |
| **Operador variación** | Solo SBX | **SBX + DE (30%)** | Nuevo |

## Objetivos V6

- ✅ Mejorar Coverage Set (objetivo: <70% dominado por NSGA-II)
- ✅ Mantener HV competitivo (≥6.35)
- ✅ Mantener Spacing bajo (<0.025)
- ✅ Mejorar convergencia en zonas específicas del frente

## Cambio adicional V6.3: Cálculo automático de T

En lugar de fijar T manualmente, ahora se calcula automáticamente como **22.5% de N** (punto medio entre 20-25% recomendado):

```python
if T is None:
    T = max(2, round(N * 0.225))  # Para N=40 → T=9
```

**¿Afecta a los resultados?** Sí, puede afectar:
- **T más pequeño** (9 vs 10): Menos presión de reemplazo, mejor convergencia pero menos diversidad
- **T más grande**: Más diversidad pero puede perder convergencia

Para N=40, el cambio es mínimo (T=9 vs T=10), pero hace el algoritmo más adaptable a diferentes tamaños de población.

## Resultados obtenidos V6

### Comparación V6 vs V5 Ajustado vs NSGA-II (Gen 100, seed01)

| Métrica | V5 Ajustado | V6 | NSGA-II | Mejor |
|---------|-------------|----|---------|-------|
| **Hypervolume** | 6.386 | 6.337 | 6.257 | V5 Ajustado |
| **Spacing** | 0.0208 | 0.0312 | 0.0114 | V5 Ajustado |
| **CS2 (dom por NSGA-II)** | 92.5% | **87.5%** | - | ✅ V6 |

### Análisis de resultados V6

- ✅ **Coverage Set mejoró**: 92.5% → 87.5% (-5%)
- ⚠️ **Hypervolume bajó**: 6.386 → 6.337 (-0.049)
- ⚠️ **Spacing empeoró**: 0.0208 → 0.0312 (+0.0104)
- ⚠️ **Spacing con picos**: Valores de 0.08 en generaciones 3-5

**Observación**: El CS2 muestra una mejora temporal significativa (baja a 40% en generaciones 9-11), pero luego sube a 87.5% en las últimas generaciones. Esto indica que el operador DE ayuda inicialmente pero no mantiene la convergencia a largo plazo.

### Comparación evolutiva

**Promedio 10 seeds (Gen 100)**:
- V6: HV = 6.252
- NSGA-II: HV = 6.236
- **V6 gana por +0.016** ✅

**Conclusión V6**: El operador DE y la mutación ajustada mejoraron ligeramente el Coverage Set, pero a costa de perder HV y Spacing. El algoritmo necesita más ajustes para encontrar el balance óptimo entre exploración y convergencia.

## Variantes V6 probadas (ajuste fino)

Se probaron diferentes combinaciones de parámetros del operador DE para optimizar el Coverage Set:

| Versión | Prob. DE | F | CR | max_reemplazos | HV | Spacing | CS2 | Mejor CS2 |
|---------|----------|---|----|----------------|----|---------|-----|-----------|
| **V6** | 30% | 0.5 | 0.5 | 1 | 6.337 | 0.031 | 87.5% | |
| **V6.1** | 50% | 0.3 | 0.7 | 2 | 6.391 | 0.026 | 100% | ❌ |
| **V6.2** | 40% | 0.4 | 0.6 | 1 | 6.391 | 0.025 | 97.5% | ❌ |
| **V6.3** | **20%** | **0.5** | **0.5** | **1** | **6.329** | **0.026** | **85.0%** | ✅ |

### Análisis de las variantes

- **V6.1 y V6.2**: Aumentar la probabilidad de DE (40-50%) empeora el Coverage Set (97.5-100%). El DE es demasiado exploratorio y no converge bien.

- **V6.3**: Reducir la probabilidad de DE a 20% logra el **mejor Coverage Set (85.0%)**, manteniendo HV y Spacing competitivos.

**Conclusión**: El operador DE debe usarse con moderación (20%) para complementar SBX sin dominar la exploración. Valores estándar (F=0.5, CR=0.5) funcionan mejor que valores ajustados.

### Parámetros finales V6.3

- **T**: Calculado automáticamente como 22.5% de N (T=9 para N=40)
- **pm**: 1/20
- **Perturbación pesos**: 0.02
- **DE**: 20% probabilidad, F=0.5, CR=0.5
- **max_reemplazos**: 1

## Pruebas adicionales de ajuste fino (V6.3 - V6.11)

Se realizaron pruebas adicionales para optimizar el Coverage Set y Spacing, probando diferentes combinaciones de parámetros:

### Resumen de todas las pruebas

| Versión | Cambio principal | HV | Spacing | CS2 | Mejor |
|---------|------------------|----|---------|-----|-------|
| **V6.3** | Base (max_repl=1) | 6.329 | 0.026 | 85.0% | |
| **V6.5** | **max_repl=2** | **6.338** | **0.025** | **82.5%** | ✅ **ÓPTIMA** |
| **V6.6** | max_repl=3 | 6.338 | 0.025 | 83.0% | |
| **V6.7** | pm=1/18 | 6.335 | 0.031 | 85.0% | |
| **V6.8** | pm=1/22 | 6.338 | 0.038 | 87.5% | |
| **V6.9** | DE F=0.3 CR=0.6 | 6.335 | 0.036 | 85.0% | |
| **V6.10** | DE_prob=15% | 6.390 | 0.027 | 97.5% | ❌ |
| **V6.11** | perturbacion=0.01 | 6.333 | 0.044 | 87.5% | |

### Análisis de resultados

#### V6.5: Mejor versión encontrada ✅

**Cambio**: `max_reemplazos = 2` (aumentado de 1)

**Resultados**:
- **CS2**: 82.5% (mejor que V6.3 con 85.0%)
- **HV**: 6.338 (mejor que V6.3 con 6.329)
- **Spacing**: 0.025 (mejor que V6.3 con 0.026)

**Razón del éxito**: Permitir hasta 2 reemplazos en el vecindario aumenta la presión de selección sin ser demasiado agresivo, mejorando la convergencia hacia el frente de Pareto.

#### Otras pruebas que empeoraron

- **V6.6 (max_repl=3)**: CS2 empeoró a 83.0%, demasiada presión de reemplazo
- **V6.7 (pm=1/18)**: Más mutación empeoró CS2 (85.0%) y Spacing (0.031)
- **V6.8 (pm=1/22)**: Menos mutación empeoró CS2 (87.5%) y Spacing (0.038)
- **V6.9 (DE F=0.3 CR=0.6)**: Parámetros DE menos agresivos empeoraron CS2 (85.0%)
- **V6.10 (DE_prob=15%)**: Reducir probabilidad DE empeoró mucho CS2 (97.5%)
- **V6.11 (perturbacion=0.01)**: Menos perturbación empeoró CS2 (87.5%) y Spacing (0.044)

### Parámetros finales V6.5 (ÓPTIMA)

- **T**: Calculado automáticamente como 22.5% de N (T=9 para N=40)
- **pm**: 1/20
- **Perturbación pesos**: 0.02
- **DE**: 20% probabilidad, F=0.5, CR=0.5
- **max_reemplazos**: **2** (cambio clave respecto a V6.3)

### Conclusión

El ajuste más efectivo fue aumentar `max_reemplazos` de 1 a 2, lo que permite una mejor convergencia sin perder demasiada diversidad. Los otros parámetros (pm, DE, perturbación) funcionan mejor con sus valores estándar.

## Versión 7: Pruebas de combinaciones de parámetros

### Análisis del problema: ¿Por qué NSGA-II domina tanto?

**Problema identificado**: CS2 = 82.5% (82.5% de nuestros puntos son dominados por NSGA-II)

**Razones principales**:

1. **NSGA-II explora mejor los extremos del frente**: ZDT3 tiene 5 segmentos discontinuos, y el último segmento (f1 ∈ [0.82, 1.0]) no está bien cubierto por MOEA/D debido a pesos lineales equiespaciados.

2. **Mejor distribución (spacing)**: NSGA-II tiene spacing = 0.011 vs MOEA/D = 0.025. NSGA-II usa crowding distance que mantiene diversidad explícitamente.

3. **Reemplazo local vs selección global**: MOEA/D reemplaza solo en vecindario (local), mientras NSGA-II tiene selección global basada en dominancia.

### Combinaciones probadas

Se probaron combinaciones lógicas de parámetros basadas en teoría:

| Versión | Parámetros | HV | Spacing | CS2 | Análisis |
|---------|-----------|----|---------|-----|----------|
| **V6.5** | Base (óptima individual) | 6.338 | 0.025 | 82.5% | Referencia |
| **V7.1** | pm=1/18, DE=30%, perturb=0.03 | 6.387 | 0.030 | 97.5% | ❌ Exploración extrema empeora |
| **V7.2** | perturb=0.03, T=25% | 6.382 | 0.028 | 90.0% | ❌ Más perturbación empeora |
| **V7.3** | pm=1/18, DE=25%, perturb=0.025, T=25% | 6.213 | 0.033 | **67.5%** | ✅ **MEJOR CS2** |

### Resultados V7.3 (Mejor combinación)

**Parámetros**:
- **pm**: 1/18 (más mutación)
- **DE_prob**: 25% (ligeramente más DE)
- **perturbacion_pesos**: 0.025 (ligeramente más)
- **max_reemplazos**: 2
- **T**: 25% (vecindarios más grandes)

**Resultados**:
- ✅ **CS2: 67.5%** (mejora de 15% respecto a V6.5 con 82.5%)
- ⚠️ **HV: 6.213** (bajó de 6.338, pero aún mejor que NSGA-II con 6.257)
- ⚠️ **Spacing: 0.033** (empeoró de 0.025, pero aceptable)

**Conclusión V7.3**: La combinación balanceada de aumentos moderados en todos los parámetros de exploración logra el mejor Coverage Set (67.5%), reduciendo significativamente la dominancia de NSGA-II. El trade-off es una ligera pérdida en HV y spacing, pero el CS2 es la métrica más crítica para comparar algoritmos.

### Lecciones aprendidas

1. **Exploración extrema no funciona**: V7.1 (exploración máxima) empeoró mucho el CS2 (97.5%)
2. **Balance es clave**: Aumentos moderados en múltiples parámetros funcionan mejor que cambios extremos en uno solo
3. **Vecindarios más grandes ayudan**: T=25% (vs 22.5%) mejora la mezcla global
4. **Mutación moderadamente mayor**: pm=1/18 (vs 1/20) ayuda sin ser excesivo

## Intentos de mejora de V7.3 (V7.4 - V7.9)

Se intentó mejorar el HV y Spacing de V7.3 manteniendo el buen CS2, pero se encontró un **trade-off fuerte** entre estas métricas:

| Versión | Cambio | HV | Spacing | CS2 | Resultado |
|---------|--------|----|---------|-----|-----------|
| **V7.3** | Base | 6.213 | 0.033 | 67.5% | Referencia |
| **V7.4** | max_repl=1, menos expl | 6.388 | 0.030 | 90.0% | ❌ CS2 empeoró |
| **V7.5** | Intermedio | 6.391 | 0.023 | 95.0% | ❌ CS2 empeoró mucho |
| **V7.6** | Sutil V7.3 | 6.213 | 0.041 | 67.5% | ❌ Spacing empeoró |
| **V7.7** | menos perturb + más DE | 6.389 | 0.027 | 90.0% | ❌ CS2 empeoró |
| **V7.8** | Balance final | 6.211 | 0.046 | **65.0%** | ⚠️ CS2 mejoró pero spacing muy malo |
| **V7.9** | Compromiso | 6.336 | 0.034 | 82.5% | ❌ CS2 empeoró |

### Análisis de los intentos

**Problema identificado**: Existe un **trade-off fuerte** entre:
- **CS2 (Coverage Set)**: Requiere exploración para cubrir extremos del frente
- **HV (Hypervolume)**: Requiere convergencia hacia el frente de Pareto
- **Spacing**: Requiere distribución uniforme (menos perturbación)

**Observaciones**:
1. **Mejorar HV y Spacing empeora el CS2**: Reducir exploración mejora convergencia pero pierde cobertura de extremos
2. **Mejorar CS2 empeora el Spacing**: Más exploración (perturbación) mejora cobertura pero empeora distribución
3. **V7.8** logró el mejor CS2 (65.0%) pero con spacing muy malo (0.046)

### Conclusión

**V7.3 mantiene el mejor balance general**:
- CS2: 67.5% (mejor que V6.5 con 82.5%)
- HV: 6.213 (aunque peor que NSGA-II con 6.257, es aceptable)
- Spacing: 0.033 (aunque peor que NSGA-II con 0.011, es aceptable)

**Recomendación**: Mantener V7.3 como versión final. El trade-off entre CS2, HV y Spacing es inherente al problema y no se puede mejorar significativamente sin sacrificar otra métrica importante.

## ¿Se puede mejorar más vs NSGA-II?

### Limitación de Ajustes de Parámetros

Los ajustes de parámetros (V7.3-V7.9) tienen un **trade-off fuerte** y **no pueden superar las ventajas estructurales de NSGA-II**:

1. **NSGA-II tiene crowding distance**: Mecanismo explícito de diversidad que mantiene spacing uniforme (0.011)
2. **NSGA-II tiene selección global**: Puede mantener soluciones en extremos aunque no sean óptimas localmente
3. **NSGA-II explora mejor extremos**: Mejor cobertura del último segmento (f1 > 0.8)

**Conclusión**: Con solo ajustar parámetros, **no podemos superar completamente estas ventajas estructurales**.

### Propuesta V8: Cambios Estructurales

Para mejorar más, necesitaríamos **cambios estructurales** (ver `PROPUESTA_V8.md`):

1. **Mecanismo de diversidad explícito**: Añadir crowding distance similar a NSGA-II
2. **Pesos adaptativos**: Ajustar pesos según densidad del frente (especialmente para f1 > 0.8)
3. **Actualización adaptativa**: Combinar reemplazo local con actualización global periódica
4. **Exploración explícita de extremos**: Mecanismo para explorar regiones poco cubiertas

Estos cambios son más complejos pero tienen el potencial de mejorar significativamente el spacing y la exploración de extremos.

### Recomendación Final

**V7.3 es la mejor versión con ajustes de parámetros** y es adecuada para:
- ✅ Mejor CS2 que V6.5 (67.5% vs 82.5%)
- ✅ Resultados reproducibles y estables
- ✅ Implementación simple y mantenible

**Para mejorar más**, se necesitarían cambios estructurales (V8) que requieren:
- ⚠️ Más tiempo de implementación
- ⚠️ Más pruebas y validación
- ⚠️ Mayor complejidad del código

**Decisión**: Si necesitas resultados ahora, **V7.3 es la mejor opción**. Si tienes tiempo para implementar cambios estructurales, **V8 podría mejorar más**.

