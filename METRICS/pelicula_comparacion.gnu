set term qt size 1000,700
set xlabel "f1"
set ylabel "f2"
set xrange [0:1]
set yrange [-0.5:6]
set grid

popsize = 40
gens = 100

do for [g=0:gens-1] {
    start = g*popsize + 1
    end = (g+1)*popsize

    set title sprintf("Generación %d / %d", g+1, gens) font ",14"
    
    plot "zdt3_seed1_personal_N40G100.out" every ::start::end using 1:2 with points pt 7 ps 1.3 lc rgb "#0066CC" title "MOEA/D", \
         "zdt3_seed1_prof_N40G100.out" every ::start::end using 1:2 with points pt 6 ps 1.3 lc rgb "#CC0000" title "NSGA-II"

    pause 0.12
}

pause -1 "Presiona Enter para cerrar..."

