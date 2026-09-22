import streamlit as st
from streamlit_autorefresh import st_autorefresh
import time
import random
import base64
from pathlib import Path

from sudoku import generate_puzzle, check_board


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Sudoku CSP Game",
    page_icon="🧩",
    layout="wide"
)


# =========================================================
# BACKGROUND FUNCTIONS
# =========================================================

BACKGROUND_FOLDER = Path(__file__).parent / "backgrounds"


def get_image_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()


def get_random_background():
    scenes = [
        BACKGROUND_FOLDER / "scene1.jpg",
        BACKGROUND_FOLDER / "scene2.jpg",
        BACKGROUND_FOLDER / "scene3.jpg",
        BACKGROUND_FOLDER / "scene4.jpg"
    ]

    existing_scenes = [
        scene for scene in scenes
        if scene.exists()
    ]

    if not existing_scenes:
        return None

    if "background_image" in st.session_state:
        available_scenes = [
            scene for scene in existing_scenes
            if scene != st.session_state.background_image
        ]

        if available_scenes:
            return random.choice(available_scenes)

    return random.choice(existing_scenes)


# =========================================================
# SESSION STATE
# =========================================================

if "game_started" not in st.session_state:
    st.session_state.game_started = False

if "background_image" not in st.session_state:
    st.session_state.background_image = get_random_background()

if "game_finished" not in st.session_state:
    st.session_state.game_finished = False

if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()

if "end_time" not in st.session_state:
    st.session_state.end_time = time.time()

if "game_id" not in st.session_state:
    st.session_state.game_id = 0


# =========================================================
# BACKGROUND STYLING
# =========================================================

if st.session_state.background_image is not None:

    background_base64 = get_image_base64(
        st.session_state.background_image
    )

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image:
                linear-gradient(
                    rgba(10, 18, 45, 0.48),
                    rgba(10, 18, 45, 0.48)
                ),
                url("data:image/jpeg;base64,{background_base64}");

            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            background-repeat: no-repeat;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# GENERAL DESIGN CSS
# =========================================================

