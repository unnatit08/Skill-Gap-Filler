import streamlit as st
import re
from datetime import datetime, timedelta

# Set page configuration
st.set_page_config(
    page_title="Skill Gap Filler",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for light pink theme
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #fbcfe8 0%, #f9a8d4 100%);
    }
    .stApp {
        background: linear-gradient(135deg, #fbcfe8 0%, #f9a8d4 100%);
    }
    .css-1d391kg {
        background-color: white;
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
    }
    .skill-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 4px solid #ec4899;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    .day-card {
        background-color: #fce7f3;
        padding: 1.8rem;
        border-radius: 15px;
        border-left: 4px solid #f472b6;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    .feature-card {
        background-color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        margin: 1rem;
    }
    .header {
        background: linear-gradient(135deg, #ec4899, #db2777);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2rem;
    }
    .resource-badge {
        background-color: #34d399;
        color: white;
        padding: 0.8rem 1.2rem;
        border-radius: 10px;
        margin-top: 1rem;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# Skill resources database
SKILL_RESOURCES = {
    'JavaScript': {
        'icon': '⚡',
        'resources': [
            'MDN JavaScript Guide - https://developer.mozilla.org/en-US/docs/Web/JavaScript',
            'freeCodeCamp JavaScript Curriculum - https://www.freecodecamp.org/learn/javascript-algorithms-and-data-structures/',
            'JavaScript.info Tutorial - https://javascript.info/',
            'Codecademy JavaScript Course - https://www.codecademy.com/learn/introduction-to-javascript'
        ]
    },
    'React': {
        'icon': '⚛️',
        'resources': [
            'React Official Tutorial - https://reactjs.org/tutorial/tutorial.html',
            'Scrimba React Course - https://scrimba.com/learn/learnreact',
            'FreeCodeCamp React Projects - https://www.freecodecamp.org/news/react-projects-for-beginners/',
            'React Documentation - https://react.dev/learn'
        ]
    },
    'Python': {
        'icon': '🐍',
        'resources': [
            'Python.org Tutorial - https://docs.python.org/3/tutorial/',
            'Real Python Articles - https://realpython.com/',
            'Codecademy Python Course - https://www.codecademy.com/learn/learn-python-3',
            'Automate the Boring Stuff with Python - https://automatetheboringstuff.com/'
        ]
    },
    'Data Analysis': {
        'icon': '📊',
        'resources': [
            'Kaggle Learn Pandas - https://www.kaggle.com/learn/pandas',
            'DataCamp Free Courses - https://www.datacamp.com/courses/free-introduction-to-data-science',
            'Google Data Analytics Certificate - https://grow.google/certificates/data-analytics/',
            'Towards Data Science Articles - https://towardsdatascience.com/'
        ]
    },
    'SQL': {
        'icon': '💾',
        'resources': [
            'SQLBolt Tutorial - https://sqlbolt.com/',
            'Mode Analytics SQL Tutorial - https://mode.com/sql-tutorial/',
            'W3Schools SQL Course - https://www.w3schools.com/sql/',
            'Khan Academy SQL - https://www.khanacademy.org/computing/computer-programming/sql'
        ]
    },
    'AWS': {
        'icon': '☁️',
        'resources': [
            'AWS Free Tier - https://aws.amazon.com/free/',
            'AWS Tutorials Point - https://www.tutorialspoint.com/aws/index.htm',
            'FreeCodeCamp AWS Course - https://www.freecodecamp.org/news/aws-certified-cloud-practitioner-certification-study-guide/',
            'AWS Whitepapers - https://aws.amazon.com/whitepapers/'
        ]
    },
    'Git': {
        'icon': '📝',
        'resources': [
            'Git Official Documentation - https://git-scm.com/doc',
            'Atlassian Git Tutorial - https://www.atlassian.com/git/tutorials',
            'GitHub Learning Lab - https://lab.github.com/',
            'freeCodeCamp Git Course - https://www.freecodecamp.org/news/learn-the-basics-of-git-in-under-10-minutes/'
        ]
    },
    'Docker': {
        'icon': '🐳',
        'resources': [
            'Docker Getting Started - https://docs.docker.com/get-started/',
            'Docker Curriculum - https://docker-curriculum.com/',
            'FreeCodeCamp Docker Course - https://www.freecodecamp.org/news/the-docker-handbook/',
            'Docker Official Tutorials - https://docs.docker.com/get-started/resources/'
        ]
    },
    'Node.js': {
        'icon': '🟢',
        'resources': [
            'Node.js Official Docs - https://nodejs.org/en/docs/',
            'The Net Ninja Node.js Course - https://www.youtube.com/playlist?list=PL4cUxeGkcC9gcy9lrvMJ75z9maRw4byYp',
            'FreeCodeCamp Backend Development - https://www.freecodecamp.org/news/backend-web-development-with-node-js/',
            'NodeSchool Workshops - https://nodeschool.io/'
        ]
    },
    'TypeScript': {
        'icon': '📘',
        'resources': [
            'TypeScript Handbook - https://www.typescriptlang.org/docs/',
            'TypeScript Deep Dive - https://basarat.gitbook.io/typescript/',
            'FreeCodeCamp TypeScript - https://www.freecodecamp.org/news/learn-typescript-beginners-guide/',
            'Academind TypeScript Course - https://www.youtube.com/watch?v=BwuLxPH8IDs'
        ]
    },
    'UI/UX Design': {
        'icon': '🎨',
        'resources': [
            'Google UX Design Certificate - https://grow.google/certificates/ux-design/',
            'Figma Community Tutorials - https://www.figma.com/community',
            'Interaction Design Foundation - https://www.interaction-design.org/',
            'Nielsen Norman Group Articles - https://www.nngroup.com/articles/'
        ]
    },
    'Agile Methodology': {
        'icon': '🔄',
        'resources': [
            'Atlassian Agile Guide - https://www.atlassian.com/agile',
            'Scrum.org Resources - https://www.scrum.org/resources',
            'Agile Alliance - https://www.agilealliance.org/agile101/',
            'Mountain Goat Software - https://www.mountaingoatsoftware.com/agile'
        ]
    }
}

COMMON_SKILLS = [
    'JavaScript', 'React', 'Python', 'Data Analysis', 'SQL', 
    'AWS', 'Git', 'Docker', 'Node.js', 'TypeScript', 
    'UI/UX Design', 'Agile Methodology'
]

def get_daily_focus(skill, day):
    focus_map = {
        'JavaScript': [
            'JavaScript fundamentals and syntax basics',
            'DOM manipulation and event handling',
            'ES6+ features and modern JavaScript patterns',
            'Async programming and API integration'
        ],
        'React': [
            'React components and JSX fundamentals',
            'State management with hooks and context',
            'Component lifecycle and useEffect patterns',
            'Routing and advanced React patterns'
        ],
        'Python': [
            'Python basics and data structures overview',
            'Functions and object-oriented programming',
            'Popular libraries and framework basics',
            'Data processing and automation scripting'
        ],
        'Data Analysis': [
            'Data cleaning and preparation techniques',
            'Statistical analysis fundamental concepts',
            'Data visualization best practices',
            'Advanced analytics and insights generation'
        ]
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

    # For demo purposes, return a subset of skills
    return found_skills[:4]

def main():
    # Header
    st.markdown("""
    <div class="header">
        <h1 style="font-size: 3rem; margin: 0;">🎓 Skill Gap Filler</h1>
        <p style="font-size: 1.2rem; opacity: 0.9;">Turn job requirements into actionable learning plans</p>
    </div>
    """, unsafe_allow_html=True)

    # Features grid
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>🔍 Skill Analysis</h3>
            <p>Identify missing skills from any job description</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>📅 14-Day Plan</h3>
            <p>Structured daily learning schedule</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h3>📚 Free Resources</h3>
            <p>Curated free learning materials</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="feature-card">
            <h3>🚀 Fast Results</h3>
            <p>Quick skill development roadmap</p>
        </div>
        """, unsafe_allow_html=True)

    # Input section
    st.markdown("### 📋 Paste Job Description")
    
    sample_job = """We are looking for a Full Stack Developer with experience in:
- JavaScript and React.js
- Node.js and Express
- Python for backend services
- SQL databases and data analysis
- AWS cloud infrastructure
- Git version control
- Agile development methodologies

Requirements:
- 3+ years professional experience
- Strong problem-solving skills
- Experience with CI/CD pipelines
- Knowledge of Docker containers
- TypeScript experience preferred"""
    
    job_description = st.text_area(
        "Paste the job description here...",
        value=sample_job,
        height=200,
        help="We'll analyze it and create a customized 14-day crash course plan with free resources to help you bridge the skill gap."
    )

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
                        # Display missing skills
                        st.markdown("### 📊 Missing Skills Analysis")
                        for skill in missing_skills:
                            skill_info = SKILL_RESOURCES.get(skill, {'icon': '📝'})
                            st.markdown(f"""
                            <div class="skill-card">
                                <h3>{skill_info['icon']} {skill}</h3>
                                <p>This skill appears to be required but might need development.</p>
                            </div>
                            """, unsafe_allow_html=True)

                        # Generate 14-day plan
                        st.markdown("### 🗓️ 14-Day Crash Course Plan")
                        
                        for day in range(1, 15):
                            skill_index = (day - 1) % len(missing_skills)
                            current_skill = missing_skills[skill_index]
                            skill_info = SKILL_RESOURCES.get(current_skill, {'resources': ['General learning resources']})
                            
                            day_focus = get_daily_focus(current_skill, day)
                            
                            st.markdown(f"""
                            <div class="day-card">
                                <h3>📅 Day {day}: {current_skill}</h3>
                                <p>{day_focus}</p>
                                <div class="resource-badge">
                                    📚 Recommended: {skill_info['resources'][0]}
                                </div>
                            </div>
                            """, unsafe_allow_html=True)

                        # Show all resources
                        st.markdown("### 📖 All Recommended Resources")
                        for skill in missing_skills:
                            skill_info = SKILL_RESOURCES.get(skill, {'resources': ['General learning resources']})
                            with st.expander(f"📚 Resources for {skill}"):
                                for resource in skill_info['resources']:
                                    st.markdown(f"- {resource}")
    
    with col2:
        if st.button("🗑️ Clear Input", use_container_width=True):
            st.rerun()

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #831843;">
        <p>❤️ Skill Gap Filler - Bridging the gap between your current skills and dream jobs</p>
        <p>© 2024 | All learning resources are freely available online</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
