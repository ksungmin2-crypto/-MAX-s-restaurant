import streamlit as st

st.title("🔒 MAX's restaurant")
st.write("주인장 마음대로 판매합니다.")

password = st.text_input("오늘의 메뉴는?", type="password")

if st.button("접속하기"):
    if password == "1234":
        st.success("맛점하세요.")
        st.write("---")
        st.subheader("⚙️ 크롤링 제어판")
        st.button("🚀 데이터 수집 시작")
    else:
        st.error("안 팔아요.")