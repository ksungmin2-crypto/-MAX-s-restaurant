import streamlit as st
import pandas as pd
import requests
from datetime import date
import io

# 페이지 기본 설정
st.set_page_config(page_title="Redash 데이터 추출기", layout="wide")

st.title("📊 Redash 데이터 다운로더")
st.write("Redash API Key와 Query ID를 입력하여 최신 데이터를 엑셀로 추출합니다.")

st.markdown("---")

col1, col2 = st.columns([2, 1])

with col1:
    # Redash 접속 정보
    redash_url = st.text_input("Redash 주소", value="https://redash.kroffle.net")[cite: 1]
    
    # API Key는 코드에 노출하지 않고 화면에서 직접 입력받도록 설정
    api_key = st.text_input(
        "Redash API Key", 
        type="password",
        placeholder="내 계정의 API Key를 입력하세요",
        help="Redash 계정 설정(Account) 페이지에서 복사한 API Key를 입력해 주세요."[cite: 1]
    )
    
    query_id = st.text_input(
        "Query ID", 
        value="11953", 
        help="Redash 쿼리 URL의 /queries/11953 숫자 부분을 입력해 주세요."
    )

    # 기간 설정
    d_col1, d_col2 = st.columns(2)
    with d_col1:
        start_date = st.date_input("시작일", value=date(2026, 1, 1))
    with d_col2:
        end_date = st.date_input("종료일", value=date(2026, 9, 21))

    # Redash API 호출 함수
    def fetch_redash_data(base_url, q_id, key, p_start, p_end):
        csv_url = f"{base_url}/api/queries/{q_id}/results.csv"
        params = {
            "api_key": key,
            "p_기간": f"{p_start}--{p_end}"
        }
        res = requests.get(csv_url, params=params)
        if res.status_code == 200:
            df = pd.read_csv(io.BytesIO(res.content))
            return df
        else:
            st.error(f"Redash 연결 실패 (상태 코드: {res.status_code}) - Query ID 또는 API Key를 확인해 주세요.")
            return None

    if "download_history" not in st.session_state:
        st.session_state.download_history = []

    # 실행 및 다운로드 버튼
    if st.button("🚀 데이터 불러오기 및 엑셀 변환", use_container_width=True):
        if not api_key:
            st.warning("⚠️ Redash API Key를 입력해 주세요!")
        else:
            with st.spinner("Redash에서 데이터를 수집하는 중입니다..."):
                df = fetch_redash_data(redash_url, query_id, api_key, start_date, end_date)
                
                if df is not None:
                    # 엑셀 파일 변환
                    output = io.BytesIO()
                    with pd.ExcelWriter(output, engine='openpyxl') as writer:
                        df.to_excel(writer, index=False, sheet_name='RedashData')
                    excel_data = output.getvalue()

                    # 이력 추가
                    st.session_state.download_history.append({
                        "time": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "query": f"Query #{query_id}",
                        "range": f"{start_date} ~ {end_date}"
                    })

                    st.success(f"총 {len(df):,}건의 데이터를 성공적으로 불러왔습니다!")
                    
                    # 다운로드 버튼 및 데이터 미리보기
                    st.download_button(
                        label="💾 엑셀 파일 받아오기",
                        data=excel_data,
                        file_name=f"redash_{query_id}_{start_date}_{end_date}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )
                    st.write("### 📊 데이터 미리보기")
                    st.dataframe(df, use_container_width=True)

with col2:
    st.subheader("📋 추출 내역")
    if st.button("내역 지우기"):
        st.session_state.download_history = []
        st.rerun()

    if not st.session_state.download_history:
        st.info("추출 내역이 없습니다.")
    else:
        for item in reversed(st.session_state.download_history):
            st.text(f"[{item['time']}]\n- {item['query']}\n- {item['range']}")
            st.markdown("---")
