#!/usr/bin/env python3
"""
Script para calcular el hipervolumen por generación y promediar entre semillas.

Uso:
    python hypervolume_per_gen.py <directorio_archivos> [--ref_x 0.8497500000] [--ref_y 1.2192250000]
    
Ejemplo:
    python hypervolume_per_gen.py ../../src/algoritmo/
    python hypervolume_per_gen.py ../nsga2_profesor/EVAL4000/EVAL4000/P40G100/

Salida:
    - hypervolume_per_gen.out: hipervolumen promedio por generación
    - hypervolume_per_gen_all.out: hipervolumen de cada semilla por generación
"""

import os
import sys
import glob
import argparse
import math


def get_non_dominated(points):
    """Filtra solo los puntos no dominados (frente de Pareto)."""
    non_dominated = []
    for i, p in enumerate(points):
        dominated = False
        for j, q in enumerate(points):
            if i != j:
                # q domina a p si q es mejor o igual en todos los objetivos
                # y estrictamente mejor en al menos uno (minimización)
                if q[0] <= p[0] and q[1] <= p[1] and (q[0] < p[0] or q[1] < p[1]):
                    dominated = True
                    break
        if not dominated:
            non_dominated.append(p)
    return non_dominated


def hypervolume_2d(points, ref_point):
    """
    Calcula el hipervolumen 2D para un conjunto de puntos.
    
    Args:
        points: Lista de tuplas (f1, f2)
        ref_point: Punto de referencia (ref_x, ref_y)
    
    Returns:
        Hipervolumen (área dominada)
    """
    if not points:
        return 0.0
    
    # Filtrar puntos que estén dentro del cuadrante definido por el punto de referencia
    valid_points = [(p[0], p[1]) for p in points if p[0] < ref_point[0] and p[1] < ref_point[1]]
    
    if not valid_points:
        return 0.0
    
    # Obtener solo puntos no dominados
    pareto_front = get_non_dominated(valid_points)
    
    if not pareto_front:
        return 0.0
    
    # Ordenar por f1 ascendente
    pareto_front.sort(key=lambda x: x[0])
    
    # Calcular hipervolumen como suma de rectángulos
    hv = 0.0
    prev_x = 0.0  # Empezamos desde x=0 (o podríamos usar el mínimo de f1)
    
    for i, point in enumerate(pareto_front):
        # Ancho del rectángulo
        width = point[0] - prev_x
        # Altura: desde y del punto hasta el ref_y
        height = ref_point[1] - point[1]
        
        if width > 0 and height > 0:
            hv += width * height
        
        prev_x = point[0]
    
    # Último rectángulo hasta ref_x
    if prev_x < ref_point[0]:
        # Altura del último punto
        last_height = ref_point[1] - pareto_front[-1][1]
        width = ref_point[0] - prev_x
        if width > 0 and last_height > 0:
            hv += width * last_height
    
    return hv


def read_all_pop_file(filepath, pop_size=40):
    """
    Lee un archivo all_popm y devuelve una lista de generaciones.
    Cada generación es una lista de puntos (f1, f2).
    """
    generations = []
    current_gen = []
    
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            parts = line.split()
            if len(parts) >= 2:
                try:
                    f1 = float(parts[0])
                    f2 = float(parts[1])
                    current_gen.append((f1, f2))
                except ValueError:
                    continue
            
            # Si completamos una generación
            if len(current_gen) == pop_size:
                generations.append(current_gen)
                current_gen = []
    
    # Si quedó alguna generación incompleta al final
    if current_gen:
        generations.append(current_gen)
    
    return generations


def find_seed_files(directory, pattern="zdt3_all_popmp*g*_seed*.out"):
    """Encuentra todos los archivos de semillas en un directorio."""
    search_pattern = os.path.join(directory, pattern)
    files = glob.glob(search_pattern)
    return sorted(files)


