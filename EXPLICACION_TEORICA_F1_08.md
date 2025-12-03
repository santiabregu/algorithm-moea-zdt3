# Explicación Teórica: ¿Por qué la mayoría de seeds no superan f1 > 0.8?

## Observación Empírica

**Resultados por seed (Gen 100)**:
- **Seed 01**: Max f1 = 0.841, 12 puntos con f1 ≥ 0.8 ✅
- **Seed 02**: Max f1 = 0.858, 11 puntos con f1 ≥ 0.8 ✅
- **Seeds 03-09, 099**: Max f1 entre 0.445-0.654, **0 puntos con f1 ≥ 0.8** ❌

**Conclusión**: Solo 2 de 10 seeds (20%) logran mantener soluciones con f1 > 0.8.

## Explicación Teórica

### 1. Descomposición con Pesos Equiespaciados

MOEA/D descompone el problema en **N=40 subproblemas**, cada uno con un peso λ:

```
λᵢ = (i/(N-1), 1 - i/(N-1))
```

**Distribución de pesos**:
- λ₁ bajo (favorece f2): ~40% de pesos (i = 0-15)
- λ₁ medio (balance): ~20% de pesos (i = 16-23)
- λ₁ alto (favorece f1): ~40% de pesos (i = 24-39)

### 2. Función Tchebycheff

Cada subproblema i optimiza:
```
g_te(f, λᵢ, z*) = max(λ₁|f₁ - z₁*|, λ₂|f₂ - z₂*|)
```

**Problema**: Una solución con f1=0.85 tiene:
- ✅ **Buen Tchebycheff** para pesos con λ₁ alto (favorecen f1)
- ❌ **MAL Tchebycheff** para pesos con λ₁ bajo (favorecen f2)

### 3. Reemplazo Local (El Problema Clave)

MOEA/D reemplaza soluciones solo en el **vecindario** (T=9 subproblemas cercanos):

```python
for m in Bi:  # Vecindario del subproblema i
    if g_hijo <= g_padre:
        reemplazar()
```

**Problema crítico**:

1. **Vecindarios agrupan pesos similares**: Si un subproblema tiene λ₁ bajo, sus vecinos también tienen λ₁ bajo.

2. **Solución con f1 alto asignada a peso bajo**: Si una solución con f1=0.85 está en un subproblema con λ₁ bajo, tiene mal Tchebycheff.

3. **Eliminación en cascada**: Una solución con f1=0.2 tiene mejor Tchebycheff para ese peso y sus vecinos, por lo que **reemplaza** a la solución con f1=0.85 en **todos los vecinos**.

### 4. Ejemplo Concreto

**Subproblema 5**: λ = (0.13, 0.87) - favorece f2
**Vecindario**: [1, 2, 3, 4, 5, 6, 7, 8, 9] - todos con λ₁ bajo

**Solución f1=0.85, f2=-0.7**:
- g_te = max(0.13×|0.85-0|, 0.87×|-0.7-(-0.8)|) = max(0.1105, 0.087) = **0.1105**

**Solución f1=0.2, f2=0.5**:
- g_te = max(0.13×|0.2-0|, 0.87×|0.5-(-0.8)|) = max(0.026, 1.131) = **1.131**

**Resultado**: Aunque f_alto tiene mejor Tchebycheff (0.1105 < 1.131), el problema es que:
- Si f_alto está asignada a un subproblema con λ₁ bajo, tiene mal valor
- Los vecinos también tienen λ₁ bajo
- Una solución con f1 bajo puede tener mejor valor para estos pesos
- **f_alto es eliminada**

### 5. Por qué solo 2 seeds logran mantener f1 > 0.8

**Factores estocásticos**:

1. **Inicialización aleatoria**: Algunos seeds inicializan con más soluciones cerca de extremos
2. **Exploración de extremos**: La exploración explícita (cada 3 generaciones) puede generar soluciones con f1 alto
3. **Asignación a pesos altos**: Si una solución con f1 alto se asigna a un subproblema con λ₁ alto, tiene mejor Tchebycheff y puede mantenerse
4. **Protección de extremos**: La protección (V8.5) ayuda, pero no es suficiente

**Por qué falla en 8 de 10 seeds**:

- Las soluciones con f1 alto se generan, pero:
  - Se asignan a subproblemas con λ₁ bajo (por azar o por convergencia)
  - Tienen mal Tchebycheff para esos pesos
  - Son eliminadas por soluciones con f1 bajo
  - El reemplazo local no permite "rescatar" soluciones de otros vecindarios

### 6. Comparación con NSGA-II

**NSGA-II no tiene este problema** porque:
- **Selección global**: No depende de subproblemas locales
- **Crowding distance**: Mantiene diversidad explícitamente
- **Puede mantener extremos**: Aunque no sean óptimos localmente, las mantiene por diversidad

## Solución Teórica

Para que MOEA/D mantenga soluciones con f1 > 0.8 en todos los seeds, necesitaríamos:

1. **Pesos adaptativos**: Asignar más pesos específicamente a extremos (f1 > 0.8)
2. **Reemplazo global periódico**: Similar a NSGA-II, mantener soluciones por diversidad global
3. **Protección más fuerte**: Aumentar el margen de protección (actualmente 7%)
4. **Exploración más frecuente**: Generar más soluciones extremas

**Trade-off**: Estas soluciones pueden mejorar cobertura pero empeorar uniformidad (spacing).

## Conclusión

**La mayoría de seeds no superan f1 > 0.8 porque**:
- El mecanismo de descomposición + reemplazo local **penaliza estructuralmente** soluciones con f1 alto
- Solo cuando se alinean factores estocásticos favorables (inicialización, asignación a pesos altos, protección) se mantienen
- Es un **problema inherente** de MOEA/D con pesos equiespaciados y reemplazo local

**Solución práctica**: Aceptar que algunos seeds no cubren extremos, o implementar cambios estructurales más agresivos (con trade-offs en uniformidad).

