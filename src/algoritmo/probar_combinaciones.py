#!/usr/bin/env python3
"""
Script para probar combinaciones de parámetros de forma sistemática.
Compara con V6.5 (base) y NSGA-II.
"""

import subprocess
import os
import shutil

# Combinaciones a probar
COMBINACIONES = {
    "V6.5_base": {
        "pm": 1/20,
        "de_prob": 0.2,
        "perturbacion_pesos": 0.02,
        "max_reemplazos": 2,
        "T_percent": 0.225,
        "descripcion": "Base (óptima individual)"
    },
    "V7.1_mas_exploracion": {
        "pm": 1/18,
        "de_prob": 0.3,
        "perturbacion_pesos": 0.03,
        "max_reemplazos": 2,
        "T_percent": 0.225,
        "descripcion": "Más exploración: pm↑, DE↑, perturb↑"
    },
    "V7.2_mejor_distribucion": {
        "pm": 1/20,
        "de_prob": 0.2,
        "perturbacion_pesos": 0.03,
        "max_reemplazos": 2,
        "T_percent": 0.25,
        "descripcion": "Mejor distribución: perturb↑, T↑"
    },
    "V7.3_balance": {
        "pm": 1/18,
        "de_prob": 0.25,
        "perturbacion_pesos": 0.025,
        "max_reemplazos": 2,
        "T_percent": 0.25,
        "descripcion": "Balance: todos moderadamente ↑"
    },
    "V7.4_exploracion_extrema": {
        "pm": 1/15,
        "de_prob": 0.3,
        "perturbacion_pesos": 0.04,
        "max_reemplazos": 3,
        "T_percent": 0.25,
        "descripcion": "Exploración extrema: todos ↑↑"
    }
}

def modificar_main_py(version, params):
    """Modifica main.py con los parámetros de la combinación."""
    main_py = "main.py"
    
    # Leer archivo
    with open(main_py, 'r') as f:
        content = f.read()
    
    # Reemplazar parámetros en la llamada a ejecutar_moead
    old_call = """        # V6.5 (base): parámetros óptimos encontrados
        pop, fit, z, historial = ejecutar_moead(
            N=N, 
            generaciones=generaciones, 
            perturbacion_pesos=0.02,
            pm=1/20,
            de_prob=0.2,
            max_reemplazos=2,
            T_percent=0.225
        )"""
    
    new_call = f"""        # {version}: {params['descripcion']}
        pop, fit, z, historial = ejecutar_moead(
            N=N, 
            generaciones=generaciones, 
            perturbacion_pesos={params['perturbacion_pesos']},
            pm={params['pm']},
            de_prob={params['de_prob']},
            max_reemplazos={params['max_reemplazos']},
            T_percent={params['T_percent']}
        )"""
    
    content = content.replace(old_call, new_call)
    
    # Escribir archivo
    with open(main_py, 'w') as f:
        f.write(content)

def ejecutar_y_guardar(version):
    """Ejecuta el algoritmo y guarda resultados en carpeta version."""
    print(f"\n{'='*60}")
    print(f"Ejecutando {version}...")
    print(f"{'='*60}")
    
    # Ejecutar
    result = subprocess.run(
        ["python3", "main.py"],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print(f"ERROR ejecutando {version}:")
        print(result.stderr)
        return False
    
    # Crear carpeta y mover archivos
    os.makedirs(version, exist_ok=True)
    for f in os.listdir("."):
        if f.startswith("zdt3_") and f.endswith(".out"):
            shutil.move(f, os.path.join(version, f))
    
    print(f"✓ {version} completado")
    return True

def comparar_con_metrics(version):
    """Compara con NSGA-II usando ./metrics."""
    metrics_dir = "../../METRICS"
    seed01_file = f"{version}/zdt3_all_popmp40g100_seed01.out"
    dest_file = os.path.join(metrics_dir, "zdt3_seed1_personal_N40G100.out")
    
    if not os.path.exists(seed01_file):
        print(f"ERROR: No existe {seed01_file}")
        return None
    
    # Copiar a METRICS
    shutil.copy2(seed01_file, dest_file)
    
    # Ejecutar metrics
    cmd = """printf "2\\n1\\n2\\nzdt3_seed1_personal_N40G100.out\\n40\\n100\\nzdt3_seed1_prof_N40G100.out\\n40\\n100\\n0\\n1.0096\\n6.2945\\n" | ./metrics 2>/dev/null"""
    
    result = subprocess.run(
        cmd,
        shell=True,
        cwd=metrics_dir,
        capture_output=True,
        text=True
    )
    
    # Leer resultados
    try:
        with open(os.path.join(metrics_dir, "hypervol.out"), 'r') as f:
            hv_line = f.readlines()[-1].strip()
            hv = float(hv_line.split()[1])
        
        with open(os.path.join(metrics_dir, "spacing.out"), 'r') as f:
            sp_line = f.readlines()[-1].strip()
            spacing = float(sp_line.split()[1])
        
        with open(os.path.join(metrics_dir, "cs2.out"), 'r') as f:
            cs2_line = f.readlines()[-1].strip()
            cs2 = float(cs2_line.split()[1])
        
        return {
            "hv": hv,
            "spacing": spacing,
            "cs2": cs2
        }
    except Exception as e:
        print(f"ERROR leyendo resultados: {e}")
        return None

if __name__ == "__main__":
    resultados = {}
    
    for version, params in COMBINACIONES.items():
        print(f"\n{'#'*60}")
        print(f"# {version}: {params['descripcion']}")
        print(f"{'#'*60}")
        
        # Modificar main.py
        modificar_main_py(version, params)
        
        # Ejecutar
        if ejecutar_y_guardar(version):
            # Comparar
            res = comparar_con_metrics(version)
            if res:
                resultados[version] = res
                print(f"  HV: {res['hv']:.3f}")
                print(f"  Spacing: {res['spacing']:.3f}")
                print(f"  CS2: {res['cs2']*100:.1f}%")
    
    # Resumen final
    print(f"\n{'='*60}")
    print("RESUMEN FINAL")
    print(f"{'='*60}")
    print(f"{'Versión':<25} {'HV':<10} {'Spacing':<10} {'CS2':<10} {'Mejor CS2'}")
    print("-" * 60)
    
    mejor_cs2 = min([r['cs2'] for r in resultados.values()])
    
    for version, res in resultados.items():
        mejor = "✓" if res['cs2'] == mejor_cs2 else ""
        print(f"{version:<25} {res['hv']:<10.3f} {res['spacing']:<10.3f} {res['cs2']*100:<10.1f}% {mejor}")