def main():
    parser = argparse.ArgumentParser(description='Calcula hipervolumen por generación')
    parser.add_argument('directory', help='Directorio con archivos de semillas')
    parser.add_argument('--ref_x', type=float, default=1.0, 
                        help='Punto de referencia X (default: 1.0 para ZDT3)')
    parser.add_argument('--ref_y', type=float, default=6.0,
                        help='Punto de referencia Y (default: 6.0 para capturar evolución completa)')
    parser.add_argument('--pop_size', type=int, default=40,
                        help='Tamaño de población (default: 40)')
    parser.add_argument('--output', type=str, default='hypervolume_per_gen.out',
                        help='Archivo de salida para promedios')
    parser.add_argument('--output_all', type=str, default='hypervolume_per_gen_all.out',
                        help='Archivo de salida para todas las semillas')
    
    args = parser.parse_args()
    
    ref_point = (args.ref_x, args.ref_y)
    
    # Encontrar archivos
    seed_files = find_seed_files(args.directory)
    
    if not seed_files:
        print(f"Error: No se encontraron archivos en {args.directory}")
        print("Buscando patrón: zdt3_all_popmp*g*_seed*.out")
        sys.exit(1)
    
    print(f"Encontrados {len(seed_files)} archivos de semillas:")
    for f in seed_files:
        print(f"  - {os.path.basename(f)}")
    
    print(f"\nPunto de referencia: ({ref_point[0]}, {ref_point[1]})")
    print(f"Tamaño de población: {args.pop_size}")
    
    # Procesar cada archivo
    all_hv_data = {}  # {gen_idx: [hv_seed1, hv_seed2, ...]}
    
    for seed_file in seed_files:
        seed_name = os.path.basename(seed_file)
        print(f"\nProcesando {seed_name}...")
        
        generations = read_all_pop_file(seed_file, args.pop_size)
        print(f"  Generaciones leídas: {len(generations)}")
        
        for gen_idx, gen_points in enumerate(generations):
            hv = hypervolume_2d(gen_points, ref_point)
            
            if gen_idx not in all_hv_data:
                all_hv_data[gen_idx] = []
            all_hv_data[gen_idx].append(hv)
    
    # Calcular estadísticas y guardar
    num_gens = max(all_hv_data.keys()) + 1
    
    # Guardar promedios
    output_path = os.path.join(args.directory, args.output)
    with open(output_path, 'w') as f:
        f.write("# gen\thv_mean\thv_std\thv_min\thv_max\n")
        for gen in range(num_gens):
            if gen in all_hv_data:
                hvs = all_hv_data[gen]
                mean_hv = sum(hvs) / len(hvs)
                
                if len(hvs) > 1:
                    variance = sum((x - mean_hv)**2 for x in hvs) / (len(hvs) - 1)
                    std_hv = math.sqrt(variance)
                else:
                    std_hv = 0.0
                
                min_hv = min(hvs)
                max_hv = max(hvs)
                
                f.write(f"{gen}\t{mean_hv:.10e}\t{std_hv:.10e}\t{min_hv:.10e}\t{max_hv:.10e}\n")
    
    print(f"\n✓ Promedios guardados en: {output_path}")
    
    # Guardar todos los datos
    output_all_path = os.path.join(args.directory, args.output_all)
    with open(output_all_path, 'w') as f:
        # Header con nombres de semillas
        header = "# gen\t" + "\t".join([os.path.basename(sf) for sf in seed_files]) + "\n"
        f.write(header)
        
        for gen in range(num_gens):
            if gen in all_hv_data:
                hvs = all_hv_data[gen]
                line = f"{gen}\t" + "\t".join([f"{hv:.10e}" for hv in hvs]) + "\n"
                f.write(line)
    
    print(f"✓ Datos completos guardados en: {output_all_path}")
    
    # Mostrar resumen
    print("\n" + "="*60)
    print("RESUMEN")
    print("="*60)
    
    first_gen = all_hv_data.get(0, [0])
    last_gen = all_hv_data.get(num_gens-1, [0])
    
    print(f"Primera generación (gen 0):")
    print(f"  HV promedio: {sum(first_gen)/len(first_gen):.6f}")
    
    print(f"Última generación (gen {num_gens-1}):")
    print(f"  HV promedio: {sum(last_gen)/len(last_gen):.6f}")
    
    improvement = (sum(last_gen)/len(last_gen)) - (sum(first_gen)/len(first_gen))
    print(f"Mejora total: {improvement:.6f}")


if __name__ == "__main__":
    main()

