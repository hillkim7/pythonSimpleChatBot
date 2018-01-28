'''
Created on 2018. 1. 28.

@author: hillk
'''

class PetBot:
    
    def __init__(self, my_name, scenario, input_processor, output_processor):
        self.my_name = my_name
        self.scenario = scenario
        self.input_processor = input_processor
        self.output_processor = output_processor
        
    def talk(self, input_text):
        morphs = self.input_processor.morphs(input_text)
        answer = self.scenario.answer_please(morphs)
        if answer:
            answer.text = self.output_processor.post_process(answer.text)
            return answer
        