import streamlit as st
import google.generativeai as genai
from datetime import datetime

# 페이지 설정
st.set_page_config(page_title="AI 생기부 빌더 (2026 지침 준수)", layout="wide")

# --- [사전 지침] 2026 기재요령 요약본 내장 ---
GUIDELINE_SUMMARY = """
당신은 '2026학년도 학교생활기록부 기재요령'을 완벽히 준수하는 고등학교 교사입니다.
[공통 원칙]
1. 문체: 반드시 '~함', '~임', '~함이 돋보임'과 같은 명사형 종결 어미를 사용함.
2. 금지사항: 교외 수상, 부모 직업, 사교육 유발 요소(어학성적, 논문 등) 절대 기재 금지.
3. 서술방식: 추상적인 표현(매우 성실함 등) 대신 구체적인 활동 근거와 학생의 변화 위주로 서술함.
[항목별 주의점]
- 교과세특: 수업 중 탐구 과정과 성취기준에 따른 성장을 구체화할 것.
- 행발: 장단점을 균형 있게 적되 단점은 변화 가능성을 언급할 것.
- 자율/진로: 학교 교육과정 내 활동이어야 하며 주도성과 기여도를 강조할 것.
- 동아리: 자율동아리는 동아리명과 간단한 설명(30자)만 가능하며 본 동아리는 역할 위주 서술.
"""

# 사이드바 설정
with st.sidebar:
    st.title("⚙️ 설정")
    user_api_key = st.text_input("Google API Key 입력", type="password")
    target_length = st.slider("희망 글자 수 (공백 포함)", 100, 700, 500, step=50)
    st.divider()
    st.info("💡 자율/진로 활동은 활동명과 날짜가 자동으로 서식에 맞춰 입력됩니다.")

# 메인 타이틀
st.title("📝 AI 생활기록부 빌더")
st.caption("2026 기재요령 지침이 적용된 스마트 초안 생성기")

# 5개 분야 탭 구성
tabs = st.tabs(["교과세특", "행발종합", "자율활동", "진로활동", "동아리활동"])

# 공통 실행 함수
def generate_sangibu(category, context, extra_info=""):
    if not user_api_key:
        st.error("사이드바에 API 키를 입력해주세요.")
        return
    
    try:
        genai.configure(api_key=user_api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        {GUIDELINE_SUMMARY}
        
        [현재 항목]: {category}
        [목표 글자 수]: {target_length}자 내외
        [추가 정보]: {extra_info}
        [학생 활동 키워드]: {context}
        
        위 내용을 바탕으로 생기부 초안을 작성해줘. 
        글의 시작은 반드시 추가 정보가 있다면 그 형식을 따르고, 전체 문장은 명사형으로 끝맺음해줘.
        """
        
        with st.spinner("AI가 지침을 검토하며 작성 중입니다..."):
            response = model.generate_content(prompt)
            st.subheader(f"✅ {category} 생성 결과")
            st.text_area("복사해서 사용하세요", value=response.text, height=300)
            st.caption(f"공백 포함 약 {len(response.text)}자 생성됨")
    except Exception as e:
        st.error(f"오류가 발생했습니다: {e}")

# --- 탭별 레이아웃 ---

# 1. 교과세특
with tabs[0]:
    subject = st.text_input("과목명", placeholder="예: 정보, 수학 I")
    content = st.text_area("학생 활동 키워드 (세특)", placeholder="파이썬 알고리즘 설계 능력, 조장으로서 협업 유도 등", key="tab1")
    if st.button("세특 생성 ✨"):
        generate_sangibu("교과별 세부능력 및 특기사항", content, f"과목명: {subject}")

# 2. 행발종합
with tabs[1]:
    content = st.text_area("관찰 기록 및 특징 (행발)", placeholder="배려심이 깊음, 학급 비품 관리에 솔선수범함 등", key="tab2")
    if st.button("행발 의견 생성 ✨"):
        generate_sangibu("행동특성 및 종합의견", content)

# 3. 자율활동
with tabs[2]:
    act_name = st.text_input("활동 이름 (자율)", placeholder="학급 자치 회의")
    act_date = st.date_input("활동 날짜 (자율)", datetime.now())
    formatted_date = act_date.strftime("%Y.%m.%d.")
    content = st.text_area("활동 상세 내용", placeholder="학급 규칙 정하기 토론에서 사회를 맡음 등", key="tab3")
    
    extra = f"문장 시작 형식을 반드시 '{act_name}({formatted_date})'로 시작할 것."
    if st.button("자율활동 생성 ✨"):
        generate_sangibu("자율활동", content, extra)

# 4. 진로활동
with tabs[3]:
    act_name = st.text_input("활동 이름 (진로)", placeholder="진로 캠프 탐색 활동")
    act_date = st.date_input("활동 날짜 (진로)", datetime.now())
    formatted_date = act_date.strftime("%Y.%m.%d.")
    content = st.text_area("진로 탐색 및 상담 내용", placeholder="소프트웨어 개발자의 직업적 가치관에 대해 탐구함", key="tab4")
    
    extra = f"문장 시작 형식을 반드시 '{act_name}({formatted_date})'로 시작할 것."
    if st.button("진로활동 생성 ✨"):
        generate_sangibu("진로활동", content, extra)

# 5. 동아리활동
with tabs[4]:
    club_name = st.text_input("동아리 이름")
    is_autonomous = st.checkbox("자율동아리 여부")
    content = st.text_area("동아리 내 역할 및 활동", placeholder="코딩 동아리에서 챗봇 제작 프로젝트를 주도함", key="tab5")
    
    extra = f"동아리명: {club_name}, 자율동아리 여부: {is_autonomous}"
    if st.button("동아리활동 생성 ✨"):
        generate_sangibu("동아리 활동", content, extra)
