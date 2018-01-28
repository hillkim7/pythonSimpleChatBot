'''
Created on 2018. 1. 28.

@author: hillk
'''
from konlpy.tag import Twitter

class InputProcessor:
    
    def __init__(self):
        self.twitter = Twitter()
    
    def morphs(self, input_line):
        morphs = self.twitter.morphs(input_line)
        return morphs
