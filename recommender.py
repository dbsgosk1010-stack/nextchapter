import streamlit as st
import anthropic
import json
import re

client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])

def analyze_and_recommend(books: list[str]) -> dict:
    b0, b1, b2 = books[0], books[1], books[2]

    prompt = f"""책 3권: {b0}, {b1}, {b2}
독자 취향을 분석하고 다음 책을 추천해줘. JSON만 출력.

{{"analysis":{{"정서":"한 문장","서사":"한 문장","문체":"한 문장","문제의식":"한 문장"}},"connections":[{{"from":"{b0}","to":"{b1}","label":"공통점"}},{{"from":"{b1}","to":"{b2}","label":"공통점"}},{{"from":"{b0}","to":"{b2}","label":"공통점"}}],"recommendations":[{{"title":"제목","author":"저자","reason":"추천이유"}},{{"title":"제목","author":"저자","reason":"추천이유"}},{{"title":"제목","author":"저자","reason":"추천이유"}}]}}"""

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )
    text = re.sub(r"```json|```", "", message.content[0].text).strip()
    return json.loads(text)
