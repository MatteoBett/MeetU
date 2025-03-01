#!/bin/bash

#SBATCH -p gpu
#SBATCH --gres gpu:3g.20gb:1
#SBATCH -N 1
#SBATCH -n 8
#SBATCH --mem 64G
#SBATCH -t 0-2:00
#SBATCH -o output_slurm.out # STDOUT
#SBATCH -e error.err

EPOCS_ENV="epocs"

module load conda
source activate $EPOCS_ENV

#python run_epocs.py -h

echo Properly activated
python run_epocs.py -f ./input/protein_list.txt -pp ./param/esm2_t36_3B_UR50D.pt -np 8 -sr False -dm True -pd ./distance_mat

