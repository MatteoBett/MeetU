#!/bin/bash

conda install conda-forge::pymol-open-source
pip3 install torch torchvision torchaudio
conda install biopandas pytest scipy tqdm -c conda-forge
pip install fair-esm
pip install faerun
