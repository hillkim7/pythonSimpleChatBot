Python 간단한 챗봇 구현
-----------------
간단한 대화형 챗봇을 구현하기 위해서
예상 질문과 키워드, 대답할 답변을 포함하는 대화 시나리오를 먼저 엑셀 파일에 작성한다.  
파인썬 프로그램에서 작성된 시나리오 엑셀 파일을 읽기 위해 엑셀에서 CSV 파일로 저장한다.  
파인썬 프로그램은 CSV 파일을 적재하여 사용자가 입력하는 질문을 적재된 시나리오에서 답변을 찾아 대답하게 된다.  
입력된 사용자 질문에 해당하는 시나리오에서 가장 적절한 답변을 찾기 위해서는
질문을 구문 분석하고 그 결과로 나온 단어와 시나리오상의 키워드를 비교하여 가장 잘 매치된 항목을 찾아서 답변을 한다.
