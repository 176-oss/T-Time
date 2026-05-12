import streamlit as st
import google.generativeai as genai
import pdfplumber # PDF 텍스트 추출용

# 1. PDF에서 기재요령 텍스트를 추출하는 함수
def extract_guidelines(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        # 모든 페이지를 다 읽으면 너무 길어지므로, 핵심 페이지(예: 1~50페이지) 위주로 추출 가능
        for page in pdf.pages[10:60]: # 기재 일반 원칙 및 항목별 예시가 있는 구간
            text += page.extract_text()
    return text

# 페이지 설정
st.set_page_config(page_title="2026 생기부 가이드 챗", layout="wide")

# 사이드바에서 API 키 입력
with st.sidebar:
    user_api_key = st.text_input("Google API Key", type="password")
    st.info("2026 기재요령 PDF가 서버에 로드되어 있습니다.")

# --- 서버에 올려둔 PDF 읽기 ---
# (미리 업로드하신 파일 이름을 'guideline.pdf'로 가정합니다)
try:
    guideline_context = extract_guidelines("2026 학교생활기록부 기재요령(중)_F_260227.pdf")
except:
    guideline_context = "기재요령 파일을 찾을 수 없습니다. 기본 지침으로 작성합니다."

st.title("🛡️ 2026 지침 준수 생기부 작성기")

col1, col2 = st.columns(2)

with col1:
    category = st.selectbox("항목", ["교과세특", "자율활동", "진로활동"])
    raw_input = st.text_area("학생 활동 키워드", height=300)
    generate_btn = st.button("지침 준수하여 작성하기")

with col2:
    if generate_btn and user_api_key:
        genai.configure(api_key=user_api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # 지침을 포함한 강력한 프롬프트 구성
        full_prompt = f"""
        당신은 아래의 '2026 학교생활기록부 기재요령'을 완벽하게 숙지한 전문가입니다.
        
        [참조 지침 요약]
        {guideline_context[:10000]} # 토큰 제한을 고려해 핵심 1만자 전달
        
        [요청 사항]
        위 지침을 바탕으로 다음 학생의 {category} 내용을 작성하세요.
        입력된 데이터: {raw_input}
        
        [반드시 지킬 것]
        1. 지침에 명시된 '기재 금지 사항'(부모 직업, 수상경력 등)이 포함되었는지 확인하고 절대 쓰지 말 것.
        2. '~함', '~임' 등의 명사형 종결 어미 사용.
        3. 지침에 나온 항목별 권장 예시 문체를 따를 것.
        """
        
        with st.spinner("지침 검토 및 작성 중..."):
            response = model.generate_content(full_prompt)
            st.success("작성 완료!")
            st.write(response.text)
