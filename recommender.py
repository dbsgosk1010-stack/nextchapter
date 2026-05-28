import streamlit as st
import google.generativeai as genai
import json
import re

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

def analyze_and_recommend(books: list[str]) -> dict:
    prompt = f"""
당신은 독서 취향 분석 전문가입니다.
독자가 읽은 책 3권: {books[0]}, {books[1]}, {books[2]}

아래 4축으로 독자의 취향을 분석하고, 다음 책 3권을 추천해주세요.

반드시 아래 JSON 형식으로만 응답하세요. 다른 텍스트는 절대 포함하지 마세요.

{{
  "analysis": {{
    "정서": "이 독자가 선호하는 감정적 톤을 2문장으로 설명",
    "서사": "이 독자가 선호하는 이야기 구조를 2문장으로 설명",
    "문체": "이 독자가 선호하는 문체 스타일을 2문장으로 설명",
    "문제의식": "이 독자가 관심 갖는 주제와 사회적 문제를 2문장으로 설명"
  }},
  "connections": [
    {{"from": "{books[0]}", "to": "{books[1]}", "label": "공통점 한 줄"}},
    {{"from": "{books[1]}", "to": "{books[2]}", "label": "공통점 한 줄"}},
    {{"from": "{books[0]}", "to": "{books[2]}", "label": "공통점 한 줄"}}
  ],
  "recommendations": [
    {{
      "title": "추천 도서명",
      "author": "저자명",
      "reason": "이 3권을 읽은 독자에게 추천하는 구체적인 이유 (정서/서사/문체/문제의식 중 어떤 취향과 연결되는지 명시)"
    }},
    {{
      "title": "추천 도서명",
      "author": "저자명",
      "reason": "추천 이유"
    }},
    {{
      "title": "추천 도서명",
      "author": "저자명",
      "reason": "추천 이유"
    }}
  ]
}}
"""
    response = model.generate_content(prompt)
    text = response.text.strip()
    text = re.sub(r"```json|```", "", text).strip()
    return json.loads(text)
