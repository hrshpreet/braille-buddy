import math
import random

# So, in learning mode, ee're teaching the user alphabets, three at a time, and repeating each batch twice to help them remember. But there’s a catch: if the user messes up on an alphabet during a test, we need to keep track of that letter and make sure it comes up again in future lessons.

# Plan:
# We maintain a `mistake_dict` that counts how many times the user has gotten each alphabet wrong. Each time they make a mistake, we increase that count by one (ONLY IN TESTS). so, if a letter has a high mistake count, it’ll show up more often in lessons, giving the user a better chance to improve.

# Flow:
# - We pick three new letters (not learned yet) from the `learnt_dict` for the lesson.
# - Then we grab some letters from the `mistake_dict`, picked probabilistically based on how times the user has made the mistake.
# - We combine both sets of letters to create a lesson.

# Scope:
# restart learning if all learnt
# focus on mistakes, if all learnt



def run_learn_mode(module_gpoi, module_audio, mistake_dict, learnt_dict, lesson_size=8, new_aplhabet_count=3):
    module_audio.say("Starting Lesson")
    
    new_alphabets = get_new_alphabets(learnt_dict=learnt_dict, count=new_aplhabet_count)
    prev_mistakes = get_prev_mistakes(mistake_dict=mistake_dict, learnt_dict=learnt_dict, count=lesson_size-2*len(new_alphabets))
    lesson = new_alphabets + new_alphabets + prev_mistakes
    give_lesson(module_gpoi=module_gpoi, module_audio=module_audio, learnt_dict=learnt_dict, lesson=lesson)




def get_new_alphabets(learnt_dict, count):
    new_alphabets = [key for key, value in learnt_dict.items() if not value][:count]
    return new_alphabets




def get_prev_mistakes(mistake_dict, learnt_dict, count, temperature=1.0):
    learnt_alphabets = {key: mistake_dict.get(key, 0) for key, value in learnt_dict.items() if value}
    if not learnt_alphabets:
        return []
    
    def softmax():
        exponentiated = {k: math.exp(v / temperature) for k, v in learnt_alphabets.items()}
        total = sum(exponentiated.values())
        probabilities = {k: v / total for k, v in exponentiated.items()}
        return probabilities
    
    probabilities = softmax()
    prev_mistakes = random.choices(
        population=list(probabilities.keys()), 
        weights=list(probabilities.values()), 
        k=count
    )
    
    return prev_mistakes




def give_lesson(module_gpoi, module_audio, learnt_dict, lesson):
    for alphabet in lesson:
        module_gpoi.print_alphabet(alphabet)
        module_audio.say(alphabet)
        response, status = module_audio.recognize_alphabet()
        
        if(response == alphabet):
            module_audio.say("Correct Answer")
            learnt_dict[alphabet] = True
        else:
            module_audio.say("Wrong answer. Try Again.")
            new_response = module_audio.recognize_alphabet()
            if(new_response == alphabet):
                module_audio.say("Correct Answer")
                learnt_dict[alphabet] = True
            else:
                skip_statement = "Good try!! The correct answer was " + alphabet
                module_audio.say(skip_statement)
        
        module_gpoi.hide_alphabet(alphabet)
        
    module_audio.say("Lesson Completed")
        
        
# RAW IDEA
# so, in learning mode, it is kind of complex and i cant wrap my mind around how to make it work. so we are teaching alphabets, 3 at a time, repeated 2 times. but then there is a complexity, if the user makes an alphabet wrong in the test, we need to keep track of that alphabet and serve that alphabet again in the upcoming lessons.

# i have an idea. 
# we keep a map of the alphabets that were wrong in the test. 1 mistake we add 1 to the count of that character. right. and then from the map we choose the alphabet probabilistically. if it is wrong quite often, then its count will be high and hence the probability that it will pop up more often in the lesson.

# also we keep another map of the alphabets that have been learnt. and if the mistake map is 0, we choose the mistake questions from the learnt map