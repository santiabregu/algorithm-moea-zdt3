# Análisis: ¿Por qué MOEA/D elimina soluciones con f1 > 0.8?

## Problema Observado

Aunque generamos soluciones con f1 > 0.8 (exploración explícita), el algoritmo las elimina durante el proceso evolutivo.

## Causa Raíz: Descomposición con Pesos Equiespaciados

### 1. Cómo funciona MOEA/D

MOEA/D descompone el problema multiobjetivo en **N subproblemas**, cada uno con un **peso λ**:

```
λᵢ = (i/(N-1), 1 - i/(N-1))
```

Con N=40:
- λ₀ = (0, 1) → optimiza solo f2
- λ₂₀ = (0.5, 0.5) → balance f1 y f2
- λ₃₉ = (1, 0) → optimiza solo f1

### 2. Función Tchebycheff

Cada subproblema i optimiza:
```
g_te(f, λᵢ, z*) = max(λ₁|f₁ - z₁*|, λ₂|f₂ - z₂*|)
```

**Problema**: Una solución con f1 alto (ej: f1=0.85) tiene:
- **Buen valor Tchebycheff** para pesos con λ₁ alto (favorecen f1)
- **MAL valor Tchebycheff** para pesos con λ₁ bajo (favorecen f2)

### 3. Reemplazo Local

MOEA/D reemplaza solo en el **vecindario** (T subproblemas cercanos):

```python
for m in Bi:  # Vecindario del subproblema i
    if g_hijo <= g_padre:
        reemplazar()
```

**Problema**: Si una solución con f1 alto está asignada a un subproblema con λ₁ bajo, tiene mal valor Tchebycheff y es eliminada por soluciones con f1 bajo que tienen mejor valor para ese peso.

### 4. Por qué se eliminan soluciones con f1 > 0.8

**Ejemplo concreto**:

Solución con f1=0.85, f2=-0.7:
- Para λ = (0.1, 0.9) (favorece f2):
  - g_te = max(0.1*|0.85-0|, 0.9*|-0.7-0|) = max(0.085, 0.63) = **0.63**
  
Solución con f1=0.2, f2=0.5:
- Para λ = (0.1, 0.9):
  - g_te = max(0.1*|0.2-0|, 0.9*|0.5-0|) = max(0.02, 0.45) = **0.45**

**Resultado**: La solución con f1=0.2 tiene mejor Tchebycheff (0.45 < 0.63) y **reemplaza** a la solución con f1=0.85.

### 5. Por qué NSGA-II no tiene este problema

NSGA-II usa **selección global** basada en:
1. **Dominancia**: Soluciones no dominadas tienen prioridad
2. **Crowding distance**: Entre soluciones del mismo frente, mantiene las más diversas

**Resultado**: NSGA-II puede mantener soluciones en extremos aunque no sean óptimas para ningún subproblema específico, porque las mantiene por **diversidad**.

## Solución: Protección Explícita de Extremos

Para mantener soluciones con f1 > 0.8, necesitamos:

1. **Proteger soluciones en extremos** durante el reemplazo (ya implementado en V8.5)
2. **Asignar pesos específicos** a extremos (pesos adaptativos)
3. **Actualización global periódica** para mantener diversidad (ya implementado)

## Conclusión

**MOEA/D elimina soluciones con f1 > 0.8 porque**:
- Los pesos equiespaciados favorecen f1 bajo para la mayoría de subproblemas
- El reemplazo local elimina soluciones con f1 alto que tienen mal Tchebycheff
- No hay mecanismo global de diversidad como NSGA-II

**Solución V8**: Añadir protección explícita y exploración de extremos, pero aún así es difícil mantenerlas porque el mecanismo fundamental (descomposición) las penaliza.

