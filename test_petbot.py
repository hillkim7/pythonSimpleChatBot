'''
Created on 2018. 1. 28.

@author: hillk
'''
import sys
from petscript.petbot import PetBot
from petscript.inputprocessor import InputProcessor
from petscript.outputprocessor import OutputProcessor
from petscript.petscript import Scenario

if len(sys.argv) < 3:
    print(sys.argv[0], "bot_name script.csv")
    sys.exit(0)

scenario = Scenario()
input_processor = InputProcessor()
output_processor = OutputProcessor()

scenario.load_scenario_file(sys.argv[2])

bot = PetBot(sys.argv[1], scenario, input_processor, output_processor)

try:
    while True:
        sys.stdout.write('>> ')
        sys.stdout.flush()
        text = sys.stdin.readline().strip()
        if text:
            answer = bot.talk(text)
            if answer:
                print(answer)
            else:
                print('^^')
except KeyboardInterrupt:
    pass
