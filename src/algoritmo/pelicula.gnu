set term qt size 900,700
set xlabel "f1"
set ylabel "f2"
set xrange [0:1]
set yrange [0:6]
set grid

popsize = 40
gens = 100

do for [g=0:gens-1] {
    start = g*popsize + 1
    end = (g+1)*popsize

    plot "all_popm.out" every ::start::end using 1:2 with points pt 7 ps 1 lc rgb "blue" title sprintf("Gen %d", g)

    pause 0.1
}
