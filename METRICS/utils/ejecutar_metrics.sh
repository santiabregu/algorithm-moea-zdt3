#!/bin/bash
# Script para ejecutar ./metrics de forma no interactiva

cd "$(dirname "$0")/.."

file1="$1"
file2="$2"
pop_size="$3"
gens="$4"
nobj="$5"

if [ -z "$file1" ] || [ -z "$file2" ] || [ -z "$pop_size" ] || [ -z "$gens" ] || [ -z "$nobj" ]; then
    echo "Uso: $0 <file1> <file2> <pop_size> <gens> <nobj>"
    exit 1
fi

# Ejecutar metrics con entrada automática
{
    echo "2"      # Comparar dos ejecuciones
    sleep 0.1
    echo "1"      # Todas las generaciones
    sleep 0.1
    echo "$nobj"  # Número de objetivos
    sleep 0.1
    echo "$file1" # Primer archivo
    sleep 0.1
    echo "$pop_size" # Tamaño de población
    sleep 0.1
    echo "$file2" # Segundo archivo
    sleep 0.1
    echo "$pop_size" # Tamaño de población
} | ./metrics "$file1" "$file2" "$pop_size" "$gens" "$nobj" 2>&1

