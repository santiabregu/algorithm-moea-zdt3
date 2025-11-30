set term qt size 900,700
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

    set title sprintf("NSGA-II (Profesor) - Generación %d", g+1)
    
    plot "zdt3_seed1_prof_N40G100.out" every ::start::end using 1:2 with points pt 7 ps 1.5 lc rgb "red" title "NSGA-II"

    pause 0.1
}

pause -1 "Presiona Enter para cerrar..."

