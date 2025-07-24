import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --- Initialize session state ---
if "habits" not in st.session_state:
    st.session_state.habits = []
if "progress" not in st.session_state:
    st.session_state.progress = pd.DataFrame(columns=["Habit", "Date", "Status"])

# --- App Title ---
st.title("MicroHabit Coach – Behavioral Nudging App")

# --- Sidebar for navigation ---
menu = st.sidebar.radio("Navigate", ["Home", "Add Habit", "Track Progress", "Visualize"])

# --- Home Page ---
if menu == "Home":
    st.subheader("Welcome!")
    st.write("This app helps you adopt small, sustainable habits for conditions like Diabetes, PCOS, or Hypothyroidism.")

# --- Add Habit ---
elif menu == "Add Habit":
    st.subheader("Add a New Habit")
    habit_name = st.text_input("Enter Habit (e.g., Walk 10 mins after lunch):")
    if st.button("Save Habit"):
        st.session_state.habits.append(habit_name)
        st.success(f"Habit '{habit_name}' added!")

# --- Track Progress ---
elif menu == "Track Progress":
    st.subheader("Mark Today's Habit Progress")
    if st.session_state.habits:
        for habit in st.session_state.habits:
            status = st.checkbox(f"Completed: {habit}")
            if status:
                new_entry = {"Habit": habit, "Date": pd.Timestamp.now().date(), "Status": "Done"}
                st.session_state.progress = pd.concat(
                    [st.session_state.progress, pd.DataFrame([new_entry])], ignore_index=True
                )
        st.success("Progress updated!")
    else:
        st.warning("No habits added yet.")

# --- Visualize ---
elif menu == "Visualize":
    st.subheader("Your Weekly Progress")
    if not st.session_state.progress.empty:
        counts = st.session_state.progress.groupby("Habit")["Status"].count()
        fig, ax = plt.subplots()
        counts.plot(kind="bar", ax=ax)
        st.pyplot(fig)
    else:
        st.info("No data yet to visualize.")
