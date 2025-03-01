#!/bin/bash

#SBATCH --array=0-125        # Array of jobs
#SBATCH -A 2428_meet_eu
#SBATCH -o stdout/run_gnina_para.%A.%a.out
#SBATCH --partition=fast
#SBATCH --mem 32GB

target_folder=/shared/projects/2428_meet_eu/matteo/docking/data/ligand_experiment_all
output_folder=/shared/projects/2428_meet_eu/matteo/docking/output/ligand_exp_docked

target_ligand=$target_folder/ligand_$SLURM_ARRAY_TASK_ID.sdf
output=$output_folder/ligands_$SLURM_ARRAY_TASK_ID.sdf

target_prot=/shared/projects/2428_meet_eu/matteo/docking/data/5wyq_prot.pdb
bound_ligand=/shared/projects/2428_meet_eu/matteo/docking/data/5wyq_lig1.pdb

SIMAGES=/shared/projects/2428_meet_eu/florence_home/singularity_images

mkdir -p $output_folder

singularity exec $SIMAGES/gnina.sif gnina -r $target_prot -l $target_ligand --autobox_ligand $bound_ligand -o $output --num_modes 1

echo "Done!"
