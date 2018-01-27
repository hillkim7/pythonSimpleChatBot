'''
Created on 2018. 1. 28.

@author: hillk
'''

import csv
import unittest
import sys

class Answer:
    def __init__(self, answer, emotion=None):
        self.answer = answer
        self.emotion = emotion

class PetScript:
    def __init__(self, question, keywords, answers, emotions):
        self.question = question    # 예상 질문
        self.keywords = self.parse_keywords(keywords)
        self.answers = self.parse_answers(answers, emotions)

    def parse_keywords(self, keywords):
        return self.split_script_text(keywords, ',')
        
    def parse_answers(self, answers, emotions):
        parsed_answers = self.split_script_text(answers, ',')
        parsed_emotions = self.split_script_text(emotions, ',')
        answer_list = []
        for i in range(len(parsed_answers)):
            if i < len(parsed_emotions):
                answer_list.append(Answer(parsed_answers[i], parsed_emotions[i]))
            else:
                print('answer without emotion: ', parsed_answers[i])
                answer_list.append(Answer(parsed_answers[i]))
        return answer_list

    @staticmethod
    def split_script_text(text, sep):
        result = []
        for w in text.split(sep):
            w = w.strip()
            if w:
                result.append(w)
        return result
    
    def __str__(self):
        return 'keywords:' + ','.join(self.keywords)

class Scenario:
    def __init__(self):
        self.script_list = []

    def load_scenario_file(self, csv_file):
        with open(csv_file, 'r', encoding='euc_kr') as fd:
            reader = csv.DictReader(fd)
            for row in reader:
                if row['키워드']:
                    self.script_list.append(PetScript(row['질문'], row['키워드'], row['답변'], row['상태']))
                
    def load_scenario_text(self, doc_text):
        #reader = csv.reader(doc_text, delimiter=',', quotechar='"')
        reader = csv.reader(doc_text)
        for row in reader:
            print('row', row)
            #self.script_list.append(PetScript(row['질문'], row['키워드'], row['답변'], row['상태']))
            
    def dump(self):
        for script in self.script_list:
            print(script.__str__())
                
class TestPetScript(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestPetScript, self).__init__(*args, **kwargs)
        self.scenario = Scenario()
        self.scenario.load_scenario_text(
"""구분,질문,키워드,답변,상태,기타
일상,밥 먹었어?,"밥,먹","아닝 저는 밥 대신 물을 마시는 걸요!,
추워서 별로 안땡겨요?(?´0`?)?,
저는 2-3일에 한번만 먹으면 돼요! 그저께 먹었으니까 내일 밥 주세요!,
난 정수기 물 보다 미네랄 많은 수돗물이 맛있더라(?>?<?)~,
싫어싫어! 안먹을거야! 아직 물 충분하단 말야(?'-'?),
오늘따라 물 맛이 좋더라구요~,
맛있게 먹었는데 오늘 날씨가 더워서 더 먹고싶어요ㅠㅠ,
식량창고에 물 채워줘요! 얼마 안남았다구!,
( ??∀?? )?전 물을 자주 먹지 않는다구요~,
저는 물 꼬박꼬박 잘 챙겨먹고있죠~ {{name}}님은 물 많이 드시고 계신가요??,
요새 통 입맛이 없어가지구~.....,
냠냠!(?????) 잘 챙겨먹고 있어용!,
{{name}}님은 식사하셨어요?","smile,
gloom,
cute,
cute,
angry,
smile,
sad,
fun,
smile,
smile,
gloom,
excited,
smile",
일상,오늘은 뭐했어?,"뭐,뭐했","날씨가 좋아서 햇볕을 쬐고 있었어요(((o(♡´▽`♡)o))),
{{name}}님을 기다리고 있었죠~,
쑥쑥 자라고 있었어요ㅎㅎ,
(??? )흥! 늦게 왔으니까 말 안해줄래요!,
흙이랑 얘기했어요!,
벌이 다녀갔어요!,
바람이 불어서 간지러웠어요~,
가만히 있기 놀이했어요! {{name}}님은 뭐하셨어요~?","excited,
smile,
smile,
angry,
cute,
smile,
fun,
cute","""
            )
        
    def test_inputs(self):
        question = "밥 먹었어?"
        keywords = "밥,먹"
        answers = """아닝 저는 밥 대신 물을 마시는 걸요!,
추워서 별로 안땡겨요?(?´0`?)?,
저는 2-3일에 한번만 먹으면 돼요! 그저께 먹었으니까 내일 밥 주세요!,
난 정수기 물 보다 미네랄 많은 수돗물이 맛있더라(?>?<?)~,
싫어싫어! 안먹을거야! 아직 물 충분하단 말야(?'-'?),
오늘따라 물 맛이 좋더라구요~"""
        emotions = "smile,gloom,cute,cute,angry,smile"
        script = PetScript(question, keywords, answers, emotions)
        self.assertIn('밥', script.keywords)

if __name__ == "__main__":
    scenario = Scenario()
    scenario.load_scenario_file(sys.argv[1])
    scenario.dump()
