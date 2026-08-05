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
    next_note = target_group[(idx + 1) % 4]
    st.session_state.quiz = {
        "type": "single",
        "prompt": f"기준 음 **[{note}]** 의 다음(상행/순방향) 단3도 음은?",
        "answer": next_note,
    }
  elif current_mode == "2. 역방향(하행) 단3도 맞추기 (집중)":
    prev_note = target_group[(idx - 1) % 4]
    st.session_state.quiz = {
        "type": "single",
        "prompt": f"기준 음 **[{note}]** 의 바로 전(하행/역방향) 단3도 음은?",
        "answer": prev_note,
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


# Session State 초기화
if "quiz" not in st.session_state or st.session_state.get("prev_mode") != mode:
  st.session_state.prev_mode = mode
  st.session_state.last_result = None
  generate_quiz()

if "score" not in st.session_state:
  st.session_state.score = {"correct": 0, "total": 0}
if "last_result" not in st.session_state:
  st.session_state.last_result = None


# 정답 제출 및 검증 콜백
def check_answer():
  user_input = st.session_state.user_ans.strip()

  if not user_input:
    return

  st.session_state.score["total"] += 1

  # 단일 음 검증
  if st.session_state.quiz["type"] == "single":
    user_formatted = user_input.upper()
    correct_formatted = st.session_state.quiz["answer"].upper()
    is_correct = user_formatted == correct_formatted

  # 그룹 음 검증 (순서 무관)
  else:
    user_set = set(user_input.upper().replace(",", " ").split())
    correct_set = st.session_state.quiz["answer_set"]
    is_correct = user_set == correct_set

  # 결과 처리
  if is_correct:
    st.session_state.score["correct"] += 1
    st.session_state.last_result = ("success", "🎉 정답입니다! 다음 문제로 넘어갑니다.")
    st.session_state.user_ans = ""  # 정답일 때만 입력창 비우기
    generate_quiz()  # 정답일 때만 다음 문제 생성
  else:
    st.session_state.last_result = (
        "error",
        "❌ 오답입니다. 다시 한번 생각해보세요!",
    )
    # 오답일 때는 generate_quiz()를 호출하지 않고 문제를 그대로 유지


st.markdown("---")
# 1. 문제 출력
st.subheader(st.session_state.quiz["prompt"])

# 2. 정답/오답 결과 메시지 표시
if st.session_state.last_result:
  res_type, res_msg = st.session_state.last_result
  if res_type == "success":
    st.success(res_msg)
  else:
    st.error(res_msg)

# 3. 입력 창
st.text_input(
    "정답을 입력하고 Enter를 누르세요",
    key="user_ans",
    on_change=check_answer,
    placeholder="예: Eb / F# / Ab B D F 등 입력 후 Enter",
)

st.markdown("---")
st.write(
    f"📊 **현재 점수:** {st.session_state.score['correct']} /"
    f" {st.session_state.score['total']} 회 시도"
)
