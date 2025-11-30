# Comparación de evolución del Hypervolume: MOEA/D vs NSGA-II
set term qt size 1000,600
set title "Evolución del Hypervolume - MOEA/D vs NSGA-II (promedio 10 semillas)"
set xlabel "Generación"
set ylabel "Hypervolume"
set grid
set key top left

# Leer los archivos de promedios
plot "utils/moead_hv_avg.out" using 1:2 with lines lw 2 lc rgb "blue" title "MOEA/D", \
     "utils/nsga2_hv_avg.out" using 1:2 with lines lw 2 lc rgb "red" title "NSGA-II"

pause -1 "Presiona Enter para cerrar..."

