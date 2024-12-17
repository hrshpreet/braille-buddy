import string

import module_gpio
import module_audio
import module_progress
import mode_learn
import mode_test

PROGRESS_FILE = 'progress.json'

def main():
    learnt_dict, mistake_dict, tested_dict = module_progress.load_progress(PROGRESS_FILE)
    
    while(True):
        module_audio.say("Choose a mode: Learn, Test or Exit.")
        mode = module_audio.recognize_word();
        
        module_progress.save_progress(mistake_dict=mistake_dict, learnt_dict=learnt_dict, tested_dict=tested_dict, PROGRESS_FILE=PROGRESS_FILE)
        
        print(mode)
        
        if mode == ('learn', True):
            mode_learn.run_learn_mode(module_gpoi=module_gpio, module_audio=module_audio, mistake_dict=mistake_dict, learnt_dict=learnt_dict)
        
        elif mode == ('test', True):
            mode_test.run_test_mode(module_gpoi=module_gpio, module_audio=module_audio, mistake_dict=mistake_dict, learnt_dict=learnt_dict, tested_dict=tested_dict)
        
        elif mode == ('exit', True):
            break;
        
        else:
            module_audio.say("Sorry, we couldnt recognize that. Please repeat.")


if __name__ == "__main__":
    main()