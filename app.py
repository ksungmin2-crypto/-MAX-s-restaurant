import streamlit as st
import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin

st.set_page_config(
    page_title="MAX's restaurant",
    page_icon="🔒",
    layout="wide"
)

# =========================
# 로그인 상태 저장
# =========================
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
# 로그인 후 화면
# =========================
st.title("🔒 MAX's restaurant")
st.success("맛점하세요.")


# 로그아웃
if st.sidebar.button("🚪 로그아웃"):
    st.session_state.logged_in = False
    st.rerun()


st.write("---")

st.subheader("⚙️ 크롤링 제어판")


# =========================
# 사이트 선택
# =========================
site_type = st.selectbox(
    "어디에서 수집할까요?",
    [
        "일반 웹사이트",
        "Shopify",
        "Cafe24"
    ]
)


# =========================
# URL 입력
# =========================
target_url = st.text_input(
    "수집할 사이트 주소",
    placeholder="https://example.com"
)


# =========================
# 크롤링 함수
# =========================
def crawl_website(url):

    # http가 없으면 자동 추가
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=15
    )

    response.raise_for_status()

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    data = []

    # 페이지에 있는 링크들을 찾음
    for link in soup.find_all("a", href=True):

        text = link.get_text(
            " ",
            strip=True
        )

        href = link.get("href")

        full_url = urljoin(
            url,
            href
        )

        if text:

            data.append({
                "텍스트": text,
                "주소": full_url
            })

    return pd.DataFrame(data)


# =========================
# 크롤링 시작 버튼
# =========================
if st.button(
    "🚀 데이터 수집 시작",
    type="primary"
):

    if target_url == "":

        st.warning(
            "사이트 주소를 입력해주세요."
        )

    else:

        progress = st.progress(
            10,
            text="사이트에 접속 중..."
        )

        try:

            progress.progress(
                40,
                text="웹페이지를 읽는 중..."
            )

            df = crawl_website(
                target_url
            )

            progress.progress(
                80,
                text="데이터를 정리하는 중..."
            )

            st.session_state["crawl_result"] = df

            progress.progress(
                100,
                text="수집 완료!"
            )

            st.success(
                f"총 {len(df)}개의 데이터를 가져왔습니다."
            )

        except Exception as e:

            st.error(
                f"수집 실패: {e}"
            )


# =========================
# 결과 화면
# =========================
if "crawl_result" in st.session_state:

    df = st.session_state["crawl_result"]

    st.write("---")

    st.subheader("📋 수집 결과")

    if df.empty:

        st.info(
            "가져온 데이터가 없습니다."
        )

    else:

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        csv = df.to_csv(
            index=False
        ).encode("utf-8-sig")

        st.download_button(
            "📥 CSV 다운로드",
            data=csv,
            file_name="crawl_result.csv",
            mime="text/csv"
        )
