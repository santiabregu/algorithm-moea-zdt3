### TERMINAL ###
set term wxt size 900,700

### ETIQUETAS ###
set xlabel "f1"
set ylabel "f2"
set title "Comparación última generación (Gen 100)"
set grid

### AJUSTES ###
set xrange [0:1]
set yrange [0:6]

popsize = 40
gen = 100

# Cálculo del rango de líneas de la generación 100 (0-index)
start = gen * popsize
end   = start + popsize - 1

### PLOT ###
plot \
    "all_popm.out" using 1:2 every ::start::end with points pt 7 ps 1 lc rgb "red"   title "Mi MOEA/D (Gen 100)", \
    "zdt3_all_popmp40g100_seed01.out" using 1:2 every ::start::end with points pt 7 ps 1 lc rgb "blue"  title "Profesor (Gen 100)"
