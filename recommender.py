import streamlit as st
import anthropic
import json
import re

client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])

def analyze_and_recommend(books: list[str]) -> dict:
    b0, b1, b2 = books[0], books[1], books[2]

    prompt = f"""책 3권: A="{b0}", B="{b1}", C="{b2}"

아래 JSON만 출력. 다른 텍스트 없이.

{{
  "analysis": {{"정서":"한 문장","서사":"한 문장","문체":"한 문장","문제의식":"한 문장"}},
  "individual": {{
    "{b0}": [{{"title":"제목","author":"저자","reason":"추천이유","deeper":{{"title":"제목","author":"저자","reason":"이유"}}}}, {{"title":"제목","author":"저자","reason":"추천이유","deeper":{{"title":"제목","author":"저자","reason":"이유"}}}}],
    "{b1}": [{{"title":"제목","author":"저자","reason":"추천이유","deeper":{{"title":"제목","author":"저자","reason":"이유"}}}}, {{"title":"제목","author":"저자","reason":"추천이유","deeper":{{"title":"제목","author":"저자","reason":"이유"}}}}],
    "{b2}": [{{"title":"제목","author":"저자","reason":"추천이유","deeper":{{"title":"제목","author":"저자","reason":"이유"}}}}, {{"title":"제목","author":"저자","reason":"추천이유","deeper":{{"title":"제목","author":"저자","reason":"이유"}}}}]
  }},
  "pairs": {{
    "{b0}+{b1}": {{"label":"연결키워드","books":[{{"title":"제목","author":"저자","reason":"이유","deeper":{{"title":"제목","author":"저자","reason":"이유"}}}},{{"title":"제목","author":"저자","reason":"이유","deeper":{{"title":"제목","author":"저자","reason":"이유"}}}}]}},
    "{b1}+{b2}": {{"label":"연결키워드","books":[{{"title":"제목","author":"저자","reason":"이유","deeper":{{"title":"제목","author":"저자","reason":"이유"}}}},{{"title":"제목","author":"저자","reason":"이유","deeper":{{"title":"제목","author":"저자","reason":"이유"}}}}]}},
    "{b0}+{b2}": {{"label":"연결키워드","books":[{{"title":"제목","author":"저자","reason":"이유","deeper":{{"title":"제목","author":"저자","reason":"이유"}}}},{{"title":"제목","author":"저자","reason":"이유","deeper":{{"title":"제목","author":"저자","reason":"이유"}}}}]}},
    "{b0}+{b1}+{b2}": {{"label":"연결키워드","books":[{{"title":"제목","author":"저자","reason":"이유","deeper":{{"title":"제목","author":"저자","reason":"이유"}}}},{{"title":"제목","author":"저자","reason":"이유","deeper":{{"title":"제목","author":"저자","reason":"이유"}}}}]}}
  }}
}}"""

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=3000,
        messages=[{"role": "user", "content": prompt}]
    )
    text = re.sub(r"```json|```", "", message.content[0].text).strip()
    return json.loads(text)
