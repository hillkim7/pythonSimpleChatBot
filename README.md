Python 간단한 챗봇 구현
-----------------
간단한 대화형 챗봇을 구현하기 위해서
예상 질문과 키워드, 대답할 답변을 포함하는 대화 시나리오를 먼저 엑셀 파일에 작성한다.  
파인썬 프로그램에서 작성된 시나리오 엑셀 파일을 읽기 위해 엑셀에서 CSV 파일로 저장한다.  
파인썬 프로그램은 CSV 파일을 적재하여 사용자가 입력하는 질문을 적재된 시나리오에서 답변을 찾아 대답하게 된다.  
입력된 사용자 질문에 해당하는 시나리오에서 가장 적절한 답변을 찾기 위해서는
질문을 구문 분석하고 그 결과로 나온 단어와 시나리오상의 키워드를 비교하여 가장 잘 매치된 항목을 찾아서 답변을 한다.

konlpy 패키지 설치
-----------------
konlpy는 한국어 전용 자연어처리(NPL) 패키지로 한글 문장의 구문 분석을 위해 사용된다.  
konlpy는 JPype1 패키지에 의존성이 있음으로 이 패키지 설치가 필요하다.

#### 한글 Windows 10에서 설치
JPype1 설치시 오류가 발생됨으로 패키지 소스 수정이 필요하다.
> D:\simpleChatBot>pip install JPype1

```
Collecting JPype1
  Using cached JPype1-0.6.2.tar.gz
Installing collected packages: JPype1
  Running setup.py install for JPype1 ... error
Exception:
Traceback (most recent call last):
  File "c:\python36\lib\site-packages\pip\compat\__init__.py", line 73, in console_to_str
    return s.decode(sys.__stdout__.encoding)
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xc7 in position 111: invalid continuation byte
......
  File "c:\python36\lib\site-packages\pip\compat\__init__.py", line 75, in console_to_str
    return s.decode('utf_8')
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xc7 in position 111: invalid continuation byte
```
패키지 소스를 에디터로 열어서 수정  
```
notepad c:\python36\lib\site-packages\pip\compat\__init__.py
```
수정전 소스
```python
if sys.version_info >= (3,):
    def console_to_str(s):
        try:
            return s.decode(sys.__stdout__.encoding)
        except UnicodeDecodeError:
            return s.decode('utf_8')
```
수정 후 소스
```python
if sys.version_info >= (3,):
    def console_to_str(s):
        try:
            return s.decode(sys.__stdout__.encoding)
        except UnicodeDecodeError:
            return s.decode('euc_kr')
            #return s.decode('utf_8')
```
소스 수정후 다시 설치
> D:\simpleChatBot>pip install JPype1

konlpy 설치
> pip install konlpy

#### raspberrypi/Ubuntu에서 설치
> sudo apt-get install openjdk-8-jdk  
> pip3 install konlpy  
> pip3 install JPype1  

konlpy 패키지 설치 확인
-----------------

```
pi@raspberrypi:~ $ python3
Python 3.5.3 (default, Jan 19 2017, 14:11:04)
[GCC 6.3.0 20170124] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from konlpy.tag import Kkma, Twitter
>>> from konlpy.utils import pprint
>>> kkma = Kkma()
>>> print(kkma.sentences('한글 NLP를 설치했습니다. 몇 시간을 날렸어요.'))
['한글 NLP를 설치했습니다.', '몇 시간을 날렸어요.']
>>> print(kkma.nouns(u'한글 NLP를 설치했습니다. 몇 시간을 날렸어요.'))
['한글', '설치', '시간']
>>> twitter = Twitter()
>>> twitter.morphs('@챗봇 내일 판매율 예측해서 Anderson한테 이메일로 보내줘.')
['@', '챗봇', '내일', '판매', '율', '예측해서', 'Anderson', '한테', '이메일', '로', '보내', '줘', '.']
>>> twitter.nouns('@챗봇 내일 판매율 예측해서 Anderson한테 이메일로 보내줘.')
['챗봇', '내일', '판매', '율', '이메일']
```

