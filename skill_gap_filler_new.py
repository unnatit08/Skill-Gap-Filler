import streamlit as st
import re
from datetime import datetime, timedelta

# Set page configuration
st.set_page_config(
    page_title="AI Job Skill Analyzer",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for white theme with dark text
st.markdown("""
<style>
    .main, .stApp {
        background: #ffffff;
    }
    .css-1d391kg, .skill-card, .feature-card {
        background-color: #ffffff;
        color: #111827 !important;
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 20px 40px rgba(0,0,0,0.05);
        margin: 1rem 0;
    }
    .skill-card, .day-card {
        border-left: 4px solid #2563eb;
    }
    .day-card {
        background-color: #f9fafb;
    }
    .header {
        background: linear-gradient(135deg, #2563eb, #1e40af);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2rem;
    }
    .resource-badge {
        background-color: #10b981;
        color: white;
        padding: 0.8rem 1.2rem;
        border-radius: 10px;
        margin-top: 1rem;
        display: inline-block;
    }
    .stTextArea textarea {
        color: #111827 !important;
        background-color: #ffffff !important;
    }
    .stButton button {
        color: white !important;
        background-color: #2563eb !important;
        border-radius: 10px;
    }
    .stButton button:hover {
        background-color: #1d4ed8 !important;
    }
    .st-expander, .st-expander .stMarkdown {
        color: #111827 !important;
    }
</style>
""", unsafe_allow_html=True)

# Skill resources and common skills
SKILL_RESOURCES = {
    # same as previous definition...
}
COMMON_SKILLS = [
    'JavaScript', 'React', 'Python', 'Data Analysis', 'SQL', 
    'AWS', 'Git', 'Docker', 'Node.js', 'TypeScript', 
    'UI/UX Design', 'Agile Methodology'
]

def get_daily_focus(skill, day):
    focus_map = {
        'JavaScript': [...], 'React': [...], 'Python': [...], 'Data Analysis': [...]
    }
    default_focus = [
        'Fundamental concepts and theoretical foundation',
        'Practical implementation and hands-on exercises',
        'Advanced techniques and optimization strategies',
        'Real-world applications and project integration'
    ]
    focuses = focus_map.get(skill, default_focus)
    return focuses[(day - 1) % len(focuses)]

def identify_missing_skills(job_description):
    text = job_description.lower()
    found_skills = []
    for skill in COMMON_SKILLS:
        if re.search(r'\b' + re.escape(skill.lower()) + r'\b', text):
            found_skills.append(skill)
    return found_skills[:4]

def main():
    # Header
    st.markdown("""
    <div class="header">
        <h1 style="font-size: 3rem; margin: 0;">🎓 AI Job Skill Analyzer</h1>
        <p style="font-size: 1.2rem; opacity: 0.9;">Turn job requirements into actionable learning plans</p>
    </div>
    """, unsafe_allow_html=True)

    # Input
    job_description = st.text_area("Paste Job Description Here...", value="", height=200)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🎯 Analyze & Create Plan", use_container_width=True):
            if not job_description.strip():
                st.error("Please paste a job description first.")
            else:
                with st.spinner("Analyzing job description and creating your personalized 14-day plan..."):
                    missing_skills = identify_missing_skills(job_description)
                    if not missing_skills:
                        st.warning("No common skills detected in the job description. Try a different job description.")
                    else:
                        st.markdown("### 📊 Missing Skills Analysis")
                        for skill in missing_skills:
                            skill_info = SKILL_RESOURCES.get(skill, {'icon': '📝'})
                            st.markdown(f"""
                            <div class='skill-card'>
                                <h3>{skill_info['icon']} {skill}</h3>
                                <p>This skill appears to be required but might need development.</p>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        st.markdown("### 🗓️ 14-Day Crash Course Plan")
                        for day in range(1, 15):
                            skill_index = (day - 1) % len(missing_skills)
                            current_skill = missing_skills[skill_index]
                            skill_info = SKILL_RESOURCES.get(current_skill, {'resources': ['General learning resources']})
                            day_focus = get_daily_focus(current_skill, day)
                            st.markdown(f"""
                            <div class='day-card'>
                                <h3>📅 Day {day}: {current_skill}</h3>
                                <p>{day_focus}</p>
                                <div class='resource-badge'>📚 Recommended: {skill_info['resources'][0]}</div>
                            </div>
                            """, unsafe_allow_html=True)

                        st.markdown("### 📖 All Recommended Resources")
                        for skill in missing_skills:
                            skill_info = SKILL_RESOURCES.get(skill, {'resources': ['General learning resources']})
                            with st.expander(f"📚 Resources for {skill}"):
                                for resource in skill_info['resources']:
                                    st.markdown(f"- {resource}")

    with col2:
        if st.button("🗑️ Clear Input", use_container_width=True):
            st.rerun()

    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #111827;'>
        <p>❤️ Skill Gap Filler - Bridging the gap between your current skills and dream jobs</p>
        <p>© 2024 | All learning resources are freely available online</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
