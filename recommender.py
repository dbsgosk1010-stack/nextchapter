import streamlit as st
import google.generativeai as genai
import json
import re

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.0-flash-lite")

def analyze_and_recommend(books: list[str]) -> dict:
    prompt = f"""책 3권: {books[0]}, {books[1]}, {books[2]}

JSON만 출력. 다른 텍스트 금지.

{{"analysis":{{"정서":"한 문장","서사":"한 문장","문체":"한 문장","문제의식":"한 문장"}},"connections":[{{"from":"{books[0]}","to":"{books[1]}","label":"공통점"}},{{"from":"{books[1]}","to":"{books[2]}","label":"공통점"}},{{"from":"{books[0]}","to":"{books[2]}","label":"공통점"}}],"recommendations":[{{"title":"책제목","author":"저자","reason":"추천이유"}},{{"title":"책제목","author":"저자","reason":"추천이유"}},{{"title":"책제목","author":"저자","reason":"추천이유"}}]}}"""

    response = model.generate_content(prompt)
    text = re.sub(r"```json|```", "", response.text).strip()
    return json.loads(text)
