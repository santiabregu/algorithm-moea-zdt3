set term x11 size 900,700
set xlabel "f1"
set ylabel "f2"
set xrange [0:1]
set yrange [0:6]
set grid

popsize = 40
gen = 50

start = gen*popsize + 1
end = (gen+1)*popsize

plot "all_popm.out" every ::start::end using 1:2 with points pt 7 ps 1 lc rgb "blue" title sprintf("Generación %d", gen)
