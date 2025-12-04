# Conclusiones de Todos los Experimentos Realizados

## Resumen Ejecutivo

A lo largo de todas las versiones (V1-V8.4), se han identificado **trade-offs claros** entre las métricas y se han establecido **patrones consistentes** sobre qué parámetros mejoran qué aspectos del algoritmo.

---

## 1. TRADE-OFFS PRINCIPALES IDENTIFICADOS

### 1.1 Trade-off: CS2 vs HV

**Patrón observado**:
- ✅ **Aumentar exploración** (mutación, DE, perturbación) → **Mejora CS2** (menos dominado)
- ❌ **Aumentar exploración** → **Empeora HV** (menos convergencia)

**Ejemplos**:
- **V7.3**: Exploración moderada → CS2 = 67.5%, HV = 6.213
- **V7.4**: Menos exploración → CS2 = 90.0%, HV = 6.388
- **V8.1**: Exploración + cambios estructurales → CS2 = 57.5%, HV = 6.197
- **V8.2**: Más protección extremos → CS2 = 67.5%, HV = 6.277

**Conclusión**: No se puede optimizar CS2 y HV simultáneamente. Hay que elegir prioridad.

### 1.2 Trade-off: CS2 vs Spacing

**Patrón observado**:
- ✅ **Aumentar exploración** (perturbación pesos) → **Mejora CS2**
- ❌ **Aumentar exploración** → **Empeora Spacing** (menos uniforme)

**Ejemplos**:
- **V7.3**: Perturbación 0.025 → CS2 = 67.5%, Spacing = 0.033
- **V7.8**: Más perturbación → CS2 = 65.0%, Spacing = 0.046 (muy malo)

**Conclusión**: Más exploración mejora cobertura pero empeora uniformidad.

### 1.3 Trade-off: Cobertura Extremos vs CS2

**Patrón observado**:
- ✅ **Exploración agresiva de extremos** (f1 > 0.8) → **Mejora cobertura extremos**
- ❌ **Exploración agresiva de extremos** → **Empeora CS2** (soluciones no óptimas se mantienen)

**Ejemplos**:
- **V8.3**: Exploración moderada → 2/10 seeds con f1 > 0.8, CS2 = 65.0%
- **V8.4**: Exploración agresiva → 5/10 seeds con f1 > 0.8, CS2 = 80.0%

**Conclusión**: Proteger extremos mejora cobertura pero empeora convergencia global.

---

## 2. PARÁMETROS Y SUS EFECTOS

### 2.1 Probabilidad de Mutación (pm)

**Efectos observados**:

| pm | Efecto en CS2 | Efecto en HV | Efecto en Spacing | Conclusión |
|----|---------------|--------------|-------------------|------------|
| **1/30** (bajo) | ❌ Malo (80%+) | ✅ Bueno | ✅ Bueno | Muy conservador, no explora |
| **1/20** (medio) | ⚠️ Medio (82-87%) | ✅ Bueno | ✅ Bueno | Balance básico |
| **1/18** (alto) | ✅ Mejor (67-80%) | ⚠️ Medio | ⚠️ Medio | Más exploración, mejor CS2 |
| **1/15** (muy alto) | ✅ Mejor | ⚠️ Medio | ❌ Malo | Demasiado exploratorio |

**Conclusión**: 
- **pm = 1/18** es el óptimo para balance CS2/HV
- Menos mutación → mejor HV pero peor CS2
- Más mutación → mejor CS2 pero peor spacing

### 2.2 Probabilidad de Differential Evolution (DE_prob)

**Efectos observados**:

| DE_prob | Efecto en CS2 | Efecto en HV | Conclusión |
|---------|---------------|--------------|------------|
| **0%** (solo SBX) | ❌ Malo (92%) | ✅ Bueno | SBX muy conservador |
| **20%** | ✅ Mejor (82-85%) | ✅ Bueno | Óptimo balance |
| **30%** | ⚠️ Medio (87%) | ✅ Bueno | Demasiado exploratorio |
| **50%** | ❌ Malo (100%) | ✅ Bueno | DE demasiado agresivo |

