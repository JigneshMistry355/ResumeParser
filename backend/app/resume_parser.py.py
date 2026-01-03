import time, json
from services.scraping.naukri import setup_driver, scroll_page, get_job_cards, extract_job_data
from services.scraping.cleaning import job_analyzer
import streamlit as st
from services.parsing.resume import load_resume
from services.parsing.resume import resume_analyzer
from services.reporting.match_analyzer import match_analyzer
import pandas as pd


url = "https://www.naukri.com/job-listings-junior-python-ai-developer-exalogico-systems-and-services-bengaluru-0-to-2-years-081225000887?src=jobsearchDesk&sid=17651861844415317&xp=1&px=1"

# url = 'https://www.naukri.com/job-listings-business-analyst-sustainability-fossil-group-bengaluru-0-to-1-years-161225017126?src=drecomm_apply&sid=17660709158616932&xp=8&px=1'

# url = 'https://www.naukri.com/job-listings-associate-machine-learning-engineer-kuku-fm-bengaluru-0-to-1-years-181225501185?src=jobsearchDesk&sid=17661266191981500&xp=2&px=1'




def main():
    st.set_page_config(page_title="Job Application Assistant - Resume Parser", layout='wide')
    st.title("Job Application Assistant - Resume Parser")

    # Initializing is must
    # if "job_data" in st.session_state:
        # del st.session_state['job_data']


    # trying to stop web scraping twice after resume upload / not working
    if "job_data" not in st.session_state:
        with st.spinner("🔍 Fetching job data..."):
            driver = setup_driver()
            try:
                driver.get(url)
                time.sleep(3)
                scroll_page(driver)
                cards = get_job_cards(driver)
                data = extract_job_data(cards)
                if "job_data" not in st.session_state:
                    st.session_state.job_data = data
            finally:
                driver.quit()


    # A way to access session state data
    
    data = st.session_state.job_data


    col1, col2 = st.columns(2)
    # Job description
    with col1:
        st.subheader("Job description")
        # setup_gemini_api()     
        job_data = job_analyzer(data) 
        with st.container(height=400):
            st.write(job_data)
        # st.write(st.session_state.job_data)
    
    # resume uploader
    with col2:
        st.subheader("Your Resume")
        resume_file = st.file_uploader("Upload your resume", type=['pdf','docx'])
        
    if job_data and resume_file:
        with st.spinner("🔍 Analyzing your application.."):
            resume_text = load_resume(resume_file)
            print("################ resume text")
            print(resume_text)
            resume_data = resume_analyzer(resume_text)
            parsed_data = resume_data.model_dump()
            st.subheader("Parsed Resume data")
            st.write(parsed_data)

            match_data = match_analyzer(data, resume_text)
            match_data = match_data.model_dump()
            print(match_data['recommendations_for_improvement'])
            st.subheader("Matched data")
            st.write(match_data)

            st.header("Analysis result")

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Overall match", f"{match_data.get('overall_match_percentage')}%")
            with col2:
                st.metric(
                    "Skills Match 🧠",
                    f"{len(match_data.get('matching_skills', []))} skills",
                )
            with col3:
                st.metric(
                    "Skills to Develop 📈",
                    f"{len(match_data.get('missing_skills', []))} skills"
                )


            tab1, tab2, tab3 = st.tabs([
                "Skills Analysis 📊",
                "Experience Match 🗂️",
                "Recommendations 💡",
                # "Cover Letter 💌",
                # "Updated Resume 📝"
            ])

            with tab1:
                
                st.subheader("Matching Skills")
                match_flex = st.container(horizontal=True, horizontal_alignment="left")
                for skill in match_data['matching_skills']:
                    match_flex.badge(f"{skill}")
                print(match_data['matching_skills'])

                st.subheader("Missing skills")
                missing_flex = st.container(horizontal=True, horizontal_alignment="left")
                for skill in match_data['missing_skills']:
                    missing_flex.badge(f"{skill}", color="yellow")

                # st.write(data)

            with tab2:
                st.subheader("Experience Analysis")
                st.info(match_data['experience_match_analysis'])
                st.subheader("Education Analysis")
                st.info(match_data['education_match_analysis'])

            with tab3:
                st.subheader("Recommendation for improvement")
                for rec in match_data['recommendations_for_improvement']:
                    st.info(f"{rec['section']}")
                    st.success(f"{rec['recommendation']}")
                    st.success(f"{rec['guidance']}")
                #  st.info(match_data['recommendations_for_improvement'])
                st.subheader("Skill gap report")
                for skill in match_data['skills_gap_analysis']:
                    st.warning(f"{skill['technical_skills']}")
                    # st.warning(f"{skill['soft_skills']}")

            education_match_percentage = int(match_data['education_match_percentage'])
            experience_match_percentage = int(match_data['experience_match_percentage'])
            project_relevance_percentage = int(match_data['project_relevance_percentage'])

            def get_score(): 
                return 0.5 * experience_match_percentage + 0.3 * project_relevance_percentage + 0.2 * education_match_percentage
            
            table_data = pd.DataFrame( {
                "fullname": parsed_data['full_name'],
                "matching_skills": len(match_data.get('matching_skills', [])),
                "missing_skills": len(match_data.get('missing_skills', [])),
                "score": get_score()
            }, index=[0])

            st.table(table_data, border="horizontal")
                
                



if __name__ == '__main__':
    main()
