import streamlit as st
import google.generativeai as genai

# 1. 웹페이지 기본 설정
st.set_page_config(page_title="명품 교과 세특 생성기", page_icon="📝")
st.title("📝 베테랑 교사의 명품 교과 세특 생성기")
st.markdown("전국 5대 대학 유형의 평가 기준과 선생님의 시그니처 문체를 완벽히 반영한 교과 맞춤형 세특 프로그램입니다.")

# 2. 사이드바 (API 키 설정)
with st.sidebar:
    st.header("🔑 환경 설정")
    api_key = st.text_input("Google Gemini API Key", type="password", help="발급받은 구글 API 키를 입력하세요.")
    st.markdown("---")
    st.markdown("✔ 동료 선생님들과 링크를 공유하여 함께 사용할 수 있습니다.")

# 3. 사용자 입력 칸 만들기
st.subheader("📋 학생 데이터 입력")

col1, col2 = st.columns(2)
with col1:
    subject = st.text_input("교과목명", placeholder="예: 영어 독해와 작문, 심화 국어, 미적분 등")
with col2:
    uni_type = st.selectbox("희망 대학 유형", ["과학기술원형", "최상위권대형", "상위권대형", "국립대형", "중위권대형"])

major = st.text_input("희망 학과(계열)", placeholder="예: 컴퓨터공학과, 경영학과, 간호학과 등")
attitude = st.text_input("선생님이 묘사할 학생의 평소 태도", placeholder="예: 차분하고 집중력이 뛰어나며 지적 호기심이 풍부함")
activity_data = st.text_area("학생 탐구 및 활동 내용", placeholder="수업 중 생긴 의문점, 읽은 원서/논문, 발표 내용, 겪었던 어려움 등을 적어주세요.", height=150)

# 4. 프롬프트 (교과 세특용 마스터 규칙)
system_prompt = """
[System Role]
당신은 서울대, 연세대 등 전국 5대 대학 유형별 서류평가 기준을 완벽히 꿰뚫고 있으며, 학생에 대한 애정과 객관적 학술 문체를 융합해 최상위권 교과 세특을 작성하는 베테랑 교사입니다. 제공된 데이터를 바탕으로 아래 [지침]을 100% 준수하여 500자 내외의 명품 교과 세특을 출력하십시오.

[마스터 명령 규칙]
1. 금지어 필터링: 공인어학성적, 사교육 스펙, 외부 대회, 단순 "~참여함" 식의 결과 나열 절대 금지.
2. 교과목 성취수준 명시화: 입력된 [교과목명]에 걸맞은 구체적인 '행동 동사(~파악함, ~추론함, ~분석함)'와 교과 전문 용어(예: 영어의 경우 상관어, 분사 구문 등)를 문맥에 맞게 1~2개 자연스럽게 녹여낼 것.
3. 선생님 시그니처 5법칙 적용:
   - 도입부: 제시된 [학생의 평소 태도]를 바탕으로 고유한 인성/태도를 묘사하며 시작할 것.
   - 결말부: 미래 잠재력을 극찬 ("~우수한 학업 성취를 이룰 다재다능한 인재로 성장할 가능성이 큼")하며 닫을 것.
   - 시그니처 수식어: '오롯이', '매끄럽게', '유려한', '명료한', '예리한 통찰력' 필수 사용.
   - 인문/전공 융합: 단순 지식을 넘어 인문학적 성찰과 희망 전공 지식을 유기적으로 엮어낼 것.

4. ★ [대학 유형별 황금 구조 분기 적용]: 
   - [과학기술원형]: 교과 의문 도출 ➡️ 자기주도 원서/논문 탐구 ➡️ 공학 도구/실험 융합 및 한계 극복 ➡️ 연구원 자질 성장
   - [최상위권대형]: 교과 의문 도출 ➡️ 원서/학술 칼럼 심화 독해 ➡️ 비판적 사고 기반 인문/과학 융합 및 대안 제시 ➡️ 학자적 잠재력
   - [상위권대형]: 교과 내 문제의식 발굴 ➡️ 전공 지식 연계 솔루션 탐색 ➡️ 협업/실천을 통한 성과 ➡️ 전공 기초 소양 도출
   - [국립대형]: 교과 단원 학습 중 전공/이슈 연계 의문 ➡️ 표준 자료 조사 ➡️ 급우들과의 소통/협업으로 해결 ➡️ 공동체 역량 성장
   - [중위권대형]: 교과 핵심 개념에 관심 ➡️ 철저한 교과서 구조 파악 ➡️ 성실한 교실 내 적용 및 극복 ➡️ 기본 학업 역량 성장
"""

# 5. 생성 버튼 및 실행 로직
if st.button("✨ 교과 세특 생성하기"):
    if not api_key:
        st.error("좌측 메뉴에 API Key를 먼저 입력해주세요!")
    elif not subject or not major or not activity_data:
        st.warning("교과목명, 희망 학과, 학생 활동 데이터를 모두 입력해주세요.")
    else:
        with st.spinner("선생님의 문체를 모방하여 명품 교과 세특을 작성 중입니다..."):
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-1.5-pro')
                
                user_prompt = f"[Data Input]\n- 교과목명: {subject}\n- 희망 대학 유형: {uni_type}\n- 희망 학과: {major}\n- 학생의 평소 태도: {attitude}\n- 학생 활동 데이터: {activity_data}"
                
                response = model.generate_content(system_prompt + "\n\n" + user_prompt)
                
                st.success("✅ 세특 생성 완료!")
                st.write(response.text)
            except Exception as e:
                st.error(f"오류가 발생했습니다. API 키가 정확한지 확인해주세요. (에러내용: {e})")
