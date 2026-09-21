import streamlit as st
import pandas as pd
from datetime import date
import io

# 페이지 기본 설정
st.set_page_config(page_title="F1P — 툴 사용", layout="wide")

st.title("F1P — 툴 사용")

# 상단 탭/버튼 메뉴
tool_tabs = [
    "☆ 데이터 다운로드", "☆ 이미지 URL 다운로드", "☆ 전체 URL 크롤링", 
    "☆ 매입 이미지 다운로드", "☆ 사내판매 썸네일", "☆ 가격/재고 조회", 
    "☆ 이미지 비교 (테스트)", "☆ 이미지 비교 2 (테스트)", "☆ 이미지 비교 3 (테스트)", 
    "☆ 누끼 따기", "☆ 구글시트 데이터", "☆ 품번 등록확인", "☆ 판매 상품 검색"
]

selected_tab = st.radio("기능 선택", tool_tabs, horizontal=True, label_visibility="collapsed")

st.markdown("---")

if selected_tab == "☆ 데이터 다운로드":
    st.subheader("데이터 다운로드")
    st.caption("Redash 쿼리를 실행해 최신 데이터를 엑셀로 받습니다.")

    col1, col2 = st.columns([2, 1])

    with col1:
        # 1. 쿼리 선택
        query_option = st.selectbox(
            "쿼리 선택",
            ["페이머스 거래내역", "상품별 재고 현황", "일별 매출 집계", "회원가입/매출 통계"],
            index=0
        )
        st.success("🟢 연결됨 (Redash API)")

        # 2. 기간 설정
        d_col1, d_col2 = st.columns(2)
        with d_col1:
            start_date = st.date_input("기간 시작", value=date(2026, 1, 1))
        with d_col2:
            end_date = st.date_input("기간 종료", value=date(2026, 9, 21))

        # 3. 버튼 영역
        btn_col1, btn_col2, btn_col3 = st.columns(3)

        if "download_history" not in st.session_state:
            st.session_state.download_history = []

        if btn_col1.button("⬇️ 다운로드", use_container_width=True):
            # 테스트용 샘플 데이터
            data = {
                "거래일자": ["2026-09-01", "2026-09-02", "2026-09-03"],
                "상품명": ["상품 A", "상품 B", "상품 C"],
                "결제금액": [15000, 32000, 28000],
                "상태": ["완료", "완료", "취소"]
            }
            df = pd.DataFrame(data)

            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='거래내역')
            excel_data = output.getvalue()

            st.session_state.download_history.append({
                "time": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
                "query": query_option,
                "range": f"{start_date} ~ {end_date}"
            })

            st.download_button(
                label="💾 엑셀 파일 받기",
                data=excel_data,
                file_name=f"{query_option}_{start_date}_{end_date}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )

        if btn_col2.button("📋 복사", use_container_width=True):
            st.toast("클립보드 복사 기능 준비 중입니다.")

        if btn_col3.button("📊 시트 뷰로 바로 보기", use_container_width=True):
            st.write("### 📊 조회 결과 미리보기")
            sample_data = {
                "거래일자": ["2026-09-01", "2026-09-02", "2026-09-03"],
                "상품명": ["상품 A", "상품 B", "상품 C"],
                "결제금액": [15000, 32000, 28000],
                "상태": ["완료", "완료", "취소"]
            }
            st.dataframe(pd.DataFrame(sample_data), use_container_width=True)

    with col2:
        st.subheader("다운로드 내역")
        if st.button("🗑️ 지우기"):
            st.session_state.download_history = []
            st.rerun()

        if not st.session_state.download_history:
            st.info("내역 없음")
        else:
            for item in reversed(st.session_state.download_history):
                st.text(f"[{item['time']}]\n- {item['query']}\n- {item['range']}")
                st.markdown("---")

else:
    st.info(f"[{selected_tab}] 기능 준비 중입니다.")
