# Análisis: ¿Por qué NSGA-II domina tanto a MOEA/D?

## Problema actual
- **CS2 = 82.5%**: 82.5% de nuestros puntos son dominados por NSGA-II
- **HV mejor**: 6.338 vs 6.257 (MOEA/D gana)
- **Spacing peor**: 0.025 vs 0.011 (NSGA-II gana)

## ¿Por qué NSGA-II domina tanto?

### 1. **NSGA-II explora mejor los extremos del frente**

**ZDT3 tiene 5 segmentos discontinuos:**
- Segmento 1: f1 ∈ [0, ~0.08]
- Segmento 2: f1 ∈ [~0.18, ~0.25]
- Segmento 3: f1 ∈ [~0.35, ~0.45]
- Segmento 4: f1 ∈ [~0.55, ~0.75]
- Segmento 5: f1 ∈ [~0.82, 1.0] ← **MOEA/D no explora bien este**

**Observación**: NSGA-II tiene puntos con f1 hasta ~0.85, mientras que MOEA/D se queda en f1 ≈ 0.8.

### 2. **Pesos lineales equiespaciados no cubren bien frentes discontinuos**

```
λᵢ = (i/(N−1), 1 − i/(N−1))
```

Con N=40, los pesos están equiespaciados en [0,1], pero:
- Los 5 segmentos de ZDT3 NO están equiespaciados
- Algunos segmentos quedan sin representación suficiente
- El último segmento (f1 > 0.8) tiene pocos pesos asignados

### 3. **NSGA-II tiene mejor distribución (spacing)**

- **NSGA-II spacing = 0.011**: Distribución muy uniforme
- **MOEA/D spacing = 0.025**: 2.3x peor

**Razón**: NSGA-II usa crowding distance que mantiene diversidad explícitamente. MOEA/D depende de los pesos y vecindarios, que pueden crear clusters.

### 4. **Reemplazo local vs selección global**

- **MOEA/D**: Reemplaza solo en vecindario (local)
- **NSGA-II**: Selección global basada en dominancia y crowding

**Consecuencia**: NSGA-II puede mantener soluciones en extremos aunque no sean óptimas localmente. MOEA/D puede perder diversidad en extremos.

## Teoría: ¿Qué debería mejorar MOEA/D?

### 1. **Mayor exploración de extremos**
- Aumentar mutación en regiones poco exploradas
- Usar más DE (más exploratorio que SBX)
- Perturbación de pesos más agresiva

### 2. **Mejor distribución de pesos**
- Pesos adaptativos o no lineales
- Más perturbación para cubrir huecos
- Vecindarios más grandes para mejor mezcla

### 3. **Mecanismo de diversidad explícito**
- Similar a crowding distance de NSGA-II
- Penalizar soluciones muy cercanas
- Forzar exploración de regiones vacías

## Combinaciones lógicas a probar

### Combinación 1: "Más exploración"
- **pm**: 1/18 (más mutación)
- **DE_prob**: 30% (más DE)
- **perturbacion_pesos**: 0.03 (más exploración de pesos)
- **max_reemplazos**: 2 (mantener)
- **T**: 22.5% (mantener)

**Razón**: Si NSGA-II explora mejor, necesitamos más exploración.

### Combinación 2: "Mejor distribución"
- **pm**: 1/20 (mantener)
- **DE_prob**: 20% (mantener)
- **perturbacion_pesos**: 0.03 (aumentar)
- **max_reemplazos**: 2 (mantener)
- **T**: 25% (vecindarios más grandes)

**Razón**: Vecindarios más grandes mejoran mezcla global, más perturbación cubre huecos.

### Combinación 3: "Balance exploración-convergencia"
- **pm**: 1/18 (más mutación)
- **DE_prob**: 25% (ligeramente más DE)
- **perturbacion_pesos**: 0.025 (ligeramente más)
- **max_reemplazos**: 2 (mantener)
- **T**: 25% (vecindarios más grandes)

**Razón**: Aumento moderado en todos los parámetros de exploración.

### Combinación 4: "Exploración extrema"
- **pm**: 1/15 (mucho más mutación)
- **DE_prob**: 30% (más DE)
- **perturbacion_pesos**: 0.04 (mucha perturbación)
- **max_reemplazos**: 3 (más reemplazos)
- **T**: 25% (vecindarios más grandes)

**Razón**: Si la exploración es el problema, maximicémosla.