**Conclusión**:
- **DE_prob = 20-25%** es el óptimo
- DE es más exploratorio que SBX, ayuda a cubrir extremos
- Demasiado DE empeora convergencia (CS2 empeora)

### 2.3 Perturbación de Pesos

**Efectos observados**:

| Perturbación | Efecto en CS2 | Efecto en Spacing | Conclusión |
|--------------|---------------|-------------------|------------|
| **0** (sin perturbación) | ❌ Malo | ✅ Bueno | Pesos equiespaciados no cubren frentes discontinuos |
| **0.02** | ⚠️ Medio | ✅ Bueno | Perturbación mínima |
| **0.025** | ✅ Mejor | ⚠️ Medio | Óptimo para ZDT3 |
| **0.05** | ✅ Mejor | ❌ Malo | Demasiado ruido, inestabilidad |

**Conclusión**:
- **Perturbación = 0.025** es el óptimo
- Perturbación ayuda a cubrir frentes discontinuos (mejora CS2)
- Demasiada perturbación empeora spacing (ruido)

### 2.4 Tamaño de Vecindario (T)

**Efectos observados**:

| T (% de N) | Efecto en CS2 | Efecto en Diversidad | Conclusión |
|------------|---------------|----------------------|------------|
| **20%** (T=8) | ✅ Bueno | ⚠️ Medio | Vecindarios pequeños, convergencia local |
| **22.5%** (T=9) | ✅ Bueno | ✅ Bueno | Balance óptimo |
| **25%** (T=10) | ✅ Mejor | ✅ Bueno | Mejor mezcla global |
| **30%** (T=12) | ⚠️ Medio | ❌ Malo | Demasiado grande, pérdida de diversidad |

**Conclusión**:
- **T = 22.5-25% de N** es el óptimo
- Vecindarios más grandes mejoran mezcla global (mejora CS2)
- Vecindarios demasiado grandes causan pérdida de diversidad

### 2.5 Máximo de Reemplazos (max_reemplazos)

**Efectos observados**:

| max_reemplazos | Efecto en CS2 | Efecto en Diversidad | Conclusión |
|----------------|---------------|----------------------|------------|
| **1** | ⚠️ Medio | ✅ Bueno | Conservador, mantiene diversidad |
| **2** | ✅ Mejor | ⚠️ Medio | Balance óptimo |
| **3+** | ❌ Malo | ❌ Malo | Demasiado agresivo, pérdida de diversidad |

**Conclusión**:
- **max_reemplazos = 2** es el óptimo
- Más reemplazos mejora convergencia pero empeora diversidad
- Menos reemplazos mantiene diversidad pero empeora convergencia

---

## 3. CAMBIOS ESTRUCTURALES Y SUS EFECTOS

### 3.1 Crowding Distance

**Efecto**:
- ✅ **Mejora Spacing** (distribución más uniforme)
- ⚠️ **Efecto neutro en CS2** (no mejora ni empeora significativamente)
- ⚠️ **Efecto neutro en HV** (ligera mejora o empeoramiento)

**Conclusión**: Crowding distance es útil para mejorar spacing pero no resuelve el problema de CS2.

### 3.2 Exploración Explícita de Extremos

**Efecto**:
- ✅ **Mejora cobertura f1 > 0.8** (de 2/10 a 5/10 seeds en V8.4)
- ✅ **Mejora HV** (mejor cobertura del frente completo)
- ❌ **Empeora CS2** (soluciones no óptimas se mantienen)

**Conclusión**: Exploración explícita de extremos es necesaria para cubrir el último segmento, pero tiene costo en CS2.

### 3.3 Protección de Extremos (margen de protección)

**Efecto**:

| Margen | Efecto en Cobertura f1>0.8 | Efecto en CS2 | Conclusión |
|--------|----------------------------|---------------|------------|
| **7%** | ⚠️ Medio (2/10 seeds) | ✅ Mejor (57.5%) | Protección mínima |
| **9%** | ⚠️ Medio (2/10 seeds) | ✅ Bueno (65.0%) | Balance |
| **10-12%** | ✅ Mejor (2/10 seeds) | ⚠️ Medio (67.5%) | Más protección |
| **15%** | ✅ Mucho mejor (5/10 seeds) | ❌ Malo (80.0%) | Muy agresivo |

