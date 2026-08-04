import random
import streamlit as st

st.set_page_config(
    page_title="재즈기타 단3도 반사 훈련", page_icon="🎸", layout="centered"
)

# 3가지 단3도 그룹 정의 (F# 적용)
GROUPS = {
    "Group A": ["Ab", "B", "D", "F"],
    "Group B": ["A", "C", "Eb", "F#"],  # F# 표기 적용
    "Group C": ["Bb", "Db", "E", "G"],
}

# 도미넌트 코드 매핑
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
        "2. 도미넌트 -> 단3도 그룹 찾기 (순서 무관)",
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
        "type": "single",
        "prompt": f"기준 음 **[{note}]** 의 바로 전(하행/역방향) 단3도 음은?",
        "answer": prev_note,
    }
  elif mode == "2. 도미넌트 -> 단3도 그룹 찾기 (순서 무관)":
    dom = random.choice(list(DOMINANTS.keys()))
    group_name = DOMINANTS[dom]
    st.session_state.quiz = {
        "type": "group",
        "prompt": f"도미넌트 코드 **[{dom}]** 의 단3도 그룹 4개 음은?",
        # 정답 비교용 집합(set) 구성
        "answer_set": set(n.upper() for n in GROUPS[group_name]),
        "display_ans": " ".join(GROUPS[group_name]),
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
        "type": "single",
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

user_input = st.text_input(
    "정답 입력 (예: Ab B D F 또는 B D F Ab 등 순서 상관없음)", key="user_ans"
)

if st.button("정답 확인 🎯"):
  st.session_state.score["total"] += 1

  # 단일 음 문제
  if st.session_state.quiz["type"] == "single":
    user_formatted = user_input.strip().upper()
    correct_formatted = st.session_state.quiz["answer"].upper()
    is_correct = user_formatted == correct_formatted
    correct_display = st.session_state.quiz["answer"]

  # 4개 음 그룹 문제 (순서 상관없이 집합으로 검증)
  else:
    # 쉼표나 공백으로 구분된 입력을 집합(set)으로 변환
    user_set = set(user_input.strip().upper().replace(",", " ").split())
    correct_set = st.session_state.quiz["answer_set"]
    is_correct = user_set == correct_set
    correct_display = st.session_state.quiz["display_ans"]

  if is_correct:
    st.success("🎉 정답입니다!")
    st.session_state.score["correct"] += 1
  else:
    st.error(f"❌ 오답입니다. 정답 구성음: **{correct_display}**")

st.markdown("---")
st.write(
    f"📊 **현재 점수:** {st.session_state.score['correct']} /"
    f" {st.session_state.score['total']} 회 정답"
)
