# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import json
import urllib.request

# NAVER API 인증 정보
client_id = "q3Yd8CQkM7oHlqOzMeQL"
client_secret = "hGWoNfAcAD"

#  요청 바디 구성 (나이키운동화 + 2025년 8월 일별)
body = {
    "startDate": "2025-08-01",
    "endDate": "2025-08-31",
    "timeUnit": "date",
    "keywordGroups": [
        {
            "groupName": "나이키운동화",
            "keywords": ["나이키운동화"]
        }
    ],
    "device": "",
    "ages": [],
    "gender": ""
}
body_str = json.dumps(body)

#  요청 구성
url = "https://openapi.naver.com/v1/datalab/search"
request = urllib.request.Request(url)
request.add_header("X-Naver-Client-Id", "q3Yd8CQkM7oHlqOzMeQL")
request.add_header("X-Naver-Client-Secret", "hGWoNfAcAD")
request.add_header("Content-Type", "application/json")

#  API 호출
try:
    response = urllib.request.urlopen(request, data=body_str.encode("utf-8"))
    rescode = response.getcode()
    if rescode == 200:
        response_body = response.read()
        result_json = json.loads(response_body.decode('utf-8'))
    else:
        st.error(f"API Error Code: {rescode}")
        st.stop()
except Exception as e:
    st.error("API 요청 중 오류 발생")
    st.text(str(e))
    st.stop()

#  결과 파싱
data = result_json['results'][0]['data']
dates = [item['period'] for item in data]
ratios = [item['ratio'] for item in data]

df = pd.DataFrame({
    '날짜': pd.to_datetime(dates),
    '검색량 지수': ratios
})
df = df.set_index('날짜')

# 📌 Streamlit 시각화
st.title("나이키운동화 검색어 트렌드 (2025년 8월)")
st.dataframe(df, use_container_width=True)
st.line_chart(df)
