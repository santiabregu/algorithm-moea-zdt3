#!/usr/bin/env python3
"""
Script para calcular el hipervolumen promedio usando el programa 'metrics' del profesor.

IMPORTANTE (nota del profesor):
- El software metrics no puede comparar muchas frentes
- Sacamos HV manualmente y comparamos todas
- Necesitamos un punto de referencia COMÚN para todas
- Cogemos el peor f1 de TODOS los archivos y el peor f2 de TODOS

Este script:
1. Lee TODOS los archivos de ambos algoritmos para encontrar el peor f1 y f2
2. Usa ese punto como referencia común
3. Ejecuta ./metrics para cada archivo con ese punto de referencia
4. Promedia los resultados por generación

Uso:
    python hypervolume_avg_metrics.py <dir1> <dir2> [opciones]
    
Ejemplo:
    python hypervolume_avg_metrics.py ../../src/algoritmo/v4/ "../nsga2_profesor/EVAL4000(2)/EVAL4000/P40G100/"

Salida:
    - moead_hv_avg.out: HV promedio por generación para MOEA/D
    - nsga2_hv_avg.out: HV promedio por generación para NSGA-II
    - ref_point.out: Punto de referencia común usado
"""

import os
import sys
import glob
import shutil
import subprocess
import argparse
import math


def find_seed_files(directory, pattern="zdt3_all_popmp*g*_seed*.out"):
    """Encuentra todos los archivos de semillas en un directorio."""
    search_pattern = os.path.join(directory, pattern)
    files = glob.glob(search_pattern)
    return sorted(files)


def find_global_reference_point(all_files):
    """
    Lee TODOS los archivos y encuentra el peor (máximo) f1 y f2.
    Este será el punto de referencia común.
    """
    max_f1 = float('-inf')
    max_f2 = float('-inf')
    
    print("Buscando punto de referencia común (peor f1 y f2 de TODOS los archivos)...")
    
    for filepath in all_files:
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
                        if f1 > max_f1:
                            max_f1 = f1
                        if f2 > max_f2:
                            max_f2 = f2
                    except ValueError:
                        continue
    
    # Añadir un pequeño margen para asegurar que todos los puntos estén dentro
    ref_x = max_f1 * 1.01  # 1% de margen
    ref_y = max_f2 * 1.01
    
    return (ref_x, ref_y)


