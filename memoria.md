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

