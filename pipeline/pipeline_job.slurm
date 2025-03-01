#!/bin/bash
#
#SBATCH -A 2428_meet_eu
#SBATCH -p gpu # partition (can be gpu)
#SBATCH --gres gpu:3g.20gb:1
#SBATCH -N 1
#SBACTH -n 32
#SBATCH --mem 128GB # mémoire vive pour l'ensemble des cœurs
#SBATCH -t 0-48:00 # durée maximum du travail (D-HH:MM)
#SBATCH -o output_slurm.out # STDOUT
#SBATCH -e error_slurm.err # STDERR

POCKETGEN_ENV="pocketgen"
EPOCS_ENV="epocs"

TRANSITION_DIR="/shared/projects/2428_meet_eu/matteo/transition/"
EPOCS_DIR="/shared/projects/2428_meet_eu/matteo/epocs/"
POCKETGEN_DIR="/shared/projects/2428_meet_eu/matteo/PocketGen/"

echo "Preprocess Pocketgen input"
cd $TRANSITION_DIR
#python preprocess_pocketgen.py

echo "Preprocessing done!"

# Start PocketGen
source activate $POCKETGEN_ENV
cd $POCKETGEN_DIR
#python generate_new.py --target input/

echo "Transfering PocketGen results"
#Transfer pocketgen output
cd $TRANSITION_DIR
python transfer_output.py

echo "Starting Pocket comparison"
module load conda
conda deactivate

source activate $EPOCS_ENV
cd $EPOCS_DIR

python run_epocs.py -f ./input/protein_list.txt -pp ./param/esm2_t36_3B_UR50D.pt -sr False -np 8 -dm True -pd ./distance_mat

echo "Post-processing epocs"
cd $TRANSITION_DIR
#python removal.py

python save_fig.py
echo done
