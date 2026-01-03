import streamlit as st
from services.parsing.resume import resume_analyzer
from services.reporting.match_analyzer import match_analyzer
from services.parsing.resume import load_resume
import pandas as pd
import json, os, uuid

file_PATH = 'applicant_data.json'
# st.session_state.result_df = None
# st.session_state.resume_file = None
display_uploader: bool = True
display_result = False
start = False

def append_applicant_data(new_data):
    # Load the existing data
    if os.path.exists(file_PATH):
        with open(file_PATH, "r") as f:
            try:
                existing_data = json.load(f)
            except json.JSONDecodeError:
                existing_data = []
    else:
        existing_data = []

    # Ensure it is a list
    if not isinstance(existing_data, list):
        existing_data = [existing_data]

    # Append new record
    existing_data.append(new_data)

    # write back to file
    with open(file_PATH, "w") as f:
        json.dump(existing_data, f, indent=4)


def clear():
    if "result_df" in st.session_state:
        del st.session_state["result_df"]
    if "resume_file" in st.session_state:
        del st.session_state.resume_file
 
    

def get_score(a,b,c): 
    return 0.5 * a + 0.3 * b + 0.2 * c


#############################################################################################################


def display():
      
    st.subheader("List of Applicants")
    st.dataframe(
        st.session_state.result_df,
        use_container_width=True,
    )

    st.session_state.result_df.sort_values(by=["score"], ascending=False)
    st.subheader("🔍 View Candidate Details")
    for idx, row in st.session_state.result_df.iterrows():
        col1, col2, col3, col4 = st.columns([2,1,1,1])

        with col1:
            st.write(f"👤 **{row['full_name']}**")

        with col2:
            st.write(f"Score: **{row['score']}**")

        with col3:
            st.write(f"Overall_match(%): **{row['overall_match(%)']}**")

        with col4:
            if st.button("View Details", key=f"view_{idx}"):
                st.session_state.selected_candidate = idx


def upload_resume():
        if st.session_state.job_data and st.session_state.resume_file:
            try:
                with st.spinner("🔍 Analyzing your application.."):
                    resume_text = load_resume(st.session_state.resume_file)
                    resume_data = resume_analyzer(resume_text)
                    parsed_data = resume_data.model_dump()

                    match_data = match_analyzer(st.session_state.job_data, resume_text)
                    match_data = match_data.model_dump()

                    append_applicant_data(match_data)

                    education_match_percentage = int(match_data['education_match_percentage'])
                    experience_match_percentage = int(match_data['experience_match_percentage'])
                    project_relevance_percentage = int(match_data['project_relevance_percentage'])

                    if "result_df" not in st.session_state: 
                        st.session_state.result_df = pd.DataFrame(
                            columns=[
                                "full_name",
                                "matching_skills",
                                "missing_skills",
                                "overall_match(%)",
                                "score"
                            ]
                        )

                    try:
                        new_row = {
                            "full_name": parsed_data['full_name'],
                            "matching_skills": len(match_data.get('matching_skills',[])),
                            "missing_skills": len(match_data.get("missing_skills", [])),
                            "overall_match(%)": match_data.get('overall_match_percentage'),
                            "score": get_score(experience_match_percentage, project_relevance_percentage, education_match_percentage)
                            }

                        st.session_state.result_df = pd.concat(
                            [st.session_state.result_df, pd.DataFrame([new_row])],
                            ignore_index=True
                            )
                    
                        st.subheader("List of Applicants")
                        st.dataframe(
                            st.session_state.result_df,
                            use_container_width=True,
                        )
                        # st.session_state.result_df.sort_values(by=["score"], ascending=False)
                        # st.subheader("🔍 View Candidate Details")
                        # for idx, row in st.session_state.result_df.iterrows():
                        #     col1, col2, col3, col4 = st.columns([1,1,1,1])

                        #     with col1:
                        #         st.write(f"👤 **{row['full_name']}**")

                        #     with col2:
                        #         st.write(f"Score: **{row['score']}**")

                        #     with col3:
                        #         st.write(f"Overall_match(%): **{row['overall_match(%)']}**")

                        #     with col4:
                        #         if st.button("View Details", key=f"view_{idx}"):
                        #             st.session_state.selected_candidate = idx
                        #             # with st.popover("View Details", width="stretch"):
                        #             #     st.write("Details")
                        #             if "selected_candidate" in st.session_state:
                        #                 idx = st.session_state.selected_candidate

                        #                 candidate_summary = st.session_state.result_df.iloc[idx]

                        #                 st.subheader("📄 Candidate Details")

                        #                 st.json({
                        #                     "Full Name": candidate_summary["fullname"],
                        #                     "Matching Skills": candidate_summary["matching_skills"],
                        #                     "Missing Skills": candidate_summary["missing_skills"],
                        #                     "Score": candidate_summary["score"]
                        #                 })
                    except NameError:
                        st.write("Could not write data to dataframe")
                    except Exception:
                        st.write("Something went wrong while writing to dataframe")
            except ValueError:
                st.write("Value mismatched")
            except Exception:
                st.write("Something went wrong while parsing resume of analyzing your application")
        else:
            st.write("Upload a resume")
    

    

if "job_data" in st.session_state and display_uploader:

    try:
        st.subheader("Your Resume")
        st.session_state.resume_file = st.file_uploader("Upload your resume", type=['pdf','docx']) 
    except Exception:
        st.markdown("Something went wrong while uploading resume file\n Upload PDF or DOCX only")
    
    if "resume_file" in st.session_state:
        start = True
        try:
            # upload_resume()
            st.button("Get results", on_click=upload_resume, type="secondary")
            display_result = True
            start = False
            
        except Exception:
            st.write("Error analyzing resume")

    if "result_df" in st.session_state and display_result:
        st.button("Clear results", on_click=clear, type="primary")
            
            
else: 
    st.markdown("No Job description available")





           