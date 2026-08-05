import random
import streamlit as st

st.set_page_config(
    page_title="재즈기타 단3도 반사 훈련", page_icon="🎸", layout="centered"
)

# 모바일 화면에 맞춘 컴팩트 CSS 스타일
st.markdown(
    """
    <style>
    /* 전체 여백 축소 */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 1rem !important;
        padding-left: 0.8rem !important;
        padding-right: 0.8rem !important;
    }
    /* 버튼 높이, 여백 및 폰트 사이즈 컴팩트화 */
    div.stButton > button {
        padding: 4px 0px !important;
        font-size: 15px !important;
        font-weight: bold !important;
        min-height: 38px !important;
        margin: 0px !important;
    }
    /* 서브헤더 및 텍스트 간격 줄임 */
    h3 {
        font-size: 1.1rem !important;
        margin-bottom: 0.3rem !important;
    }
    hr {
        margin: 0.5rem 0 !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# 3가지 단3도 그룹 정의
GROUPS = {
    "Group A": ["Ab", "B", "D", "F"],
    "Group B": ["A", "C", "Eb", "F#"],
    "Group C": ["Bb", "Db", "E", "G"],
}

DOMINANTS = {
    "G7": "Group A",
    "Bb7": "Group A",
    "Db7": "Group A",
    "E7": "Group A",
    "Ab7": "Group B",
    "B7": "Group B",
    "D7": "Group B",
    "F7": "Group B",
    "A7": "Group C",
    "C7": "Group C",
    "Eb7": "Group C",
    "F#7": "Group C",
}

ALL_NOTES = ["C", "Db", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]

# 헤더
st.markdown("### 🎸 단3도 반사 훈련")

mode = st.radio(
    "모드",
    [
        "1. 순방향(상행)",
        "2. 역방향(하행)",
        "3. 도미넌트 그룹",
        "4. 무작위 혼합",
    ],
    horizontal=True,  # 가로로 배치하여 공간 절약
    key="mode_select",
)


def generate_quiz():
  note = random.choice(ALL_NOTES)
  target_group = next(notes for notes in GROUPS.values() if note in notes)
  idx = target_group.index(note)
  current_mode = st.session_state.mode_select

  if current_mode == "1. 순방향(상행)":
    st.session_state.quiz = {
        "type": "single",
        "prompt": f"기준 음 **[{note}]** 의 다음(상행) 단3도는?",
        "answer": target_group[(idx + 1) % 4],
    }
  elif current_mode == "2. 역방향(하행)":
    st.session_state.quiz = {
        "type": "single",
        "prompt": f"기준 음 **[{note}]** 의 바로 전(하행) 단3도는?",
        "answer": target_group[(idx - 1) % 4],
    }
  elif current_mode == "3. 도미넌트 그룹":
    dom = random.choice(list(DOMINANTS.keys()))
    group_name = DOMINANTS[dom]
    st.session_state.quiz = {
        "type": "group",
        "prompt": f"코드 **[{dom}]** 의 단3도 4개 음은?",
        "answer_set": set(n.upper() for n in GROUPS[group_name]),
        "display_ans": " ".join(GROUPS[group_name]),
    }
  else:
    direction = random.choice(["상행", "하행"])
    ans = (
        target_group[(idx + 1) % 4]
        if direction == "상행"
        else target_group[(idx - 1) % 4]
    )
    st.session_state.quiz = {
        "type": "single",
        "prompt": f"기준 음 **[{note}]** 의 **{direction}** 단3도는?",
        "answer": ans,
    }

  st.session_state.selected_notes = []
  st.session_state.last_result = None


if "quiz" not in st.session_state or st.session_state.get("prev_mode") != mode:
  st.session_state.prev_mode = mode
  generate_quiz()

if "score" not in st.session_state:
  st.session_state.score = {"correct": 0, "total": 0}
if "last_result" not in st.session_state:
  st.session_state.last_result = None
if "selected_notes" not in st.session_state:
  st.session_state.selected_notes = []


def submit_answer(user_input_list):
  st.session_state.score["total"] += 1
  quiz = st.session_state.quiz

  if quiz["type"] == "single":
    user_ans = user_input_list[0].upper()
    correct_ans = quiz["answer"].upper()
    is_correct = user_ans == correct_ans
  else:
    user_set = set(n.upper() for n in user_input_list)
    correct_set = quiz["answer_set"]
    is_correct = user_set == correct_set

  if is_correct:
    st.session_state.score["correct"] += 1
    st.session_state.last_result = ("success", "🎉 정답입니다!")
    generate_quiz()
  else:
    wrong_notes_str = " ".join(user_input_list)
    st.session_state.last_result = (
        "warning",
        f"❌ **{wrong_notes_str}** 오답! 다시 생각해보세요.",
    )
    st.session_state.selected_notes = []


# 상단 결과 메세지
if st.session_state.last_result:
  res_type, res_msg = st.session_state.last_result
  if res_type == "success":
    st.success(res_msg)
  elif res_type == "warning":
    st.warning(res_msg)

# 문제 및 패스 버튼
col_prompt, col_skip = st.columns([3, 1])
with col_prompt:
  st.markdown(f"### {st.session_state.quiz['prompt']}")
with col_skip:
  if st.button("⏭️ 패스", use_container_width=True):
    ans_text = (
        st.session_state.quiz["answer"]
        if st.session_state.quiz["type"] == "single"
        else st.session_state.quiz["display_ans"]
    )
    st.session_state.last_result = ("warning", f"💡 정답: **{ans_text}**")
    generate_quiz()
    st.rerun()

if st.session_state.quiz["type"] == "group":
  st.caption(
      "선택:"
      f" **{' '.join(st.session_state.selected_notes) if st.session_state.selected_notes else '없음'}**"
  )

# 12개 음 패드 (3행 4열 컴팩트 배치)
cols = st.columns(4)
for i, note in enumerate(ALL_NOTES):
  col = cols[i % 4]
  if col.button(note, key=f"btn_{note}", use_container_width=True):
    if st.session_state.quiz["type"] == "single":
      submit_answer([note])
      st.rerun()
    else:
      if len(st.session_state.selected_notes) < 4:
        st.session_state.selected_notes.append(note)
        if len(st.session_state.selected_notes) == 4:
          submit_answer(st.session_state.selected_notes)
        st.rerun()

# 그룹 모드 지우기 버튼
if st.session_state.quiz["type"] == "group":
  if st.button("❌ 선택 지우기", use_container_width=True):
    st.session_state.selected_notes = []
    st.rerun()

st.markdown("---")
st.caption(
    f"📊 **점수:** {st.session_state.score['correct']} /"
    f" {st.session_state.score['total']} 회"
)
