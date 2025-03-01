import os
from urllib.request import urlretrieve

MSA_PATH = r"./fold_seek_results"
OUTPUT_PDB = r"./pdb_foldseek"

def scrapper(msa_dir : str, output_dir : str):
    url = "https://files.rcsb.org/view/"
    file = os.path.join(msa_dir, "alis_pdb100.m8")
    with open(file, 'r', encoding='utf-8') as filetemp:
        filetemp = [line.split()[1] for line in filetemp.readlines()]

    for name in filetemp:
        name = name[:4]
        print(f"downloading {name}")
        full_url = url + name + ".pdb"
        name = f"{name}.pdb"
        urlretrieve(full_url, os.path.join(output_dir, name))

scrapper(MSA_PATH, OUTPUT_PDB)
