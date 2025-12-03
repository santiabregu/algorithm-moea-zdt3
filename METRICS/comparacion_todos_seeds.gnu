# Comparación del Frente de Pareto Final (Gen 100) - TODOS LOS SEEDS
# Muestra todos los puntos de todas las semillas para ver variabilidad

set term qt size 1200,800
set title "Frente de Pareto Final (Gen 100) - Todos los Seeds - MOEA/D V8.6 vs NSGA-II" font ",16"
set xlabel "f1" font ",12"
set ylabel "f2" font ",12"
set xrange [0:1]
set yrange [-0.5:1.5]
set grid
set key top right font ",11"

# Primero combinar todos los seeds de MOEA/D
system("cd utils && bash combinar_todos_seeds.sh")

# Plotear todos los puntos de MOEA/D (todos los seeds) y NSGA-II (seed01)
# MOEA/D: puntos más pequeños y semi-transparentes para ver densidad
# NSGA-II: puntos más grandes y opacos para destacar
plot "utils/todos_seeds_gen100_moead.out" using 1:2 with points pt 7 ps 0.6 lc rgb "#0066CC" title "MOEA/D V8.6 (todos seeds, 400 puntos)", \
     "zdt3_seed1_prof_N40G100.out" every ::3961::4000 using 1:2 with points pt 6 ps 1.3 lc rgb "#CC0000" title "NSGA-II (seed01, 40 puntos)"

pause -1 "Presiona Enter para cerrar..."

