# Comparación del Frente de Pareto Final (Generación 100)
set term qt size 1000,700
set title "Frente de Pareto Final (Generación 100) - MOEA/D vs NSGA-II"
set xlabel "f1"
set ylabel "f2"
set xrange [0:1]
set yrange [-0.5:1.5]
set grid
set key top right

popsize = 40
gens = 100

# Última generación = líneas 3961 a 4000
start = (gens-1)*popsize + 1
end = gens*popsize

plot "zdt3_seed1_personal_N40G100.out" every ::start::end using 1:2 with points pt 7 ps 1.5 lc rgb "blue" title "MOEA/D (tuyo)", \
     "zdt3_seed1_prof_N40G100.out" every ::start::end using 1:2 with points pt 6 ps 1.5 lc rgb "red" title "NSGA-II (profesor)"

pause -1 "Presiona Enter para cerrar..."

