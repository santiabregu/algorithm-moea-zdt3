#!/bin/bash
# Script para combinar la última generación de todos los seeds en un solo archivo

# Directorio con los archivos de seeds (desde METRICS/utils/)
SEEDS_DIR="../../src/algoritmo"
OUTPUT_FILE="todos_seeds_gen100_moead.out"

# Parámetros
popsize=40
gens=100
start=$(( (gens-1)*popsize + 1 ))
end=$(( gens*popsize ))

# Limpiar archivo de salida
> "$OUTPUT_FILE"

# Seeds disponibles (seed99 se guarda como seed099)
seeds=(01 02 03 04 05 06 07 08 09 099)

echo "Combinando última generación (gen 100) de todos los seeds..."

for seed in "${seeds[@]}"; do
    seed_file="${SEEDS_DIR}/zdt3_all_popmp40g100_seed${seed}.out"
    
    if [ -f "$seed_file" ]; then
        # Extraer última generación (líneas start a end)
        sed -n "${start},${end}p" "$seed_file" >> "$OUTPUT_FILE"
        echo "  ✓ Seed ${seed}: $(sed -n "${start},${end}p" "$seed_file" | wc -l) puntos"
    else
        echo "  ⚠ Seed ${seed}: archivo no encontrado"
    fi
done

total_points=$(wc -l < "$OUTPUT_FILE")
echo ""
echo "✓ Total: ${total_points} puntos combinados en ${OUTPUT_FILE}"

