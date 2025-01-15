import streamlit as st
import lorem
from datetime import datetime


def calculate_wpm(text, time_taken_seconds):
    if not text or time_taken_seconds == 0:
        return 0
    words = text.split()
    num_words = len(words)
    minutes = time_taken_seconds / 60
    wpm = num_words / minutes if minutes > 0 else 0
    return round(wpm)


def calculate_accuracy(original, typed):
    if not typed:
        return 0
    original_words = original.split()
    typed_words = typed.split()
    correct_words = sum(1 for o, t in zip(original_words, typed_words) if o == t)
    total_words = len(typed_words)
    accuracy = (correct_words / total_words) * 100 if total_words > 0 else 0
    return round(accuracy, 2)


def main():
    st.title("Typing Speed Test")
    st.balloons()

    # Initialize session state variables
    if 'start_time' not in st.session_state:
        st.session_state.start_time = None
    if 'test_active' not in st.session_state:
        st.session_state.test_active = False
    if 'text_to_type' not in st.session_state:
        st.session_state.text_to_type = lorem.paragraph()
    if 'submitted' not in st.session_state:
        st.session_state.submitted = False
    if 'end_time' not in st.session_state:
        st.session_state.end_time = None
    if 'user_input' not in st.session_state:
        st.session_state.user_input = ""

    # Display instructions and sample text
    st.write("Type the following text as accurately as you can:")
    st.markdown(
        f'<div style="background-color: black; padding: 20px; border-radius: 5px;">{st.session_state.text_to_type}</div>',
        unsafe_allow_html=True)

    # Start button
    if not st.session_state.test_active:
        if st.button("Start Test"):
            st.balloons()
            st.session_state.test_active = True
            st.session_state.start_time = datetime.now()
            st.session_state.submitted = False
            st.session_state.user_input = ""
            st.rerun()

    # Text input area
    if st.session_state.test_active and not st.session_state.submitted:
        user_input = st.text_area(
            "Start typing here:",
            height=150,
            key="typing_input"
        )
        st.session_state.user_input = user_input

        # Submit button
        if st.button("Submit Test"):
            st.write("hi")
            st.session_state.submitted = True
            st.session_state.end_time = datetime.now()
            st.rerun()

    # Show results only after submission
    if st.session_state.submitted and st.session_state.test_active:
        time_elapsed = (st.session_state.end_time - st.session_state.start_time).total_seconds()

        final_wpm = calculate_wpm(st.session_state.user_input, time_elapsed)
        final_accuracy = calculate_accuracy(st.session_state.text_to_type, st.session_state.user_input)
        words_typed = len(st.session_state.user_input.split())

        # Display final metrics with better styling
        st.markdown("### Your Results:")
        st.markdown("<br>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Words Per Minute", final_wpm)
        with col2:
            st.metric("Accuracy", f"{final_accuracy}%")
        with col3:
            st.metric("Words Typed", words_typed)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f" Time taken: {round(time_elapsed, 1)} seconds")

        # Reset button
        if st.button("Try Again"):
            st.session_state.test_active = False
            st.session_state.start_time = None
            st.session_state.submitted = False
            st.session_state.text_to_type = lorem.paragraph()
            st.session_state.user_input = ""
            st.rerun()


if __name__ == "__main__":
    main()