import numpy as np
import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt
import os, re, json
from typing import Dict
import argparse

sns.set_theme("paper")

def load_distance_matrix(path : str):
    return np.load(path)

def prepare_frame(pmat : np.matrix, path_json_ref : str, prefix : str = "lig_5wyq_"):
    with open(path_json_ref) as jsonfile:
        dico_ref = json.load(jsonfile)
    print(len(dico_ref))
    names = [re.sub(prefix, "", elt.split('.')[0]) for elt in dico_ref.keys()]
    
    pmatrix = pmat["arr_0"]
    print(pmatrix.shape)
    pline = names
    pcol = names

    return pd.DataFrame(data=pmatrix, columns=pcol, index=pline)

def make_dico(pdf_res : pd.DataFrame, target : str = "5wyq_lig1"):
    dico_dist_to_own = {i[4:] : {'x' : -1, 'y':-1} for i in pdf_res.columns}
    target_nat = f'DNP_{target}'
    target_ide = f'DIP_{target}'
     
    for key in dico_dist_to_own.keys():
        for col in pdf_res.columns:
            if key in col and 'DIP' in col:
                dico_dist_to_own[key]['x'] = pdf_res.loc[f'DNP_{key}', col]
            
            if col == target_nat:
                dico_dist_to_own[key]['y'] = pdf_res.loc[f'DIP_{key}', target_nat]
    return dico_dist_to_own

def plot_distribution(dico_ref : Dict[str, float]):
    x_vals = [dico_ref[key]['x'] for key in dico_ref]
    y_vals = [dico_ref[key]['y'] for key in dico_ref]
    xmax = max(x_vals)*1.5
    ymax = max(y_vals)*1.5

    plt.figure(figsize=(6, 6))
    plt.scatter(x_vals, y_vals, color='blue')
    plt.hlines(y=dico_ref[target]['y'], xmin=0, xmax=xmax, colors='r', label="Natural ligand's limits")
    plt.vlines(x=dico_ref[target]['x'], ymin=0, ymax=ymax, colors='r')
    plt.xlim(0, xmax)
    plt.ylim(0, ymax)

    for key in dico_ref:
        plt.text(dico_ref[key]['x'], dico_ref[key]['y'], key.split('_')[1], fontsize=6, ha='right')

    plt.xlabel("Distance to the ligand's own IP")
    plt.ylabel("Ligand's IP distance to TrmD NP")
    plt.title("Ligand's pocket distance to their IP respect to the natural ligand")

    plt.grid(True)
    plt.legend()

    plt.savefig(r"/shared/projects/2428_meet_eu/matteo/epocs/distance_mat/plot_pockets.png", dpi=600)  

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Draw the relative cross-similarity between pockets for a given ligand respect to their Ideal Pocket or the natural pocket of the target protein")

    parser.add_argument("-i", "--input_dir", help="Path to the matrix file containing the distance between pockets", type=str, default='/shared/projects/2428_meet_eu/matteo/epocs/tmp/distance_matrix.npz')
    parser.add_argument('-j', '--json_file', help='Path to the directory json with inside the order of the pockets in the matrix', type=str, default='/shared/projects/2428_meet_eu/matteo/epocs/tmp')
    parser.add_argument("-p", "--prefix", help="Prefix of the ligand", type=str, default='lig_5wyq_')
    parser.add_argument('-t', '--target', help='The filename containig the natural ligand', type=str, default='5wyq_lig1')

    args = parser.parse_args()
    path_to_mat = args.input_dir
    path_to_json = args.json_file
    prefix = args.prefix
    target = args.target

    path_to_json = os.path.join(path_to_json, os.listdir(path_to_json)[0])

    dist_mat = load_distance_matrix(path_to_mat)
    df = prepare_frame(dist_mat, path_to_json, prefix)
    dico = make_dico(df, target)
    plot_distribution(dico)
