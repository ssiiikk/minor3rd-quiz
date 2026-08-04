import random
import streamlit as st

st.set_page_config(
    page_title="재즈기타 단3도 반사 훈련", page_icon="🎸", layout="centered"
)

# 3가지 그룹 정의
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

st.title("🎸 재즈기타 단3도 반사 훈련")

mode = st.radio(
    "연습 모드 선택",
    [
        "1. 역방향(하행) 단3도 맞추기 (집중)",
        "2. 도미넌트 -> 단3도 그룹 찾기",
        "3. 무작위 상행/하행 퀴즈",
    ],
)

# Session State 초기화
if "quiz" not in st.session_state:
  st.session_state.quiz = None
if "score" not in st.session_state:
  st.session_state.score = {"correct": 0, "total": 0}


def generate_quiz():
  if mode == "1. 역방향(하행) 단3도 맞추기 (집중)":
    note = random.choice(ALL_NOTES)
    target_group = next(notes for notes in GROUPS.values() if note in notes)
    idx = target_group.index(note)
    prev_note = target_group[(idx - 1) % 4]
    st.session_state.quiz = {
        "prompt": f"기준 음 **[{note}]** 의 바로 전(하행/역방향) 단3도 음은?",
        "answer": prev_note,
    }
  elif mode == "2. 도미넌트 -> 단3도 그룹 찾기":
    dom = random.choice(list(DOMINANTS.keys()))
    group_name = DOMINANTS[dom]
    st.session_state.quiz = {
        "prompt": f"도미넌트 코드 **[{dom}]** 의 단3도 그룹 4개 음은?",
        "answer": " ".join(GROUPS[group_name]),
    }
  else:
    note = random.choice(ALL_NOTES)
    direction = random.choice(["상행(위로)", "하행(아래로)"])
    target_group = next(notes for notes in GROUPS.values() if note in notes)
    idx = target_group.index(note)
    ans = (
        target_group[(idx + 1) % 4]
        if direction == "상행(위로)"
        else target_group[(idx - 1) % 4]
    )
    st.session_state.quiz = {
        "prompt": f"기준 음 **[{note}]** 의 **{direction}** 단3도 음은?",
        "answer": ans,
    }


col1, col2 = st.columns(2)
with col1:
  if st.button("🔄 새 문제 생성"):
    generate_quiz()

if st.session_state.quiz is None:
  generate_quiz()

st.markdown("---")
st.subheader(st.session_state.quiz["prompt"])

user_input = st.text_input("정답 입력 (예: Eb, F# 등)", key="user_ans")

if st.button("정답 확인 🎯"):
  correct_ans = st.session_state.quiz["answer"]
  st.session_state.score["total"] += 1

  # 입력 형태 다듬기 (대소문자 및 공백 수용)
  user_formatted = " ".join(user_input.strip().upper().split())
  ans_formatted = " ".join(correct_ans.strip().upper().split())

  if user_formatted == ans_formatted:
    st.success("🎉 정답입니다!")
    st.session_state.score["correct"] += 1
  else:
    st.error(f"❌ 오답입니다. 정답: **{correct_ans}**")

st.markdown("---")
st.write(
    f"📊 **현재 점수:** {st.session_state.score['correct']} /"
    f" {st.session_state.score['total']} 회 정답"
)