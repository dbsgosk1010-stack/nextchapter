import streamlit as st
from recommender import analyze_and_recommend
from visualizer import draw_book_map

st.set_page_config(page_title="NextChapter", page_icon="📚", layout="centered")

st.title("📚 NextChapter")
st.caption("읽은 책 3권을 입력하면, 당신만의 독서 취향을 분석하고 다음 책을 추천해드려요.")

st.divider()

col1, col2, col3 = st.columns(3)
with col1:
    book1 = st.text_input("첫 번째 책", placeholder="예: 채식주의자")
with col2:
    book2 = st.text_input("두 번째 책", placeholder="예: 82년생 김지영")
with col3:
    book3 = st.text_input("세 번째 책", placeholder="예: 아몬드")

if st.button("✨ 취향 분석 & 다음 책 추천", use_container_width=True):
    if not (book1 and book2 and book3):
        st.warning("책 3권을 모두 입력해주세요.")
    else:
        books = [book1, book2, book3]
        with st.spinner("독서 취향을 분석하는 중..."):
            result = analyze_and_recommend(books)

        st.divider()
        st.subheader("🗺️ 나의 독서지도")
        draw_book_map(books, result["connections"])

        st.divider()
        st.subheader("🎯 취향 분석 결과")
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("**정서**")
            st.info(result["analysis"]["정서"])
            st.markdown("**서사**")
            st.info(result["analysis"]["서사"])
        with col_b:
            st.markdown("**문체**")
            st.info(result["analysis"]["문체"])
            st.markdown("**문제의식**")
            st.info(result["analysis"]["문제의식"])

        st.divider()
        st.subheader("📖 추천 도서")
        for i, rec in enumerate(result["recommendations"], 1):
            with st.expander(f"{i}. {rec['title']} — {rec['author']}"):
                st.write(f"**추천 이유:** {rec['reason']}")
