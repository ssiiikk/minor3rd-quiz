import random
import streamlit as st

st.set_page_config(
    page_title="재즈기타 단3도 반사 훈련", page_icon="🎸", layout="centered"
)

# 3가지 단3도 그룹 정의 (F# 적용)
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
        "1. 순방향(상행) 단3도 맞추기",
        "2. 역방향(하행) 단3도 맞추기 (집중)",
        "3. 도미넌트 -> 단3도 그룹 찾기 (순서 무관)",
        "4. 무작위 상행/하행 퀴즈",
    ],
    key="mode_select",
)


# 문제 생성 함수
def generate_quiz():
  note = random.choice(ALL_NOTES)
  target_group = next(notes for notes in GROUPS.values() if note in notes)
  idx = target_group.index(note)
  current_mode = st.session_state.mode_select

  if current_mode == "1. 순방향(상행) 단3도 맞추기":
    st.session_state.quiz = {
        "type": "single",
        "prompt": f"기준 음 **[{note}]** 의 다음(상행/순방향) 단3도 음은?",
        "answer": target_group[(idx + 1) % 4],
    }
  elif current_mode == "2. 역방향(하행) 단3도 맞추기 (집중)":
    st.session_state.quiz = {
        "type": "single",
        "prompt": f"기준 음 **[{note}]** 의 바로 전(하행/역방향) 단3도 음은?",
        "answer": target_group[(idx - 1) % 4],
    }
  elif current_mode == "3. 도미넌트 -> 단3도 그룹 찾기 (순서 무관)":
    dom = random.choice(list(DOMINANTS.keys()))
    group_name = DOMINANTS[dom]
    st.session_state.quiz = {
        "type": "group",
        "prompt": f"도미넌트 코드 **[{dom}]** 의 단3도 그룹 4개 음은?",
        "answer_set": set(n.upper() for n in GROUPS[group_name]),
        "display_ans": " ".join(GROUPS[group_name]),
    }
  else:
    direction = random.choice(["상행(위로)", "하행(아래로)"])
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

  # 선택된 음 패드 초기화
  st.session_state.selected_notes = []


# State 초기화
if "quiz" not in st.session_state or st.session_state.get("prev_mode") != mode:
  st.session_state.prev_mode = mode
  generate_quiz()

if "score" not in st.session_state:
  st.session_state.score = {"correct": 0, "total": 0}
if "last_result" not in st.session_state:
  st.session_state.last_result = None
if "selected_notes" not in st.session_state:
  st.session_state.selected_notes = []


# 정답 확인 로직
def submit_answer(user_input_list):
  st.session_state.score["total"] += 1
  quiz = st.session_state.quiz

  if quiz["type"] == "single":
    user_ans = user_input_list[0].upper()
    correct_ans = quiz["answer"].upper()
    is_correct = user_ans == correct_ans
    correct_display = quiz["answer"]
  else:
    user_set = set(n.upper() for n in user_input_list)
    correct_set = quiz["answer_set"]
    is_correct = user_set == correct_set
    correct_display = quiz["display_ans"]

  if is_correct:
    st.session_state.score["correct"] += 1
    st.session_state.last_result = ("success", "🎉 정답입니다!")
  else:
    st.session_state.last_result = (
        "error",
        f"❌ 오답입니다. 정답: **{correct_display}**",
    )

  generate_quiz()


# 이전 결과 출력
if st.session_state.last_result:
  res_type, res_msg = st.session_state.last_result
  if res_type == "success":
    st.success(res_msg)
  else:
    st.error(res_msg)

st.markdown("---")
st.subheader(st.session_state.quiz["prompt"])

# 그룹 문제 시 현재 선택한 음 표시
if st.session_state.quiz["type"] == "group":
  st.write(
      "선택한 음:"
      f" **{' '.join(st.session_state.selected_notes) if st.session_state.selected_notes else '없음'}**"
  )

# --- 12개 음 패드 (버튼 입력) ---
st.markdown("#### 👇 음 선택")
cols = st.columns(4)  # 4열로 버튼 배치

for i, note in enumerate(ALL_NOTES):
  col = cols[i % 4]
  if col.button(note, key=f"btn_{note}", use_container_width=True):
    if st.session_state.quiz["type"] == "single":
      # 단일 음 문제는 클릭 즉시 제출
      submit_answer([note])
      st.rerun()
    else:
      # 그룹 문제는 선택한 음을 리스트에 추가 (최대 4개)
      if len(st.session_state.selected_notes) < 4:
        st.session_state.selected_notes.append(note)
        # 4개가 채워지면 자동 제출
        if len(st.session_state.selected_notes) == 4:
          submit_answer(st.session_state.selected_notes)
        st.rerun()

# 그룹 문제용 보조 버튼 (지우기 / 제출)
if st.session_state.quiz["type"] == "group":
  col_btn1, col_btn2 = st.columns(2)
  with col_btn1:
    if st.button("❌ 선택 지우기", use_container_width=True):
      st.session_state.selected_notes = []
      st.rerun()
  with col_btn2:
    if st.button("🎯 제출하기", use_container_width=True):
      if st.session_state.selected_notes:
        submit_answer(st.session_state.selected_notes)
        st.rerun()

st.markdown("---")
st.write(
    f"📊 **현재 점수:** {st.session_state.score['correct']} /"
    f" {st.session_state.score['total']} 회 정답"
)
