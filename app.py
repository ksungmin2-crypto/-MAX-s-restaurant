import pandas as pd
import requests
import streamlit as st

# ==========================================
# 1. 비밀번호 설정 (원하시는 비밀번호로 변경하세요)
# ==========================================
USER_PASSWORD = "1234"  # 사용하고 싶으신 비밀번호로 바꿔주세요!

# 로그인 상태 관리 변수 초기화
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ==========================================
# 2. 로그인 화면 처리
# ==========================================
if not st.session_state.logged_in:
    st.title("🔒 MAX's restaurant")
    st.write("오늘의 추천 메뉴는?.")

    password_input = st.text_input("된장찌개와 계란말이", type="password")

    if st.button("주문"):
        if password_input == USER_PASSWORD:
            st.session_state.logged_in = True
            st.success("로그인 성공!")
            st.rerun()  # 화면 새로고침
        else:
            st.error("비밀번호가 올바르지 않습니다.")

# ==========================================
# 3. 로그인 성공 후 나오는 메인 화면
# ==========================================
else:
    # 로그아웃 버튼 (오른쪽 위 상단)
    col1, col2 = st.columns([4, 1])
    with col2:
        if st.button("로그아웃"):
            st.session_state.logged_in = False
            st.rerun()

    st.title("📊 Redash 데이터 다운로더")
    st.write(
        "Redash API Key와 Query ID를 입력하여 최신 데이터를 추출합니다."
    )

    # 사용자 입력창
    redash_url = st.text_input(
        "Redash 주소", value="https://redash.kroffle.net"
    )
    api_key = st.text_input("Redash API Key", type="password")
    query_id = st.text_input("Query ID (숫자)")

    # 데이터 추출 버튼
    if st.button("데이터 추출하기"):
        if not api_key or not query_id:
            st.warning("API Key와 Query ID를 모두 입력해주세요.")
        else:
            try:
                endpoint = f"{redash_url.rstrip('/')}/api/queries/{query_id}/results.csv?api_key={api_key}"
                response = requests.get(endpoint)

                if response.status_code == 200:
                    from io import StringIO

                    df = pd.read_csv(StringIO(response.text))

                    st.success("데이터를 성공적으로 불러왔습니다!")
                    st.dataframe(df)

                    st.download_button(
                        label="📥 CSV(엑셀) 파일로 다운로드",
                        data=response.text,
                        file_name=f"redash_query_{query_id}.csv",
                        mime="text/csv",
                    )
                else:
                    st.error(
                        f"데이터를 가져올 수 없습니다. (에러 코드: {response.status_code})"
                    )
                    st.info(
                        "Redash 주소, API Key, Query ID가 맞는지 다시 확인해주세요."
                    )

            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")
