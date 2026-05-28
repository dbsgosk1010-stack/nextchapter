import streamlit as st
import google.generativeai as genai
import json
import re
import time

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.0-flash-lite")

def call_gemini(prompt):
    time.sleep(2)
    response = model.generate_content(prompt)
    return re.sub(r"```json|```", "", response.text).strip()

def analyze_and_recommend(books: list[str]) -> dict:
    b0, b1, b2 = books[0], books[1], books[2]

    # 1호출: 취향 분석
    p1 = f"""책 3권 {b0}, {b1}, {b2}의 독자 취향을 분석해 JSON만 출력.
{{"정서":"한 문장","서사":"한 문장","문체":"한 문장","문제의식":"한 문장"}}"""
    analysis = json.loads(call_gemini(p1))

    # 2호출: 추천
    p2 = f"""취향: {analysis}
이 독자에게 맞는 책 3권 추천. JSON만 출력.
[{{"title":"제목","author":"저자","reason":"한 문장"}},{{"title":"제목","author":"저자","reason":"한 문장"}},{{"title":"제목","author":"저자","reason":"한 문장"}}]"""
    recommendations = json.loads(call_gemini(p2))

    connections = [
        {"from": b0, "to": b1, "label": "연결"},
        {"from": b1, "to": b2, "label": "연결"},
        {"from": b0, "to": b2, "label": "연결"},
    ]

    return {"analysis": analysis, "connections": connections, "recommendations": recommendations}
