# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import json
import urllib.request

# NAVER API 인증 정보
client_id = "q3Yd8CQkM7oHlqOzMeQL"
client_secret = "hGWoNfAcAD"

# 바디 구성 (나이키운동화 + 2025년 8월 일별)
body = {
    "startDate": "2025-08-01",
    "endDate": "2025-08-31",
    "timeUnit": "date",
     #일간 단위로
    "keywordGroups": [
        {
            "groupName": "나이키운동화",
            "keywords": ["나이키운동화"]
        }
    ],
    "device": "",
    #
    "ages": [],
    "gender": ""
}
body_str = json.dumps(body)
# body를 JSON 문자열로 변환
# API 서버는 JSON 문자열을 받아야함  파이썬 키-값을 그대로 보낼 수 없음
# json.dumps = 파이썬 dict 등을 JSON 문자열로 바꿔주는 함수.

#  요청 구성
url = "https://openapi.naver.com/v1/datalab/search"
request = urllib.request.Request(url)
request.add_header("X-Naver-Client-Id", "q3Yd8CQkM7oHlqOzMeQL")
request.add_header("X-Naver-Client-Secret", "hGWoNfAcAD")
request.add_header("Content-Type", "application/json")

#  API 호출
try:
    response = urllib.request.urlopen(request, data=body_str.encode("utf-8"))
    rescode = response.getcode() # HTTP 상태 코드 확인
    if rescode == 200: # 성공
        response_body = response.read()
        result_json = json.loads(response_body.decode('utf-8'))
#응답 바이트를 .decode('utf-8')로 문자열(str)로 변환(JSON은 보통 UTF-8)한 뒤 그 문자열을 json.loads로 파싱해 result_json에 담음 
    else:
        st.error(f"API Error Code: {rescode}")
        st.stop()
except Exception as e:
    st.error("API 요청 중 오류 발생")
    st.text(str(e))
    st.stop()

#  결과 파싱
data = result_json['results'][0]['data']  # 그룹(dict)별 
dates = [item['period'] for item in data]
ratios = [item['ratio'] for item in data]

# period = 구간별 시작 날짜(yyyy-mm-dd 형식)
# ratio = 구간별 검색량의 상대적 비율. 구간별 결과에서 가장 큰 값을 100으로 설정한 상댓값 ( 비율(%)가 아니라 지수라서 100을 넘어가지 않음 )
df = pd.DataFrame({
    '날짜': pd.to_datetime(dates),
    '검색량 지수': ratios
})

# 날짜를 index로 설정함
df = df.set_index('날짜')

#  Streamlit 시각화
# https://docs.streamlit.io/ 제목 서식에 텍스트를 표시
st.title("나이키운동화 검색어 트렌드 (2025년 8월)")

# https://docs.streamlit.io/ st.데이터프레임 테이블로 표시
st.dataframe(df, use_container_width=True)

# https://docs.streamlit.io/ 선형 차트를 표시
st.line_chart(df)
