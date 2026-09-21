import pandas as pd
import requests
import streamlit as st

# 화면 제목 표시
st.title("📊 Redash 데이터 다운로더")
st.write("Redash API Key와 Query ID를 입력하여 최신 데이터를 추출합니다.")

# 사용자 입력창 만들기
redash_url = st.text_input("Redash 주소", value="https://redash.kroffle.net")
api_key = st.text_input("Redash API Key", type="password")
query_id = st.text_input("Query ID (숫자)")

# 버튼 클릭 시 실행
if st.button("데이터 추출하기"):
    if not api_key or not query_id:
        st.warning("API Key와 Query ID를 모두 입력해주세요.")
    else:
        try:
            # Redash에서 데이터 불러오기
            endpoint = f"{redash_url.rstrip('/')}/api/queries/{query_id}/results.csv?api_key={api_key}"
            response = requests.get(endpoint)

            if response.status_code == 200:
                from io import StringIO

                df = pd.read_csv(StringIO(response.text))

                st.success("데이터를 성공적으로 불러왔습니다!")
                st.dataframe(df)

                # 파일 다운로드 버튼 생성
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
