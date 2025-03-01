import os, shutil
from typing import Dict

from MolKit import Read
from MolKit import mmcifWriter
from rdkit import Chem
from pymatgen.core import Structure
from pymatgen.io.cif import CifWriter


def remove_contact_author_line(input_file : str, output_file : str):
    """
    Removes the line containing `_software.contact_author` from a CIF file.
    """
    try:
        with open(input_file, 'r') as file:
            lines = file.readlines()

        modified_lines = [line for line in lines if not line.strip().startswith('_software.contact_author')]

        with open(output_file, 'w') as file:
            file.writelines(modified_lines)

    except Exception as e:
        print(f"An error occurred in deleting unproper field in file: {e}")

def sdf_to_cif(sdf_file : str, cif_file : str):
    suppl = Chem.SDMolSupplier(sdf_file, removeHs=False)
    
    for mol in suppl:
        if mol is not None:
            conf = mol.GetConformer()
            atom_symbols = [atom.GetSymbol() for atom in mol.GetAtoms()]
            coords = [conf.GetAtomPosition(i) for i in range(mol.GetNumAtoms())]

            structure = Structure(lattice=[[10, 0, 0], [0, 10, 0], [0, 0, 10]],  # Dummy cubic lattice
                                  species=atom_symbols,
                                  coords=coords,
                                  coords_are_cartesian=True)

            # Write to CIF
            CifWriter(structure).write_file(cif_file)
        else:
            print("mol is None")
def file_conversion(dico_link : Dict[str, str]):
    """
    Subprocesses to convert the files in .cif format from .pdbqt
    """
    for key, target in dico_link.items():
        # Load the PDBQT file
        try :
            molecule = Read(key)[0]
            client = mmcifWriter.MMCIFWriter()
            client.write(target, molecule)
        
        except Exception:
            sdf_to_cif(key, target)

        remove_contact_author_line(target, target)
        
    return target 

def identify_files(
                   root_Pocketgen_data_dir : str = r'/shared/projects/2428_meet_eu/matteo/PocketGen/input'
                   ):
    """
    Identify the output files to select for further analysis, and reconstruct 
    their absolute path.
    """
    for index, data_dir in enumerate(os.listdir(root_Pocketgen_data_dir)): 
        assert os.path.exists(root_Pocketgen_data_dir), "Pocketgen output does not exist"
        gen_lig, gen_pro = os.path.join(root_Pocketgen_data_dir, data_dir, "7.pdb"), os.path.join(root_Pocketgen_data_dir, data_dir, "7_docked.pdbqt")
        ori_lig, ori_pro = os.path.join(root_Pocketgen_data_dir, data_dir, "7_orig.pdb"), os.path.join(root_Pocketgen_data_dir, data_dir, "7.sdf")
        yield [gen_lig, gen_pro], [ori_lig, ori_pro], data_dir


def send_files(
               epocs_dir : str = r'/shared/projects/2428_meet_eu/matteo/epocs/input',
               pocketgen_dir : str = r'/shared/projects/2428_meet_eu/matteo/PocketGen/input'
               ):
    """
    Send the files to the wanted directory, i.e. differentially depending
    on whether they are proteins or ligand.
    """
    if not os.path.exists(epocs_dir):
        os.makedirs(epocs_dir)
    else:
        shutil.rmtree(epocs_dir)
        os.makedirs(epocs_dir)

    prot_dir = os.path.join(epocs_dir, "prot")
    ligand_dir = os.path.join(epocs_dir, "ligand")

    if not os.path.exists(prot_dir):
        os.makedirs(prot_dir)
    else:
        shutil.rmtree(prot_dir)
        os.makedirs(prot_dir)
    if not os.path.exists(ligand_dir):
        os.makedirs(ligand_dir)
    else:
        shutil.rmtree(ligand_dir)
        os.makedirs(ligand_dir)

    for list_gen_outpath, list_ori_outpath, ligand_name in identify_files(root_Pocketgen_data_dir=pocketgen_dir):
        gen_prot_file = os.path.join(prot_dir, f"DIP_prot_{ligand_name}.cif")
        gen_ligand_file = os.path.join(ligand_dir, f"DIP_lig_{ligand_name}.cif")

        ori_prot_file = os.path.join(prot_dir, f"DNP_prot_{ligand_name}.cif")
        ori_ligand_file = os.path.join(ligand_dir, f"DNP_lig_{ligand_name}.cif")
        
        dico_link = dict(zip(list_gen_outpath + list_ori_outpath, [gen_prot_file, gen_ligand_file] + [ori_prot_file, ori_ligand_file]))
        
        output_pdb_path = file_conversion(dico_link)
        
    return output_pdb_path, dico_link


def write_association_list(epocs_dir : str = r'/shared/projects/2428_meet_eu/matteo/epocs/input'):
    """
    Write the protein file associated to its ligand in a .txt file. 
    Left column is for the protein file relative path, right column is for the 
    ligand file relative path

    Notes on PocketGen output:

    7.pdb is the generated pocket
    7_docked.sdf is the ligand docked to the new pocket

    7_orig.pdb is the original pocket
    7.sdf is the original ligand docking
    """
    
    ligand_dir = os.path.join(epocs_dir, "ligand")
    prot_dir = os.path.join(epocs_dir, "prot")
    
    dico = dict(zip(
        sorted([os.path.join(prot_dir, prot_file) for prot_file in os.listdir(prot_dir)]),
        sorted([os.path.join(ligand_dir, ligand_file) for ligand_file in os.listdir(ligand_dir)])
        ))
    with open(os.path.join(epocs_dir, 'protein_list.txt'), 'w') as association_file:
        for key, value in dico.items():
            association_file.write(f"{key} {value}\n")

if __name__ == '__main__':
    print("Transfer started")
    send_files()

    write_association_list()