**Conclusión**:
- **Margen 7-9%** es óptimo para balance CS2/cobertura
- **Margen 15%** mejora cobertura extremos pero empeora CS2 significativamente

### 3.4 Actualización Adaptativa Periódica

**Efecto**:
- ✅ **Mantiene diversidad** (similar a NSGA-II)
- ⚠️ **Efecto variable en CS2** (depende de frecuencia)
- ⚠️ **Puede interrumpir convergencia** si es muy frecuente

**Conclusión**:
- **Cada 7-10 generaciones** es el rango óptimo
- Más frecuente (cada 6) puede interrumpir convergencia
- Menos frecuente (cada 10+) no mantiene suficiente diversidad

---

## 4. PATRONES GENERALES OBSERVADOS

### 4.1 Exploración vs Convergencia

**Patrón**:
- **Más exploración** (mutación alta, DE, perturbación) → **Mejor CS2, peor HV**
- **Menos exploración** (mutación baja, solo SBX) → **Mejor HV, peor CS2**

**Razón teórica**: 
- Exploración ayuda a cubrir extremos y regiones poco exploradas (mejora CS2)
- Pero reduce convergencia hacia el frente óptimo (empeora HV)

### 4.2 Diversidad vs Convergencia

**Patrón**:
- **Más diversidad** (crowding distance, actualización adaptativa) → **Mejor spacing, efecto variable en CS2**
- **Menos diversidad** (reemplazo agresivo) → **Mejor convergencia local, peor spacing**

**Razón teórica**:
- Diversidad mantiene distribución uniforme (mejora spacing)
- Pero puede mantener soluciones no óptimas (efecto variable en CS2)

### 4.3 Protección de Extremos vs Convergencia Global

**Patrón**:
- **Más protección de extremos** → **Mejor cobertura f1 > 0.8, peor CS2**
- **Menos protección** → **Mejor CS2, peor cobertura extremos**

**Razón teórica**:
- Proteger extremos mantiene soluciones en regiones poco exploradas (mejora cobertura)
- Pero estas soluciones pueden no ser óptimas globalmente (empeora CS2)

---

## 5. CONFIGURACIÓN ÓPTIMA ENCONTRADA

### 5.1 Para Mejor CS2 (menos dominado por NSGA-II)

**Parámetros**:
- **pm**: 1/18
- **DE_prob**: 25%
- **perturbacion_pesos**: 0.025
- **T**: 25% de N
- **max_reemplazos**: 2
- **Protección extremos**: 7-9% (margen)
- **Exploración extremos**: 12-13% de población, cada 3 generaciones

**Resultado**: CS2 = 57.5-65.0%, HV = 6.197-6.238

**Versión**: V8.1 o V8.3

### 5.2 Para Mejor HV (superar NSGA-II)

**Parámetros**:
- **pm**: 1/18
- **DE_prob**: 25%
- **perturbacion_pesos**: 0.025
- **T**: 25% de N
- **max_reemplazos**: 2
- **Protección extremos**: 10-12% (margen)
- **Exploración extremos**: 15% de población, cada 2-3 generaciones

**Resultado**: HV = 6.277-6.283, CS2 = 67.5-80.0%

**Versión**: V8.2 o V8.4

### 5.3 Para Mejor Cobertura de Extremos (f1 > 0.8)

**Parámetros**:
- **pm**: 1/18
- **DE_prob**: 25%
- **perturbacion_pesos**: 0.025
- **T**: 25% de N
- **max_reemplazos**: 2
- **Protección extremos**: 15% (margen muy agresivo)
- **Exploración extremos**: 18% de población, cada 2 generaciones
- **Target f1**: 0.7-0.95 (más alto)

**Resultado**: 5/10 seeds con f1 > 0.8, HV = 6.283, CS2 = 80.0%

**Versión**: V8.4

### 5.4 Para Mejor Balance General

**Parámetros**:
- **pm**: 1/18
- **DE_prob**: 25%
- **perturbacion_pesos**: 0.025
- **T**: 25% de N
- **max_reemplazos**: 2
- **Protección extremos**: 9% (margen balanceado)
- **Exploración extremos**: 12.5% de población, cada 3 generaciones
- **Actualización adaptativa**: cada 8 generaciones

