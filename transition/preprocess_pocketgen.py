import os, shutil, argparse

def make_reference(path_ref_prot_file : str, path_ref_prot_ligand : str, input_dir : str):
    """
    Create the input directory for the natural ligand and protein
    """
    path, name_prot = os.path.split(path_ref_prot_file)
    path, name_ligand = os.path.split(path_ref_prot_ligand)
    
    global_name = f"{name_prot[:4]}_{name_ligand.split('.')[0]}"
    new_dir = os.path.join(input_dir, global_name)

    if os.path.exists(new_dir):
        shutil.rmtree(new_dir)
    os.makedirs(new_dir)
    
    shutil.copyfile(path_ref_prot_file, os.path.join(new_dir, f"{global_name}.pdb"))
    shutil.copyfile(path_ref_prot_ligand, os.path.join(new_dir, f"{global_name}_ligand.sdf"))

def make_dir_new_ligand(input_dir : str, dir_ligands : str, path_ref_prot_file:str, number : int = 10):
    """
    Create the appropriate directory for the desired number of ligands to test
    """
    for index, ligand_file in enumerate(os.listdir(dir_ligands)):
        path_ligand_file = os.path.join(dir_ligands, ligand_file)

        make_reference(path_ref_prot_file, path_ligand_file, input_dir)
        if index == number:
            print(f"Ended at number {number} with file {ligand_file}")
            return

def change_in_dir_names(input_dir : str):
    """
    Adjust file naming for a PocketGen-friendly format
    """

    for folder in os.listdir(input_dir):
        for in_folder in os.listdir(os.path.join(input_dir, folder)):
            if (not in_folder.endswith('.pdb') and not in_folder.endswith('.sdf')) or len(os.listdir(os.path.join(input_dir, folder))) > 4:
                continue
            path_infolder = os.path.join(input_dir, folder)
            current_file_path = os.path.join(path_infolder, in_folder)
            if '_' in in_folder:
                os.rename(current_file_path, os.path.join(path_infolder, f"{folder}_ligand.sdf"))
            
            else:
                os.rename(current_file_path, os.path.join(path_infolder, f"{folder}.pdb"))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_pocketgen', type=str, default='/shared/projects/2428_meet_eu/matteo/PocketGen/input', help='Directory where the input of PocketGen is stored')
    
    parser.add_argument('--output_docking_prot', type=str, default='/shared/projects/2428_meet_eu/matteo/docking/data/5wyq_prot.pdb', help = '.pdb File containing the protein to which the ligands were docked')
    
    parser.add_argument('--output_docking_ligand_ref', type=str, default='/shared/projects/2428_meet_eu/matteo/docking/data/5wyq_lig1.sdf', help = '.sdf File containing the natural ligand for the protein of interest')

    parser.add_argument('--output_docking_ligand', type=str, default='/shared/projects/2428_meet_eu/matteo/docking/output/ligand_exp_docked', help = 'Directory were the docked ligands are stored')
    parser.add_argument('--number', type=int, default=115, help = 'Number of ligands you would like to transfer for pocket comparison')
    args = parser.parse_args()
    
    input_dir = args.input_pocketgen
    ref_prot = args.output_docking_prot
    ref_lig = args.output_docking_ligand_ref
    dir_all_lig = args.output_docking_ligand
    number = args.number

    change_in_dir_names(input_dir)
    make_reference(ref_prot, ref_lig, input_dir)
    make_dir_new_ligand(input_dir, dir_all_lig, ref_prot, number = number)

