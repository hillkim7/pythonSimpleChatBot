'''
Created on 2018. 1. 28.

@author: hillk
'''

import csv
import unittest
import sys
import random

class Answer:
    def __init__(self, text, emotion=None):
        self.text = text
        self.emotion = emotion
    
    def __str__(self):
        return str((self.text, self.emotion))

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
    
    def scores(self, morphs):
        score = 0
        for m in morphs:
            if m in self.keywords:
                score += 1
        return score
    
    def best_answer(self):
        return random.choice(self.answers)


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
            #print('row', row)
            self.script_list.append(PetScript(row['질문'], row['키워드'], row['답변'], row['상태']))
            
    def dump(self):
        for script in self.script_list:
            print(script.__str__())
    
    def make_score_table(self, morphs):
        scores = []
        for script in self.script_list:
            scores.append(script.scores(morphs))
        return scores

    def find_top_score(self, scores):
        top = 0
        for i in range(1, len(scores)):
            if scores[i] > scores[top]:
                top = i
        return top

    def answer_please(self, input_morphs):
        scores = self.make_score_table(input_morphs)
        top_pos = self.find_top_score(scores)
        if scores[top_pos] > 0:
            pet_script = self.script_list[top_pos]
            return pet_script.best_answer()

class TestPetScript(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestPetScript, self).__init__(*args, **kwargs)
        
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

    def test_best_answer(self):
        scenario = Scenario()
        scenario.script_list.append(PetScript('q1', 'K1, K2, K3', '0', 'E1'))
        scenario.script_list.append(PetScript('q1', 'K3, K4, K5', '1', 'E2'))
        scenario.script_list.append(PetScript('q1', 'K5, K6', '2', 'E3'))
        answer = scenario.answer_please(['K3', 'K4', 'K6'])
        self.assertIn('1', answer.text)

    def test_best_answer2(self):
        scenario = Scenario()
        scenario.script_list.append(PetScript('q1', 'K1, K2, K3', '0', 'E1'))
        scenario.script_list.append(PetScript('q1', 'K3, K4, K5', '1', 'E2'))
        scenario.script_list.append(PetScript('q1', 'K5, K6', '2', 'E3'))
        answer = scenario.answer_please(['K6'])
        self.assertIn('2', answer.text)

    def test_none_answer(self):
        scenario = Scenario()
        scenario.script_list.append(PetScript('q1', 'K1, K2, K3', '0', 'E1'))
        scenario.script_list.append(PetScript('q1', 'K3, K4, K5', '1', 'E2'))
        scenario.script_list.append(PetScript('q1', 'K5, K6', '2', 'E3'))
        answer = scenario.answer_please(['K7'])
        self.assertEqual(None, answer)

if __name__ == "__main__":
    scenario = Scenario()
    scenario.load_scenario_file(sys.argv[1])
    scenario.dump()