st.markdown(
    """
    <style>

    /* Remove unnecessary Streamlit elements */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }


    /* Main headings */

    h1, h2, h3 {
        color: #66b3ff !important;
        -webkit-text-fill-color: #66b3ff !important;
        text-shadow: 0 2px 8px rgba(0, 0, 0, 0.45);
    }


    /* Buttons */

    .stButton > button {
        width: 100%;
        min-height: 45px;
        border-radius: 12px;
        font-weight: 700;
        border: none;
        transition: all 0.2s ease-in-out;
    }

    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 18px rgba(0, 0, 0, 0.30);
    }

    .stButton > button:active {
        transform: scale(0.97);
    }


    /* Text inputs */

    .stTextInput input {
        height: 46px !important;
        min-height: 46px !important;
        padding: 0 !important;

        text-align: center !important;
        font-size: 21px !important;
        font-weight: 800 !important;

        color: #66b3ff !important;
        -webkit-text-fill-color: #66b3ff !important;

        background: rgba(24, 27, 40, 0.96) !important;

        border: 1px solid rgba(255, 255, 255, 0.20) !important;
        border-radius: 4px !important;

        transition:
            transform 0.18s ease,
            box-shadow 0.18s ease,
            border 0.18s ease;
    }

    .stTextInput input:hover {
        transform: scale(1.04);
        border: 2px solid #8da9ff !important;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.35);
    }

    .stTextInput input:focus {
        transform: scale(1.06);
        border: 2px solid #b6c7ff !important;
        box-shadow: 0 0 0 3px rgba(120, 160, 255, 0.35);
    }


    /* Original puzzle numbers */

    .stTextInput input:disabled {
        color: #f4d58d !important;
        -webkit-text-fill-color: #f4d58d !important;

        background: rgba(45, 48, 65, 0.98) !important;

        opacity: 1 !important;

        border: 1px solid rgba(244, 213, 141, 0.45) !important;
    }


    /* Spacing between Streamlit columns */

    [data-testid="stHorizontalBlock"] {
        gap: 1.2rem !important;
    }


    /* Sudoku 3×3 box containers */

    [data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(5, 15, 38, 0.98);

        border: 3px solid #668cff;
        border-radius: 8px;

        padding: 5px;

        box-shadow:
            0 0 12px rgba(75, 125, 255, 0.18),
            0 8px 20px rgba(0, 0, 0, 0.35);
    }


    /* Sidebar */

    [data-testid="stSidebar"] {
        background: rgba(12, 18, 40, 0.94);
    }

    [data-testid="stSidebar"] * {
        color: white;
    }


    /* Information cards */

    .info-card {
        background: rgba(15, 22, 48, 0.90);

        border: 1px solid rgba(255, 255, 255, 0.25);
        border-radius: 18px;

        padding: 30px 24px;
        margin: 14px 8px;

        min-height: 150px;

        color: white;
        text-align: center;

        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.28);
    }


    /* Clearly visible error messages */

    [data-testid="stAlert"] {
        border: 2px solid #ff4b4b !important;
        border-radius: 12px !important;
        background: rgba(80, 10, 20, 0.95) !important;
        color: white !important;
        font-weight: 700 !important;
        box-shadow: 0 0 15px rgba(255, 75, 75, 0.35);
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# HOME SCREEN
# =========================================================

if not st.session_state.game_started:

    st.write("")
    st.write("")
    st.write("")

    left_space, center_space, right_space = st.columns(
        [1, 2, 1]
    )

    with center_space:

        st.title("🧩 Sudoku CSP Game")

        st.subheader(
            "Welcome to the Constraint Challenge! 🎯"
        )

        st.write("")
        st.write("### 🚀 Ready to test your logic?")

        if st.button(
            "🚀 START CHALLENGE",
            use_container_width=True
        ):

            st.session_state.game_started = True

            st.session_state.background_image = (
                get_random_background()
            )

            puzzle, solution = generate_puzzle("Medium")

            st.session_state.puzzle = puzzle
            st.session_state.solution = solution

            st.session_state.board = [
                row[:] for row in puzzle
            ]

            st.session_state.difficulty = "Medium"
            st.session_state.start_time = time.time()
            st.session_state.end_time = time.time()
            st.session_state.game_finished = False
            st.session_state.game_id = 0

            st.rerun()

    st.stop()


# =========================================================
# GAME SCREEN HEADER
# =========================================================

st.title("🧩 Sudoku CSP Game")

st.caption(
    "A Constraint Satisfaction Problem game based on Sudoku"
)


# =========================================================
# TOP INFORMATION CARDS
# =========================================================

info_col1, info_col2, info_col3 = st.columns(3)

with info_col1:

    st.markdown(
        """
        <div class="info-card">
            <h4>🎯 Objective</h4>
            Complete the Sudoku grid correctly.
        </div>
        """,
        unsafe_allow_html=True
    )

with info_col2:

    st.markdown(
        """
        <div class="info-card">
            <h4>🧠 Variables</h4>
            Empty cells with values from 1–9.
        </div>
        """,
        unsafe_allow_html=True
    )

with info_col3:

    st.markdown(
        """
        <div class="info-card">
            <h4>🔒 Constraints</h4>
            No repetition in rows, columns, or boxes.
        </div>
        """,
        unsafe_allow_html=True
    )


st.write("")


# =========================================================
# SIDEBAR CONTROLS
# =========================================================

st.sidebar.title("🎮 Game Controls")

difficulty = st.sidebar.selectbox(
    "Choose Difficulty",
    ["Easy", "Medium", "Hard"],
    index=["Easy", "Medium", "Hard"].index(
        st.session_state.difficulty
    )
)


if st.sidebar.button("🔄 New Game"):

    puzzle, solution = generate_puzzle(difficulty)

    st.session_state.background_image = (
        get_random_background()
    )

    st.session_state.puzzle = puzzle
    st.session_state.solution = solution

    st.session_state.board = [
        row[:] for row in puzzle
    ]

    st.session_state.difficulty = difficulty
    st.session_state.start_time = time.time()
    st.session_state.end_time = time.time()
    st.session_state.game_finished = False
    st.session_state.game_id += 1

    st.rerun()


if st.sidebar.button("↩️ Reset Puzzle"):

    st.session_state.board = [
        row[:] for row in st.session_state.puzzle
    ]

    st.session_state.start_time = time.time()
    st.session_state.end_time = time.time()
    st.session_state.game_finished = False
    st.session_state.game_id += 1

    st.rerun()


if st.sidebar.button("🏠 Back to Home"):

    st.session_state.game_started = False
    st.session_state.game_finished = False

    st.rerun()


st.sidebar.markdown("---")

st.sidebar.subheader("📚 CSP Explanation")

st.sidebar.write("**Variables:** Empty Sudoku cells")
st.sidebar.write("**Domain:** Numbers from 1 to 9")
st.sidebar.write("**Constraints:**")
st.sidebar.write("• No duplicate in a row")
st.sidebar.write("• No duplicate in a column")
st.sidebar.write("• No duplicate in a 3×3 box")


# =========================================================
# DIFFICULTY DISPLAY
# =========================================================

st.write("")

difficulty_col1, difficulty_col2 = st.columns(2)

with difficulty_col1:

    st.markdown(
        f"""
        <div class="info-card">
            <h4>Difficulty</h4>
            <h3>{st.session_state.difficulty}</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

with difficulty_col2:

    st.markdown(
        """
        <div class="info-card">
            <h4>Number System</h4>
            <h3>1 – 9</h3>
        </div>
        """,
        unsafe_allow_html=True
    )


st.write("")
st.subheader("📝 Solve the Sudoku")


# =========================================================
# TIMER AND PROGRESS INDICATOR
# =========================================================

# Refresh every second only while the game is active
if not st.session_state.game_finished:

    st_autorefresh(
        interval=1000,
        key="sudoku_timer"
    )


if st.session_state.game_finished:

    elapsed_seconds = int(
        st.session_state.end_time
        - st.session_state.start_time
    )

else:

    elapsed_seconds = int(
        time.time()
        - st.session_state.start_time
    )


minutes = elapsed_seconds // 60
seconds = elapsed_seconds % 60


completed_cells = 0
total_empty_cells = 0

for row in range(9):

    for col in range(9):

        if st.session_state.puzzle[row][col] == 0:

            total_empty_cells += 1

            if st.session_state.board[row][col] != 0:
                completed_cells += 1


progress_percentage = (
    completed_cells / total_empty_cells
    if total_empty_cells > 0
    else 0
)


timer_col, progress_col = st.columns(2)

with timer_col:

    st.markdown(
        f"""
        <div class="info-card">
            <h4>⏱️ Time Elapsed</h4>
            <h2>{minutes:02d}:{seconds:02d}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

with progress_col:

    st.markdown(
        f"""
        <div class="info-card">
            <h4>📊 Puzzle Progress</h4>
            <h2>{completed_cells} / {total_empty_cells}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )


st.progress(
    progress_percentage,
    text=(
        f"Completed: {completed_cells} "
        f"of {total_empty_cells} empty cells"
    )
)

st.write("")


# =========================================================
# SUDOKU BOARD
# =========================================================

st.markdown(
    """
    <div style="
        text-align: center;
        color: white;
        font-size: 18px;
        font-weight: 600;
        margin-bottom: 18px;
    ">
        Fill the empty cells and satisfy every constraint
    </div>
    """,
    unsafe_allow_html=True
)


left_space, board_space, right_space = st.columns(
    [1, 3, 1]
)

with board_space:

    for box_row in range(3):

        box_row_columns = st.columns(
            3,
            gap="small"
        )

        for box_col in range(3):

            with box_row_columns[box_col]:

                with st.container(border=True):

                    for local_row in range(3):

                        row = box_row * 3 + local_row

                        cell_columns = st.columns(
                            3,
                            gap="small"
                        )

                        for local_col in range(3):

                            col = box_col * 3 + local_col

                            with cell_columns[local_col]:

                                original_value = (
                                    st.session_state.puzzle[row][col]
                                )

                                # Fixed puzzle number
                                if original_value != 0:

                                    st.text_input(
                                        label="",
                                        value=str(original_value),
                                        disabled=True,
                                        key=(
                                            f"given_"
                                            f"{st.session_state.game_id}_"
                                            f"{row}_{col}"
                                        ),
                                        label_visibility="collapsed"
                                    )

                                # Editable player cell
                                else:

                                    current_value = (
                                        st.session_state.board[row][col]
                                    )

                                    value = st.text_input(
                                        label="",
                                        value=(
                                            ""
                                            if current_value == 0
                                            else str(current_value)
                                        ),
                                        max_chars=1,
                                        key=(
                                            f"cell_"
                                            f"{st.session_state.game_id}_"
                                            f"{row}_{col}"
                                        ),
                                        label_visibility="collapsed"
                                    )

                                    if value.isdigit():

                                        number = int(value)

                                        if 1 <= number <= 9:

                                            st.session_state.board[row][col] = (
                                                number
                                            )

                                    elif value == "":

                                        st.session_state.board[row][col] = 0

                                    else:

                                        st.session_state.board[row][col] = 0


# =========================================================
# ACTION BUTTONS
# =========================================================

st.write("")
st.divider()

action_col1, action_col2, action_col3 = st.columns(3)


with action_col1:

    if st.button(
        "✅ CHECK ANSWER",
        use_container_width=True
    ):

        if check_board(
            st.session_state.board,
            st.session_state.solution
        ):

            # Stop the timer
            st.session_state.game_finished = True
            st.session_state.end_time = time.time()

            elapsed = int(
                st.session_state.end_time
                - st.session_state.start_time
            )

            minutes = elapsed // 60
            seconds = elapsed % 60

            st.balloons()

            st.success(
                f"🎉 PUZZLE SOLVED! "
                f"You completed it in "
                f"{minutes} minutes and {seconds} seconds."
            )

        else:

            st.error(
                "❌ PUZZLE NOT SOLVED. "
                "Check your rows, columns, and 3×3 boxes."
            )


with action_col2:

    if st.button(
        "💡 SHOW SOLUTION",
        use_container_width=True
    ):

        st.session_state.board = [
            row[:] for row in st.session_state.solution
        ]

        st.session_state.game_finished = True
        st.session_state.end_time = time.time()
        st.session_state.game_id += 1

        st.rerun()


with action_col3:

    if st.button(
        "↩️ RESET BOARD",
        use_container_width=True
    ):

        st.session_state.board = [
            row[:] for row in st.session_state.puzzle
        ]

        st.session_state.start_time = time.time()
        st.session_state.end_time = time.time()
        st.session_state.game_finished = False
        st.session_state.game_id += 1

        st.rerun()


# =========================================================
# INSTRUCTIONS
# =========================================================

st.write("")
st.divider()

st.subheader("📖 How to Play")

instruction_col1, instruction_col2 = st.columns(2)

with instruction_col1:

    st.write(
        """
        **1.** Fill every empty cell with a number from 1 to 9.

        **2.** A number cannot repeat in the same row.

        **3.** A number cannot repeat in the same column.
        """
    )

with instruction_col2:

    st.write(
        """
        **4.** A number cannot repeat inside a 3×3 box.

        **5.** Complete the board and click **Check Answer**.

        **6.** Use Reset if you want to start the same puzzle again.
        """
    )