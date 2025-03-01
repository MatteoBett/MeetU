#!/bin/bash

#SBATCH -p gpu
#SBATCH --gres gpu:7g.40gb:1
#SBATCH -N 1
#SBATCH -n 32
#SBATCH --mem 128G
#SBATCH -t 0-48:00
#SBATCH -e error.err
#SBATCH -o output.out

POCKETGEN_ENV="pocketgen"
POCKETGEN_DIR="/shared/projects/2428_meet_eu/matteo/Pocketgen/"

module load conda
source activate $POCKETGEN_ENV

echo Properly activated 

python generate_new.py --target input/
