import os
import json

def load_progress(PROGRESS_FILE):
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r') as file:
            data = json.load(file)
            return data.get('learnt_dict', {}), data.get('mistake_dict', {}), data.get('tested_dict', {})
    else:
        return {}, {}, {}
    
def save_progress(learnt_dict, mistake_dict, tested_dict, PROGRESS_FILE):
    with open(PROGRESS_FILE, 'w') as file:
        json.dump({'learnt_dict': learnt_dict, 'mistake_dict': mistake_dict, 'tested_dict': tested_dict}, file)
