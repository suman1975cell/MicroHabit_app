import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import random

# ------------------- Initialize Session State -------------------
if "habits" not in st.session_state:
    st.session_state.habits = []
if "progress" not in st.session_state:
    st.session_state.progress = pd.DataFrame(columns=["Habit", "Date", "Status"])

# ------------------- App Title -------------------
st.set_page_config(page_title="MicroHabit Coach", page_icon="🌱", layout="centered")
st.title("🌱 MicroHabit Coach – Behavioral Nudging App")

# ------------------- Sidebar Navigation -------------------
menu = st.sidebar.radio(
    "Navigate",
    ["Home", "Add Habit", "Track Progress", "Visualize Progress", "Suggestions"]
)# --- Sidebar Footer ---
st.sidebar.markdown("---")
st.sidebar.caption("**Built by Dr. Suman Kotwal**")

# ------------------- Home -------------------
if menu == "Home":
    st.subheader("Welcome!")
    st.write(
        """
        **MicroHabit Coach** helps you build healthy micro-habits for conditions like:
        - Diabetes
        - PCOS
        - Hypothyroidism

        Add your habits, track them daily, and stay motivated with nudges!
        """
    )

# ------------------- Add Habit -------------------
elif menu == "Add Habit":
    st.subheader("Add a New Habit")

    habit_name = st.text_input("Enter Habit (e.g., Walk 10 mins after lunch):")
    if st.button("Save Habit"):
        if habit_name:
            st.session_state.habits.append(habit_name)
            st.success(f"Habit '{habit_name}' added!")
        else:
            st.warning("Please enter a habit name.")

    # Show current habits
    if st.session_state.habits:
        st.write("### Current Habits:")
        for h in st.session_state.habits:
            st.write(f"- {h}")

# ------------------- Track Progress -------------------
elif menu == "Track Progress":
    st.subheader("Mark Today's Habit Progress")

    if st.session_state.habits:
        for habit in st.session_state.habits:
            status = st.checkbox(f"Completed: {habit}")
            if status:
                new_entry = {
                    "Habit": habit,
                    "Date": pd.Timestamp.now().date(),
                    "Status": "Done"
                }
                st.session_state.progress = pd.concat(
                    [st.session_state.progress, pd.DataFrame([new_entry])],
                    ignore_index=True
                )
        if st.button("Save Progress"):
            st.success("Progress updated!")

            # Behavioral nudge
            nudges = [
                "Great job! Small steps = big changes.",
                "Consistency beats perfection – keep going!",
                "You're building a healthier future!"
            ]
            st.info(random.choice(nudges))
    else:
        st.warning("No habits added yet. Go to 'Add Habit' first.")

# ------------------- Visualize Progress -------------------
elif menu == "Visualize Progress":
    st.subheader("Your Weekly Progress")

    if not st.session_state.progress.empty:
        counts = st.session_state.progress.groupby("Habit")["Status"].count()

        fig, ax = plt.subplots()
        counts.plot(kind="bar", ax=ax, color="green")
        ax.set_ylabel("Completions")
        ax.set_title("Habit Completion Count")
        st.pyplot(fig)

        st.write("Raw Data:")
        st.dataframe(st.session_state.progress)
    else:
        st.info("No data yet to visualize.")

# ------------------- Suggestions -------------------
elif menu == "Suggestions":
    st.subheader("Condition-Specific Habit Suggestions")

    condition = st.selectbox("Choose Condition", ["Diabetes", "PCOS", "Hypothyroidism"])

    suggestions = {
        "Diabetes": [
            "Check fasting glucose daily",
            "Take 10-min walk after meals",
            "Opt for low-carb dinner"
        ],
        "PCOS": [
            "Eat protein-rich breakfast",
            "Track menstrual cycle",
            "Strength training 3x/week"
        ],
        "Hypothyroidism": [
            "Take levothyroxine on empty stomach",
            "Check TSH every 6 weeks",
            "30-min morning walk"
        ]
    }

    if st.button("Show Suggestions"):
        st.write("### Suggested Micro-Habits:")
        for habit in suggestions[condition]:
            st.write(f"- {habit}")
