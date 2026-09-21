import streamlit as st

st.title("🔒 MAX's restaurant")
st.write("주인장 마음대로 판매합니다. 오늘의 메뉴는?")

# 비밀번호 입력
password = st.text_input("비밀번호를 입력하세요", type="password")

if password == "1234":
    st.success("로그인 성공! 맛점하세요.")
    st.write("---")
    st.subheader("오늘의 추천 메뉴")
    st.write("1. 제육볶음 - 8,000원")
    st.write("2. 김치찌개 - 7,500원")
    st.write("3. 돈까스 - 8,500원")
elif password != "":
    st.error("비밀번호가 틀렸습니다.")
