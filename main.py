import streamlit as st
from datetime import  date
import calendar


def calculate_age(birth_date):
    today = date.today()
    years = today.year - birth_date.year
    months = today.month - birth_date.month
    days = today.day - birth_date.day

    if days < 0:
        months -= 1
        days += calendar.monthrange(today.year, (today.month - 1) or 12)[1]
    if months < 0:
        years -= 1
        months += 12

    return years, months, days


def calculate_next_birthday(birth_date):
    today = date.today()
    try:
        next_birthday = date(today.year, birth_date.month, birth_date.day)

    except ValueError:
        next_birthday = date(today.year, 3, 1)

    if next_birthday < today:
        try:
            next_birthday = date(today.year + 1, birth_date.month, birth_date.day)
        except ValueError:
            next_birthday = date(today.year + 1, 3, 1)

    return (next_birthday - today).days


def get_fun_facts(total_days):
    minutes_lived = total_days * 24 * 60
    hours_slept = total_days * 8  # Assuming 8 hours of sleep per day
    heartbeats = minutes_lived * 80  # Assuming 80 beats per minute
    breaths = minutes_lived * 12  # Assuming 12 breaths per minute
    steps = total_days * 4000  # Assuming average 4000 steps per day
    words_spoken = total_days * 7000  # Assuming average 7000 words per day

    return {
        "Total Minutes": f"{minutes_lived:,}",
        "Hours Slept": f"{hours_slept:,}",
        "Heart Beats": f"{heartbeats:,}",
        "Breaths Taken": f"{breaths:,}",
        "Steps Walked": f"{steps:,}",
        "Words Spoken": f"{words_spoken:,}"
    }


def get_life_milestones(total_days):
    milestones = {
        10000: "10,000 days milestone",
        15000: "15,000 days milestone",
        20000: "20,000 days milestone",
        25000: "25,000 days milestone",
        30000: "30,000 days milestone"
    }  # some milestones are created
    upcoming_milestone = None
    for days in sorted(milestones.keys()):
        if total_days < days:
            upcoming_milestone = (days, milestones[days], days - total_days)
            break
    return upcoming_milestone


def main():
    st.set_page_config(page_title="Age Calculator", page_icon="🎂", layout="wide")

    # Custom CSS
    st.markdown("""

        <style>
        .main { padding: 10rem;}
        .stButton>button { 
            width: 100%;
            font-weight: bold;
            border-radius: 12px;
            box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
        }
        .stat-card {
            padding: 1rem;
            border-radius: 0.5rem;
            background-color: pink;
            background: linear-gradient(135deg, #f06, #f79);
            margin: 0.5rem ;
            text-align: center;

        }

        .milestone-card {
            padding: 1rem;
            border-radius: 0.5rem;
            background-color: pink;
            background: linear-gradient(135deg, #f06, #f79);
            margin: 0.5rem ;
            text-align: center;
        }
        </style>
    """, unsafe_allow_html=True)

    # Header with emoji decoration

    # Tabs for different sections
    tab1, tab2 = st.tabs(["📅 Calculate Your Time Journey", "✨ Fun Facts & Milestones"])

    with tab1:
        st.markdown("###  Enter Your Birth Date")
        birth_date = st.date_input(
            "When did your journey begin?",
            min_value=date(1900, 1, 1),
            max_value=date.today(),
            help="Select your birth date"
        )

        if st.button("Reveal Your Time Journey! "):
            if birth_date > date.today():
                st.error("🚫 Time travel not invented yet! Please select a date in the past.")
                return

            # Basic age calculation
            years, months, days = calculate_age(birth_date)
            total_days = (date.today() - birth_date).days

            # Create visually appealing metrics
            st.markdown("### 🎯 Your Life in Numbers")
            metric_cols = st.columns(3)

            with metric_cols[0]:
                st.metric("Years", years)
            with metric_cols[1]:
                st.metric("Months", months)
            with metric_cols[2]:
                st.metric("Days", days)

            # Birthday Countdown with progress bar
            days_until_birthday = calculate_next_birthday(birth_date)
            st.markdown("### 🎂🎂Birthday Countdown🎂🎂 ")
            if days_until_birthday == 0:
                st.balloons()
                st.success("🎉 Happy Birthday! Today is your special day! 🎉")
            else:
                progress = (365 - days_until_birthday) / 365
                st.progress(progress)
                st.write(f"**{days_until_birthday}** days until your next birthday! 🎈")

            # Season and birth_day info
            st.markdown("### 🌍 Your Birth Time")
            time_cols = st.columns(2)
            with time_cols[0]:
                months_to_seasons = {
                    12: 'Winter ❄️', 1: 'Winter ❄️', 2: 'Winter ❄️',
                    3: 'Spring 🌸', 4: 'Spring 🌸', 5: 'Spring 🌸',
                    6: 'Summer ☀️', 7: 'Summer ☀️', 8: 'Summer ☀️',
                    9: 'Fall 🍁', 10: 'Fall 🍁', 11: 'Fall 🍁'
                }
                birth_season = months_to_seasons[birth_date.month]
                st.info(f"You were born in {birth_season}")

            with time_cols[1]:
                day_of_week = birth_date.strftime("%A")
                st.info(f"Born on a **{day_of_week}** (Day {birth_date.timetuple().tm_yday} of the year)")

    with tab2:
        if 'total_days' in locals():
            # Fun Statistics with emojis
            st.markdown("### 📊 Life Statistics")
            facts = get_fun_facts(total_days)

            # Create 3x2 grid for statistics
            for i in range(0, len(facts), 2):
                cols = st.columns(2)
                for j in range(2):
                    if i + j < len(facts):
                        fact_name = list(facts.keys())[i + j]
                        fact_value = facts[fact_name]
                        with cols[j]:
                            st.markdown(f"""
                                <div class="stat-card">
                                    <h3>{fact_name}</h3>
                                    <h2>{fact_value}</h2>
                                </div>
                            """, unsafe_allow_html=True)

            # Milestone tracker with progress bar
            milestone = get_life_milestones(total_days)
            if milestone:
                st.markdown("### 🏆 Next Life Milestone")
                days, name, days_left = milestone
                progress = (days - days_left) / days

                st.markdown(f"""
                    <div class="milestone-card">
                        <h3>{name}</h3>
                        <p>Coming up in {days_left:,} days!</p>
                    </div>
                """, unsafe_allow_html=True)
                st.progress(progress)

                # Add encouragement based on progress
                if progress < 0.3:
                    st.write("🌱 Just starting your journey to this milestone!")
                elif progress < 0.7:
                    st.write("⭐ You're making great progress!")
                else:
                    st.write("🎯 Almost there!")
        else:
            st.info("👆 Calculate your age first to see fun facts and milestones!")


if __name__ == "__main__":
    main()