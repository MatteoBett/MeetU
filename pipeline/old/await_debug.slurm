echo "Preprocess Pocketgen input"
cd $TRANSITION_DIR
python preprocess_pocketgen.py

# Start PocketGen
source activate $POCKETGEN_ENV
cd $POCKETGEN_DIR
python generate_new.py --target input/

#Transfer pocketgen output
cd $TRANSITION_DIR
python transfer_output.py
