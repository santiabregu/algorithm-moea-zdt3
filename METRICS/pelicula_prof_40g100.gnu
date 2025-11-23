set term wxt size 900,700
set xlabel "f1"
set ylabel "f2"
set xrange [0:1]
set yrange [0:6]
set grid

popsize = 40
gen = 99     # última generación (0–99)

start = gen*popsize
end = start + popsize - 1

plot "zdt3_all_popmp40g100_seed01.out" every ::start::end using 1:2 \
     with points pt 7 ps 1 lc rgb "red" title "Frente final profesor"

pause -1 "Pulsa ENTER para cerrar"
