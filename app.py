import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="AI 생기부 도우미", layout="wide")

# 사이드바에서 API 키를 입력받음
with st.sidebar:
    st.header("🔑 보안 설정")
    user_api_key = st.text_input("Google API Key를 입력하세요", type="password")
    st.info("API 키는 서버에 저장되지 않고 브라우저를 닫으면 삭제됩니다.")
    
    st.markdown("---")
    category = st.selectbox("항목 선택", ["교과세특", "자율활동", "진로활동"])
    max_chars = st.slider("희망 글자 수", 100, 500, 500)

st.title("📝 AI 생활기록부 작성 도우미")

# 입력창과 결과창 로직
col1, col2 = st.columns(2)

with col1:
    raw_text = st.text_area("학생 활동 키워드 입력", height=300)
    generate_btn = st.button("생기부 초안 생성하기 ✨")

with col2:
    if generate_btn:
        if not user_api_key:
            st.error("API 키를 먼저 입력해주세요!")
        elif not raw_text:
            st.warning("내용을 입력해주세요.")
        else:
            try:
                # 사용자가 입력한 키로 Gemini 설정
                genai.configure(api_key=user_api_key)
                model = genai.GenerativeModel('gemini-2.5-flash')
                
                with st.spinner("생성 중..."):
                    prompt = f"너는 고등학교 생기부 전문가야. '{category}' 항목을 '{raw_text}' 내용을 바탕으로 작성해줘..."
                    response = model.generate_content(prompt)
                    st.success("생성 완료!")
                    st.write(response.text)
            except Exception as e:
                st.error(f"오류 발생: API 키가 올바른지 확인해주세요. ({e})")