def run_metrics_tool(metrics_dir, filename, pop_size, generations, nobj, ref_point):
    """
    Ejecuta el programa metrics del profesor y devuelve el hipervolumen por generación.
    """
    metrics_executable = os.path.join(metrics_dir, "metrics")
    
    if not os.path.exists(metrics_executable):
        print(f"Error: No se encuentra el ejecutable 'metrics' en {metrics_dir}")
        return None
    
    # Input para metrics: manual reference point
    metrics_input = f"1\n1\n{nobj}\n{filename}\n{pop_size}\n{generations}\n0\n{ref_point[0]}\n{ref_point[1]}\n"
    
    try:
        result = subprocess.run(
            ["./metrics"],
            input=metrics_input,
            capture_output=True,
            text=True,
            cwd=metrics_dir,
            timeout=60
        )
        
        hypervol_file = os.path.join(metrics_dir, "hypervol.out")
        
        if not os.path.exists(hypervol_file):
            return None
        
        hv_data = {}
        with open(hypervol_file, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split()
                if len(parts) >= 2:
                    try:
                        gen = int(parts[0])
                        hv = float(parts[1])
                        hv_data[gen] = hv
                    except ValueError:
                        continue
        
        return hv_data
        
    except subprocess.TimeoutExpired:
        return None
    except Exception as e:
        print(f"  Error: {e}")
        return None


def process_directory(directory, metrics_dir, ref_point, pop_size, generations, nobj):
    """Procesa todos los archivos de un directorio y devuelve HV promedio por generación."""
    seed_files = find_seed_files(directory)
    
    if not seed_files:
        print(f"  No se encontraron archivos en {directory}")
        return None
    
    print(f"  Encontrados {len(seed_files)} archivos")
    
    all_hv_data = {}
    
    for seed_file in seed_files:
        seed_name = os.path.basename(seed_file)
        print(f"    Procesando {seed_name}...", end=" ", flush=True)
        
        # Copiar archivo al directorio de metrics
        dest_file = os.path.join(metrics_dir, seed_name)
        shutil.copy2(seed_file, dest_file)
        
        try:
            hv_data = run_metrics_tool(
                metrics_dir, seed_name, pop_size, generations, nobj, ref_point
            )
            
            if hv_data:
                print("✓")
                for gen, hv in hv_data.items():
                    if gen not in all_hv_data:
                        all_hv_data[gen] = []
                    all_hv_data[gen].append(hv)
            else:
                print("✗")
        finally:
            if os.path.exists(dest_file):
                os.remove(dest_file)
    
    return all_hv_data


def save_results(all_hv_data, output_path, algorithm_name):
    """Guarda los resultados promediados."""
    if not all_hv_data:
        return
    
    num_gens = max(all_hv_data.keys())
    
    with open(output_path, 'w') as f:
        f.write(f"# {algorithm_name} - Hipervolumen promedio por generación\n")
        f.write("# gen\thv_mean\thv_std\thv_min\thv_max\n")
        for gen in range(1, num_gens + 1):
            if gen in all_hv_data:
                hvs = all_hv_data[gen]
                mean_hv = sum(hvs) / len(hvs)
                
                if len(hvs) > 1:
                    variance = sum((x - mean_hv)**2 for x in hvs) / (len(hvs) - 1)
                    std_hv = math.sqrt(variance)
                else:
                    std_hv = 0.0
                
                f.write(f"{gen}\t{mean_hv:.10e}\t{std_hv:.10e}\t{min(hvs):.10e}\t{max(hvs):.10e}\n")
    
    return all_hv_data


def main():
    parser = argparse.ArgumentParser(
        description='Calcula HV promedio usando metrics del profesor con punto de referencia común'
    )
    parser.add_argument('dir1', help='Directorio con archivos del primer algoritmo (MOEA/D)')
    parser.add_argument('dir2', help='Directorio con archivos del segundo algoritmo (NSGA-II)')
    parser.add_argument('--pop_size', type=int, default=40)
    parser.add_argument('--generations', type=int, default=100)
    parser.add_argument('--nobj', type=int, default=2)
    parser.add_argument('--output_dir', type=str, default=None,
                        help='Directorio de salida (default: directorio actual)')
    parser.add_argument('--metrics_dir', type=str, default=None)
    parser.add_argument('--name1', type=str, default='moead', help='Nombre del primer algoritmo')
    parser.add_argument('--name2', type=str, default='nsga2', help='Nombre del segundo algoritmo')
    
    args = parser.parse_args()
    
    # Encontrar directorio de metrics
    script_dir = os.path.dirname(os.path.abspath(__file__))
    metrics_dir = args.metrics_dir or os.path.dirname(script_dir)
    output_dir = args.output_dir or script_dir
    
    if not os.path.exists(os.path.join(metrics_dir, "metrics")):
        print(f"Error: No se encuentra 'metrics' en {metrics_dir}")
        sys.exit(1)
    
    # Encontrar TODOS los archivos de ambos directorios
    files1 = find_seed_files(args.dir1)
    files2 = find_seed_files(args.dir2)
    all_files = files1 + files2
    
    if not all_files:
        print("Error: No se encontraron archivos")
        sys.exit(1)
    
    print(f"Total de archivos encontrados: {len(all_files)}")
    print(f"  - {args.name1}: {len(files1)} archivos")
    print(f"  - {args.name2}: {len(files2)} archivos")
    
    # PASO 1: Encontrar punto de referencia común (peor f1 y f2 de TODOS)
    ref_point = find_global_reference_point(all_files)
    print(f"\n{'='*60}")
    print(f"PUNTO DE REFERENCIA COMÚN (peor f1, peor f2 + 1% margen)")
    print(f"  ref_x = {ref_point[0]:.10f}")
    print(f"  ref_y = {ref_point[1]:.10f}")
    print(f"{'='*60}\n")
    
    # Guardar punto de referencia
    ref_file = os.path.join(output_dir, "ref_point_common.out")
    with open(ref_file, 'w') as f:
        f.write(f"# Punto de referencia común para comparación justa\n")
        f.write(f"# Calculado como el peor f1 y f2 de TODOS los archivos + 1% margen\n")
        f.write(f"{ref_point[0]:.10f}\t{ref_point[1]:.10f}\n")
    print(f"Punto de referencia guardado en: {ref_file}")
    
    # PASO 2: Procesar primer directorio (MOEA/D)
    print(f"\n--- Procesando {args.name1.upper()} ---")
    hv_data1 = process_directory(args.dir1, metrics_dir, ref_point, 
                                  args.pop_size, args.generations, args.nobj)
    
    # PASO 3: Procesar segundo directorio (NSGA-II)
    print(f"\n--- Procesando {args.name2.upper()} ---")
    hv_data2 = process_directory(args.dir2, metrics_dir, ref_point,
                                  args.pop_size, args.generations, args.nobj)
    
    # PASO 4: Guardar resultados
    output1 = os.path.join(output_dir, f"{args.name1}_hv_avg.out")
    output2 = os.path.join(output_dir, f"{args.name2}_hv_avg.out")
    
    save_results(hv_data1, output1, args.name1.upper())
    save_results(hv_data2, output2, args.name2.upper())
    
    print(f"\n✓ Resultados guardados:")
    print(f"  - {output1}")
    print(f"  - {output2}")
    
    # RESUMEN
    print(f"\n{'='*60}")
    print("RESUMEN COMPARATIVO")
    print(f"{'='*60}")
    
    if hv_data1 and hv_data2:
        num_gens = max(max(hv_data1.keys()), max(hv_data2.keys()))
        
        # Primera generación
        hv1_first = hv_data1.get(1, [0])
        hv2_first = hv_data2.get(1, [0])
        mean1_first = sum(hv1_first) / len(hv1_first)
        mean2_first = sum(hv2_first) / len(hv2_first)
        
        # Última generación
        hv1_last = hv_data1.get(num_gens, [0])
        hv2_last = hv_data2.get(num_gens, [0])
        mean1_last = sum(hv1_last) / len(hv1_last)
        mean2_last = sum(hv2_last) / len(hv2_last)
        
        print(f"\n{'Generación':<12} | {args.name1.upper():<15} | {args.name2.upper():<15} | Mejor")
        print(f"{'-'*12}-+-{'-'*15}-+-{'-'*15}-+-{'-'*10}")
        
        winner1 = args.name1.upper() if mean1_first > mean2_first else args.name2.upper()
        print(f"{'Gen 1':<12} | {mean1_first:>15.6f} | {mean2_first:>15.6f} | {winner1}")
        
        winner_last = args.name1.upper() if mean1_last > mean2_last else args.name2.upper()
        print(f"{'Gen ' + str(num_gens):<12} | {mean1_last:>15.6f} | {mean2_last:>15.6f} | {winner_last}")
        
        diff = mean1_last - mean2_last
        print(f"\nDiferencia final: {diff:+.6f} ({args.name1.upper()} - {args.name2.upper()})")
        
        if diff > 0:
            print(f"\n🏆 {args.name1.upper()} tiene mejor hipervolumen final!")
        else:
            print(f"\n🏆 {args.name2.upper()} tiene mejor hipervolumen final!")


if __name__ == "__main__":
    main()
