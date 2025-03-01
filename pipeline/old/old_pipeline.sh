#!/bin/bash

echo "Preprocess Pocketgen input"

python /shared/projects/2428_meet_eu/matteo/transition/preprocess_pocketgen.py


# Start PocketGen
conda activate /shared/projects/2428_meet_eu/conda/envs/pocketgen
python /shared/projects/2428_meet_eu/matteo/PocketGen/generate_new.py --target /shared/projects/2428_meet_eu/matteo/PocketGen/input/
conda deactivate pocketgen

#Transfer pocketgen output
python /shared/projects/2428_meet_eu/matteo/transition/transfer_output.py

echo "Starting Pocket comparison"
conda activate /shared/projects/2428_meet_eu/conda/envs/epocs
python run_epocs.py -f /shared/projects/2428_meet_eu/matteo/epocs/input/pocket_list.txt -pp ./param/esm2_t36_3B_UR50D.pt -np 8 -dm True -pd ./distance_mat
conda deactivate epocs

echo "Post-processing epocs"
python /shared/projects/2428_meet_eu/matteo/transition/removal.py


