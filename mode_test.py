import mode_learn



def run_test_mode(module_gpoi, module_audio, mistake_dict, learnt_dict, tested_dict, test_size=5):
    module_audio.say("Starting Test")
    
    untested_count = 5
    untested_alphabets = get_untested(learnt_dict=learnt_dict, tested_dict=tested_dict, count=untested_count)
    
    prev_mistakes = mode_learn.get_prev_mistakes(mistake_dict=mistake_dict, learnt_dict=learnt_dict, count=test_size-len(untested_alphabets))
    
    test = untested_alphabets + prev_mistakes
    take_test(module_gpoi=module_gpoi, module_audio=module_audio, mistake_dict=mistake_dict, tested_dict=tested_dict, test=test)




def get_untested(learnt_dict, tested_dict, count):
    untested_alphabets = [key for key in learnt_dict if learnt_dict[key] and not tested_dict.get(key, False)]
    return untested_alphabets[:count]




def take_test(module_gpoi, module_audio, mistake_dict, tested_dict, test):
    for alphabet in test:
        module_gpoi.print_alphabet(alphabet)
        response, status = module_audio.recognize_alphabet()
        if(response == alphabet):
            if mistake_dict[alphabet] > 0:
                mistake_dict[alphabet] -= 1
            tested_dict[alphabet] = True
            module_audio.say("Correct Answer")

        else:
            module_audio.say("Wrong answer. Try Again.")
            new_response = module_audio.recognize_alphabet()
            if(new_response == alphabet):
                tested_dict[alphabet] = True
                module_audio.say("Correct Answer")
            else:
                mistake_dict[alphabet] += 1
                skip_statement = "The correct answer was " + alphabet
                module_audio.say(skip_statement)
        module_gpoi.hide_alphabet(alphabet)
                    
    module_audio.say("Lesson Completed")