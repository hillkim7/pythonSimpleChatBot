'''
Created on 2018. 1. 28.

@author: hillk
'''
import sys
from konlpy.tag import Twitter

twitter = Twitter()

print('한글 문장을 입력하세요.')

try:
    while True:
        sys.stdout.write('>> ')
        sys.stdout.flush()
        text = sys.stdin.readline().strip()
        if text:
            answer = twitter.morphs(text)
            print(answer)
except KeyboardInterrupt:
    pass
