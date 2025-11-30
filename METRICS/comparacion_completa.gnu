# Comparación Completa: HV + Spacing + Frente Final
set term qt size 1400,900

set multiplot layout 2,2 title "Comparación MOEA/D vs NSGA-II" font ",16"

# --- Gráfico 1: Evolución del Hypervolume ---
set title "Hypervolume (mayor = mejor)"
set xlabel "Generación"
set ylabel "HV"
set grid
set key top left
plot "utils/moead_hv_avg.out" using 1:2 with lines lw 2.5 lc rgb "#0066CC" title "MOEA/D", \
     "utils/nsga2_hv_avg.out" using 1:2 with lines lw 2.5 lc rgb "#CC0000" title "NSGA-II"

# --- Gráfico 2: Evolución del Spacing ---
set title "Spacing (menor = mejor)"
set xlabel "Generación"
set ylabel "Spacing"
set key top right
plot "spacing.out" using 1:2 with lines lw 2.5 lc rgb "#0066CC" title "MOEA/D", \
     "spacing2.out" using 1:2 with lines lw 2.5 lc rgb "#CC0000" title "NSGA-II"

# --- Gráfico 3: Frente Final ---
set title "Frente de Pareto Final (Gen 100)"
set xlabel "f1"
set ylabel "f2"
set xrange [0:1]
set yrange [-0.5:1.5]
set key top right

popsize = 40
gens = 100
start = (gens-1)*popsize + 1
end = gens*popsize

plot "zdt3_seed1_personal_N40G100.out" every ::start::end using 1:2 with points pt 7 ps 1.3 lc rgb "#0066CC" title "MOEA/D", \
     "zdt3_seed1_prof_N40G100.out" every ::start::end using 1:2 with points pt 6 ps 1.3 lc rgb "#CC0000" title "NSGA-II"

# --- Gráfico 4: Coverage Set ---
set title "Coverage Set"
set xlabel "Generación"
set ylabel "Fracción dominada"
set xrange [1:100]
set yrange [0:1]
set key top right
plot "cs.out" using 1:2 with lines lw 2.5 lc rgb "#0066CC" title "NSGA-II dom. por MOEA/D", \
     "cs2.out" using 1:2 with lines lw 2.5 lc rgb "#CC0000" title "MOEA/D dom. por NSGA-II"

unset multiplot
pause -1 "Presiona Enter para cerrar..."

