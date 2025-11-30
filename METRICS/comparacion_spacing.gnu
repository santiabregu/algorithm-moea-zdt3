# Comparación de Spacing: MOEA/D vs NSGA-II
set term qt size 1000,600
set title "Evolución del Spacing - MOEA/D vs NSGA-II (seed01)"
set xlabel "Generación"
set ylabel "Spacing (menor = mejor distribución)"
set grid
set key top right

plot "spacing.out" using 1:2 with lines lw 2 lc rgb "blue" title "MOEA/D", \
     "spacing2.out" using 1:2 with lines lw 2 lc rgb "red" title "NSGA-II"

pause -1 "Presiona Enter para cerrar..."

