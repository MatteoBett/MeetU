import os, shutil

def send_matrix(src_path : str = '/shared/projects/2428_meet_eu/matteo/epocs/tmp/distance_matrix.npz', 
                end_path : str = '/shared/projects/2428_meet_eu/matteo/epocs/distance_mat'):
    
    base_src = '/'.join(src_path.split('/')[:-1])
    if len(os.listdir(end_path)) != 0:
        num = len(os.listdir(end_path))
    else:
        num = 0
    
    new_name = src_path.split('.')[0] + f'_{int(num)+1}.npz'
    end_path = os.path.join(end_path, new_name.split('/')[-1])
    
    os.rename(src_path, new_name)
    shutil.copyfile(new_name, end_path)

if __name__ == "__main__":
    
    try :
        send_matrix()
        print("moved matrix")
    except Exception:
        print("no matrix to move")
    
    if os.path.exists(r'/shared/projects/2428_meet_eu/matteo/epocs/clusters'):
        shutil.rmtree(r'/shared/projects/2428_meet_eu/matteo/epocs/clusters')
        
    if os.path.exists(r'/shared/projects/2428_meet_eu/matteo/epocs/embeddings'):
        shutil.rmtree(r'/shared/projects/2428_meet_eu/matteo/epocs/embeddings')
        
    if os.path.exists(r'/shared/projects/2428_meet_eu/matteo/epocs/pocket_embeddings'):
        shutil.rmtree(r'/shared/projects/2428_meet_eu/matteo/epocs/pocket_embeddings')
        
    if os.path.exists(r'/shared/projects/2428_meet_eu/matteo/epocs/pocket_residues'):
        shutil.rmtree(r'/shared/projects/2428_meet_eu/matteo/epocs/pocket_residues')
        
    if os.path.exists(r'/shared/projects/2428_meet_eu/matteo/epocs/sequences'):
        shutil.rmtree(r'/shared/projects/2428_meet_eu/matteo/epocs/sequences')
        
    if os.path.exists(r'/shared/projects/2428_meet_eu/matteo/epocs/tmp'):
        shutil.rmtree(r'/shared/projects/2428_meet_eu/matteo/epocs/tmp')
        