**Resultado**: HV = 6.238 (supera NSGA-II), CS2 = 65.0%, Spacing = 0.034

**Versión**: V8.3

---

## 6. LIMITACIONES ESTRUCTURALES IDENTIFICADAS

### 6.1 Reemplazo Local vs Selección Global

**Problema**:
- MOEA/D usa reemplazo local (solo en vecindario)
- NSGA-II usa selección global (toda la población)

**Consecuencia**:
- MOEA/D no puede "rescatar" soluciones buenas en malos subproblemas
- NSGA-II puede mantener extremos aunque no sean óptimos localmente

**Solución parcial**: Actualización adaptativa periódica (V8) ayuda pero no resuelve completamente.

### 6.2 Pesos Equiespaciados vs Frente Discontinuo

**Problema**:
- Pesos equiespaciados no cubren bien los 5 segmentos discontinuos de ZDT3
- Especialmente el último segmento (f1 > 0.8) tiene poca representación

**Consecuencia**:
- Solo 2-5 de 10 seeds logran mantener f1 > 0.8
- NSGA-II cubre mejor este segmento

**Solución parcial**: Perturbación de pesos (0.025) y exploración explícita de extremos (V8) ayudan pero no resuelven completamente.

### 6.3 Trade-off Inherente

**Problema**:
- No se puede optimizar CS2, HV y Spacing simultáneamente
- Mejorar uno empeora otro

**Consecuencia**:
- Hay que elegir prioridad según objetivo de competición
- No existe "versión perfecta" que gane en todas las métricas

---

## 7. CONCLUSIONES FINALES

### 7.1 Sobre Parámetros

1. **Mutación moderadamente alta** (pm = 1/18) es necesaria para exploración
2. **DE con probabilidad baja** (20-25%) ayuda sin ser demasiado agresivo
3. **Perturbación de pesos moderada** (0.025) es esencial para frentes discontinuos
4. **Vecindarios medianos** (22.5-25% de N) balancean convergencia y diversidad
5. **Reemplazos limitados** (max_reemplazos = 2) mantienen diversidad

### 7.2 Sobre Cambios Estructurales

1. **Crowding distance** mejora spacing pero no resuelve CS2
2. **Exploración explícita de extremos** es necesaria pero tiene costo en CS2
3. **Protección de extremos** debe ser balanceada (7-9% óptimo, 15% demasiado agresivo)
4. **Actualización adaptativa** ayuda a mantener diversidad pero no debe ser muy frecuente

### 7.3 Sobre Trade-offs

1. **CS2 vs HV**: Trade-off fuerte, no se pueden optimizar simultáneamente
2. **CS2 vs Spacing**: Trade-off moderado, más exploración empeora uniformidad
3. **Cobertura extremos vs CS2**: Trade-off fuerte, proteger extremos empeora convergencia global

### 7.4 Sobre Limitaciones

1. **Reemplazo local** es limitante estructural de MOEA/D
2. **Pesos equiespaciados** no cubren bien frentes discontinuos
3. **NSGA-II tiene ventajas estructurales** que MOEA/D no puede superar completamente

### 7.5 Versión Recomendada Según Objetivo

- **Mejor CS2**: V8.1 (CS2 = 57.5%)
- **Mejor HV**: V8.4 (HV = 6.283)
- **Mejor cobertura extremos**: V8.4 (5/10 seeds con f1 > 0.8)
- **Mejor balance general**: V8.3 (HV = 6.238, CS2 = 65.0%)

---

## 8. LECCIONES APRENDIDAS

1. **Balance es clave**: Cambios extremos en un parámetro empeoran otras métricas
2. **Exploración moderada funciona mejor**: Demasiada exploración empeora convergencia
3. **Cambios estructurales son necesarios**: Solo ajustar parámetros tiene límites
4. **Trade-offs son inherentes**: No se puede ganar en todas las métricas simultáneamente
5. **Metodología rigurosa es esencial**: Punto de referencia común, múltiples seeds, métricas del profesor

