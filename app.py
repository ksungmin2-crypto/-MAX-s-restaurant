from datetime import datetime, timedelta
from io import StringIO
import pandas as pd
import requests
import streamlit as st

# ==========================================
# 1. 비밀번호 설정
# ==========================================
USER_PASSWORD = "1234"  # 사용하고 싶으신 비밀번호로 바꿔주세요!

# 로그인 상태 관리 변수 초기화
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ==========================================
# 2. 로그인 화면 처리 (요청하신 문구 적용)
# ==========================================
if not st.session_state.logged_in:
    st.title("🔒 MAX's restaurant")
    st.write("오늘의 추천 메뉴는?.")

    password_input = st.text_input(
        "된장찌개와 계란말이", type="password"
    )

    if st.button("주문"):
        if password_input == USER_PASSWORD:
            st.session_state.logged_in = True
            st.success("주문 성공!")
            st.rerun()  # 화면 새로고침
        else:
            st.error("품절입니다.")

# ==========================================
# 3. 로그인 성공 후 나오는 메인 화면
# ==========================================
else:
    # 로그아웃 버튼 (오른쪽 위 상단)
    col1, col2 = st.columns([4, 1])
    with col2:
        if st.button("식사 완료"):
            st.session_state.logged_in = False
            st.rerun()

    st.title("📊 Redash 데이터 다운로더")
    st.write(
        "기간 및 조건별로 Redash 데이터를 조회하고 다운로드합니다."
    )

    # 기본 설정 입력
    redash_url = st.text_input(
        "Redash 주소", value="https://redash.kroffle.net"
    )
    api_key = st.text_input("Redash API Key", type="password")
    query_id = st.text_input("Query ID (숫자)", value="11953")

    # 기간 설정 (기본값: 최근 7일)
    st.subheader("📅 기간 및 파라미터 설정")
    col_start, col_end = st.columns(2)
    with col_start:
        start_date = st.date_input(
            "시작일", datetime.today() - timedelta(days=7)
        )
    with col_end:
        end_date = st.date_input("종료일", datetime.today())

    # 데이터 추출 버튼
    if st.button("데이터 추출하기"):
        if not api_key or not query_id:
            st.warning("API Key와 Query ID를 모두 입력해주세요.")
        else:
            try:
                # Redash 파라미터 규격(p_파라미터명) 적용
                endpoint = (
                    f"{redash_url.rstrip('/')}/api/queries/{query_id}/results.csv"
                    f"?api_key={api_key}"
                    f"&p_start_date={start_date}"
                    f"&p_end_date={end_date}"
                )

                response = requests.get(endpoint)

                if response.status_code == 200:
                    df = pd.read_csv(StringIO(response.text))

                    st.success("데이터를 성공적으로 불러왔습니다!")
                    st.dataframe(df)

                    st.download_button(
                        label="📥 CSV(엑셀) 파일로 다운로드",
                        data=response.text,
                        file_name=f"redash_{query_id}_{start_date}_{end_date}.csv",
                        mime="text/csv",
                    )
                else:
                    st.error(
                        f"데이터를 가져올 수 없습니다. (에러 코드: {response.status_code})"
                    )
                    st.info(
                        "Redash 쿼리에 파라미터 이름(start_date, end_date)이 올바르게 지정되어 있는지 확인해 주세요."
                    )

            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")
