import streamlit as st

st.set_page_config(
    page_title="MAX's restaurant",
    page_icon="🔒",
    layout="wide"
)

# 로그인 상태 저장
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# =========================
# 로그인 화면
# =========================
if not st.session_state.logged_in:

    st.title("🔒 MAX's restaurant")
    st.write("주인장 마음대로 판매합니다.")

    password = st.text_input(
        "오늘의 메뉴는?",
        type="password"
    )

    if st.button("접속하기"):

        if password == "1234":

            st.session_state.logged_in = True

            st.rerun()

        else:

            st.error("안 팔아요.")

    st.stop()


# =========================
# 로그인 성공 후 화면
# =========================
st.title("🔒 MAX's restaurant")

st.success("맛점하세요.")

# 로그아웃 버튼
if st.sidebar.button("🚪 로그아웃"):

    st.session_state.logged_in = False

    st.rerun()


st.write("---")

st.subheader("⚙️ 크롤링 제어판")


# 사이트 종류 선택
site_type = st.selectbox(
    "어디에서 수집할까요?",
    [
        "일반 웹사이트",
        "Shopify",
        "Cafe24"
    ]
)


# URL 입력
target_url = st.text_input(
    "수집할 사이트 주소",
    placeholder="https://example.com"
)


# 크롤링 버튼
if st.button("🚀 데이터 수집 시작"):

    if target_url == "":

        st.warning("사이트 주소를 입력해주세요.")

    else:

        st.info(
            f"{site_type}에서 데이터를 수집할 준비가 되었습니다."
        )

        st.write("입력한 주소:")
        st.write(target_url)
