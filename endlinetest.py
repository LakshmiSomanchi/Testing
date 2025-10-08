# app.py
import streamlit as st
import pandas as pd
from datetime import datetime, date, time
import os
import uuid
from pyairtable import Table # Import the pyairtable library

# --- Streamlit Page Configuration ---
st.set_page_config(page_title="BMC Self Assessment", layout="wide")

# --- Step 1: Cache the large data structure for efficiency ---
@st.cache_data
def get_questions():
    """Loads the entire survey questions dictionary from the PDF."""
    # This is the large dictionary of questions you provided earlier.
    # I've truncated it here for brevity, but you should use your full dictionary.
    return {
        "Identification": {
            "Identification": {
                "Name of the Dairy Partner": ["Parag", "Sunfresh Lactalis", "Govind", "Schreiber"],
                "Name of the respondent": None,
                "Respondent Email ID": None,
                "Respondent Contact Number": None,
                "Designation": ["Route Incharge", "Facilitator", "Manager", "Supervisor", "Entrepreneur", "Other"],
                "Specify if other - Designation": None,
                "Department": ["Procurement", "Dairy Extension", "Quality", "Other"],
                "Specify if other - Department": None,
                "Milk chilling and collection center": ["BMC", "MCC"],
                "BMC/ MCC Name": None,
                "BMC/ MCC code": None,
                "Route Number": None,
                "Route Details": None,
                "Location (Village, Taluka, District)": None,
                "Date of response": None,
                "Consent to fill the form": ["Yes", "No"],
                "Signature of the respondent": None,
                "Reviewed and confirmed by Route Incharge": ["Yes", "No"],
                "Signature of Route In charge": None,
                "Reviewed and confirmed by Ksheersagar SPOC": ["Yes", "No"],
                "Signature of SPOC": None,
            }
        },
        "1. Animal Care": {
            "1.1 Cattle Health": {
                "1.1.1 Preventive Care": {
                    "1.1.1.1 Vaccination, deworming, tick control and preventive checks ups": [
                        "a. 100% of dairy farmers are aware and have sufficient knowledge of recommended vaccinations (6), deworming, and tick control schedules",
                        "b. 100% of dairy farmers can access vaccines (3) and as per vaccination services provided by government and/ or private, deworming and tick medicines, and preventive checkups timely as per recommended schedule",
                        "c. Timely doorstep services ensured for all cattle for vaccinations (3), deworming, tick and preventive checkups as per recommended schedule at an affordable price",
                        "d. Timely affordable doorstep services ensured for all cattle for vaccinations (6), deworming, and preventive checkups as per recommended schedule.",
                        "e. 100% cattle vaccinated (8 recommended vaccines, stock as provided by government from time to time), dewormed, checked periodically based on prescribed schedule customized to different physiological stages of the cattle cycle",
                        "f. None of the above (In case your response is none of the above, please mention what best suits your milk shed)",
                        "g. Not aware (Dairy farmers in your milk shed are completely not aware of any of the above)"
                    ],
                    "1.1.1.2 Documentation and maintenance of records": [
                        "a. Written records of all cattle and their treatments are maintained and available for further investigation by 40% of farmers",
                        "b. Written records of all cattle and their treatments are maintained and available for further investigation by 60% of farmers",
                        "c. Written records of all cattle and their treatments are maintained and available for further investigation by 80% of farmers",
                        "d. Written records of all cattle and their treatments are maintained and available for further investigation by 100% of dairy farmers",
                        "e. Digital records of all cattle and their treatments are maintained and available for further investigation for all dairy farmers",
                        "f. None of the above (In case your response is none of the above, please mention what best suits your milk shed)",
                        "g. Not aware (Dairy farmers in your milk shed are completely not aware of any of the above)"
                    ],
                    "1.1.1.3 Sick animal segregation": [
                        "a. Segregation of healthy cattle from the sick is practiced by 60% of dairy farmers",
                        "b. Segregation of healthy cattle from the sick is practiced by 80% of dairy farmers",
                        "c. Segregation of healthy cattle from the sick is practiced by 100% farmers and a designated space available for segregation",
                        "d. Segregation of 100% of sick animals is practiced",
                        "e. Segregation of healthy cattle from the 100% sick animals is practiced by 100% dairy farmers",
                        "f. None of the above (In case your response is none of the above, please mention what best suits your milk shed)",
                        "g. Not aware (Dairy farmers in your milk shed are completely not aware of any of the above)"
                    ],
                    "1.1.1.4 New cattle introduction and testing": [
                        "a. 100% of dairy farmers are aware and have preliminary knowledge of the criteria for selection of healthy animal/s before introducing them into the herd",
                        "b. Health status of animals sourced is known to 100% of dairy farmers",
                        "c. Health status of animals sourced is known to 100% of dairy farmers and their introduction is controlled into the herd through quarantine. Testing of these animals at an affordable price is ensured.",
                        "d. Health status of animals sourced is known to 100% of dairy farmers through testing that is available at an affordable price and 100% of cattle introduced are quarantined.",
                        "e. Health status of 100% animals sourced is known through in house testing infrastructure and their introduction into the herd is 100% controlled through quarantine",
                        "f. None of the above (In case your response is none of the above, please mention what best suits your milk shed)",
                        "g. Not aware (Dairy farmers in your milk shed are completely not aware of any of the above)"
                    ],
                    "1.1.1.5 Feeding of colostrum": [
                        "a. Colostrum fed to newborn calves by 100% dairy farmers",
                        "b. Colostrum fed to newborn calves for 3 days by 100% of dairy farmers",
                        "c. Colostrum fed at least 2 LPD of fresh colostrum over 3 days to newborn calves by 100% of dairy farmers",
                        "d. Colostrum fed to newborn calves (2 L in first 2 hours and 1-2 LPD for next 2-3 days) by all dairy farmers",
                        "e. Colostrum fed to newborn calves (2 L in first 2 hours and 2 LPD of fresh colostrum in a day over 3-4 times for next 5-7 days)",
                        "f. None of the above (In case your response is none of the above, please mention what best suits your milk shed)",
                        "g. Not aware (Dairy farmers in your milk shed are completely not aware of any of the above)"
                    ],
                    "1.1.1.6 Use of herbal remedies": [
                        "a. 100 % of dairy farmers are aware of Herbal remedies for most common preventive diseases",
                        "b. Herbal remedies are adopted and practiced by 100% of dairy farmers",
                        "c. Herbal raw materials or ready to use herbal medicines are made easily available and herbal remedies are practiced by 100% dairy farmers",
                        "d. Herbal remedies are adopted and practiced on 100% cattle with highest level of self-efficacy and diseases are prevented.",
                        "e. Herbal gardens are promoted widely and herbal remedies and ready to use medicines are easily accessible to 100% of dairy farmers who are practicing herbal remedies on regular",
                        "f. None of the above (In case your response is none of the above, please mention what best suits your milk shed)",
                        "g. Not aware (Dairy farmers in your milk shed are completely not aware of any of the above)"
                    ],
                    "1.1.1.7 Hazard and contamination": [
                        "a. 100% of dairy farmers are aware and have knowledge of potential hazards caused by bio contaminants",
                        "b. 100% of dairy farmers monitor farms from potential hazards and secure boundaries from adjoining neighbors",
                        "c. 100% of dairy farmers are aware and have knowledge of inter-herd and intra- herd practices to reduce bio contamination",
                        "d. Biosecurity is enhanced and bio contamination reduced through the adoption of inter-herd and intra-herd practice by 80% dairy farmers",
                        "e. Biosecurity is enhanced and bio contamination reduced through the adoption of inter-herd and intra-herd practice by 100% dairy farmers"
                    ],
                    "1.1.1.8 Post dipping": [
                        "a. 100% of dairy farmers are aware of post dipping with prescribed chemicals to prevent mastitis",
                        "b. 100% of dairy farmers are adopting post dipping with prescribed dosages of chemicals to prevent mastitis",
                        "c. 100% of dairy farmers are having access to chemicals for post dipping and are adopting on 100% of their milch cattle",
                        "d. 100% of dairy farmers have access to chemicals for post dipping at an affordable price at their doorstep and practice post dipping on 100% of their cattle immediate post milking",
                        "e. Post dipping done mandatorily as practice on 100% of cattle in herd immediately post milking using globally approved prescribed chemicals",
                        "f. None of the above (In case your response is none of the above, please mention what best suits your milk shed)",
                        "g. Not aware (Dairy farmers in your milk shed are completely not aware of any of the above)"
                    ]
                },
                # ... (rest of "1.1.2 Disease Diagnosis", "1.1.3 Disease Treatment" etc.) ...
            }
        },
        # ... (rest of "2. Dairy Extension Services", "3. Procurement and Milk Quality", etc.) ...
        # NOTE: For deployment, ensure your full QUESTIONS dictionary is here.
        # This is a placeholder to keep the example concise.
    }

QUESTIONS = get_questions()

# Session State Initialization
if "step" not in st.session_state:
    st.session_state["step"] = 1
if "responses" not in st.session_state:
    st.session_state["responses"] = {}
if "section_keys" not in st.session_state:
    st.session_state["section_keys"] = list(QUESTIONS.keys())

responses = st.session_state["responses"]
section_keys = st.session_state["section_keys"]

# --- Airtable Connection Setup ---
# Your Airtable Personal Access Token and Base ID should be stored in Streamlit secrets.
# See the .streamlit/secrets.toml example below.
try:
    API_KEY = st.secrets["airtable"]["api_key"]
    BASE_ID = st.secrets["airtable"]["base_id"]
    
    # Define your Airtable table names
    # Ensure these match the table names you set up in Airtable!
    SUBMISSIONS_TABLE_NAME = "Submissions_Test" # Main table for each completed survey
    RESPONSES_TABLE_NAME = "Responses_Test"     # Table for individual question answers
    
    submissions_table = Table(API_KEY, BASE_ID, SUBMISSIONS_TABLE_NAME)
    responses_table = Table(API_KEY, BASE_ID, RESPONSES_TABLE_NAME)
    st.sidebar.success("✅ Connected to Airtable.")
except (FileNotFoundError, KeyError) as e:
    st.sidebar.error(f"⚠️ Airtable connection failed. Ensure .streamlit/secrets.toml is configured correctly: {e}")
    st.stop() # Stop the app if Airtable connection fails

# --- Helper Functions ---
def safe_index(options, value, default_index=0):
    """Safely gets the index of a value in a list, returning a default if not found."""
    try:
        if value is None or (isinstance(value, list) and not value):
            return default_index
        options_str = [str(o) for o in options]
        if not isinstance(value, list) and str(value) in options_str:
            return options_str.index(str(value))
        if isinstance(value, str) and value in options_str:
            return options_str.index(value)
        return default_index
    except (ValueError, TypeError):
        return default_index

def render_questions_recursively(questions_data, parent_key=""):
    """Recursively renders questions, saving values directly to the 'responses' dictionary."""
    for key, value in questions_data.items():
        current_key_full = f"{parent_key}-{key}" if parent_key else key

        # Skip rendering 'Remarks' fields here, as they are handled explicitly below
        if "Remarks" in key:
            continue

        if isinstance(value, dict):
            st.markdown(f"**{key}**")
            render_questions_recursively(value, parent_key=current_key_full)
        else:
            question_key = current_key_full
            
            if isinstance(value, list):
                if "multiple options" in key.lower(): # Check if it's a multiselect type question
                    responses[question_key] = st.multiselect(
                        key,
                        value,
                        default=responses.get(question_key, [])
                    )
                else: # Default to radio buttons for single-select lists
                    default_index = safe_index(value, responses.get(question_key))
                    if not (0 <= default_index < len(value)):
                        default_index = 0
                    responses[question_key] = st.radio(
                        key,
                        value,
                        index=default_index,
                        key=f"radio_{question_key}" # Unique key for Streamlit elements
                    )
            elif value is None: # For text input fields
                if "Date of response" in key:
                    responses[question_key] = st.date_input(
                        key,
                        value=responses.get(question_key, date.today()),
                        key=f"date_{question_key}"
                    )
                else:
                    responses[question_key] = st.text_input(
                        key,
                        value=responses.get(question_key, ""),
                        key=f"text_{question_key}"
                    )
            
            # Handle remarks for this question
            remarks_key = f"{question_key} - Remarks"
            current_remarks = responses.get(remarks_key, "")
            responses[remarks_key] = st.text_area(
                f"Remarks for **{key}** (Optional)",
                value=current_remarks,
                key=f"remarks_{question_key}"
            )
            st.markdown("---")


def show_questions_for_block(block_name, questions_data, is_identification=False):
    st.subheader(block_name)
    if is_identification:
        identification_content = next(iter(questions_data.values()), {})
        st.markdown(f"**{list(questions_data.keys())[0]}**")
        for question_key, options in identification_content.items():
            if "Specify if other" in question_key:
                continue

            if isinstance(options, list):
                # Handle Designation and Department 'Other' logic
                if question_key in ["Designation", "Department"]:
                    default_index = safe_index(options, responses.get(question_key))
                    if not (0 <= default_index < len(options)):
                        default_index = 0
                    responses[question_key] = st.radio(
                        f"**{question_key}:**",
                        options,
                        index=default_index,
                        key=f"id_radio_{question_key}"
                    )
                    if responses.get(question_key) == "Other":
                        other_key = None
                        if question_key == "Designation":
                            other_key = "Specify if other - Designation"
                        elif question_key == "Department":
                            other_key = "Specify if other - Department"
                        if other_key:
                            responses[other_key] = st.text_input(
                                f"Please specify your **{question_key}**",
                                value=responses.get(other_key, ""),
                                key=f"id_text_{other_key}"
                            )
                else: # Regular radio for other lists in Identification
                    default_index = safe_index(options, responses.get(question_key))
                    if not (0 <= default_index < len(options)):
                        default_index = 0
                    responses[question_key] = st.radio(
                        f"**{question_key}:**",
                        options,
                        index=default_index,
                        key=f"id_radio_{question_key}"
                    )
            elif options is None:
                if "Date of response" in question_key:
                    responses[question_key] = st.date_input(
                        f"**{question_key}:**",
                        value=responses.get(question_key, date.today()),
                        key=f"id_date_{question_key}"
                    )
                else:
                    responses[question_key] = st.text_input(
                        f"**{question_key}:**",
                        value=responses.get(question_key, ""),
                        key=f"id_text_{question_key}"
                    )
            st.markdown("---")

    else:
        render_questions_recursively(questions_data, parent_key=block_name)

# --- Application Flow Control ---
if st.session_state["step"] == 1:
    st.title("BMC Self Assessment Survey")
    st.header("Informed Consent")
    st.markdown("""
        Namaste. We are conducting this self-assessment survey for BMCs/CCs/VLCs. Your participation is **voluntary**.
        The information will help us design a comprehensive dairy processing curriculum to sustainably improve the quality and quantity of milk produced.
        The data is confidential and will not be shared outside the research team.
    """)
    if st.button("Proceed to Assessment"):
        st.session_state["step"] = 2
        st.rerun()

elif st.session_state["step"] in range(2, len(section_keys) + 2):
    current_index = st.session_state["step"] - 2
    current_step_key = section_keys[current_index]

    st.title("BMC Self Assessment Survey")
    st.markdown(f"**Step {st.session_state['step'] - 1} of {len(section_keys)}:** {current_step_key}")

    questions_for_step = QUESTIONS.get(current_step_key, {})
    
    is_identification_step = (current_step_key == "Identification")
    
    show_questions_for_block(current_step_key, questions_for_step, is_identification=is_identification_step)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.session_state["step"] > 2:
            if st.button("Back"):
                st.session_state["step"] -= 1
                st.rerun()
        elif st.session_state["step"] == 2:
            if st.button("Back to Consent"):
                st.session_state["step"] = 1
                st.rerun()
    with col2:
        is_last_survey_step = st.session_state["step"] == len(section_keys) + 1
        next_button_text = "Review & Submit" if is_last_survey_step else "Save and Next"
        if st.button(next_button_text):
            st.session_state["step"] += 1
            st.rerun()

elif st.session_state["step"] == len(section_keys) + 2:
    st.title("Finalize and Submit")
    
    with st.form("final_submit_form"):
        st.subheader("Review your responses: 👇")
        final_responses = st.session_state["responses"].copy()
        display_data = {}
        for k, v in final_responses.items():
            if v is not None:
                if isinstance(v, (datetime, date, time)):
                    display_data[k] = str(v)
                elif isinstance(v, list):
                    display_data[k] = "; ".join(map(str, v))
                elif isinstance(v, str) and v.strip() == "":
                    continue
                else:
                    display_data[k] = v
        
        if display_data:
            df = pd.DataFrame(list(display_data.items()), columns=["Question/Field", "Response"])
            # Filter out "Specify if other" remarks if 'Other' wasn't selected
            df = df[~df['Question/Field'].str.contains("Specify if other - Designation") |
                    ((df['Question/Field'].str.contains("Specify if other - Designation")) & (final_responses.get('Designation') == 'Other'))]
            df = df[~df['Question/Field'].str.contains("Specify if other - Department") |
                    ((df['Question/Field'].str.contains("Specify if other - Department")) & (final_responses.get('Department') == 'Other'))]
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.warning("No responses recorded yet.")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("Back to Form"):
                st.session_state["step"] = len(section_keys) + 1
                st.rerun()
        with col2:
            if st.form_submit_button("✅ Submit & Save Final to Airtable"):
                with st.spinner("Saving your responses to Airtable... This may take a moment."):
                    try:
                        # 1. Prepare main submission record for the 'Submissions' table
                        # Extract key identification fields for the main submission record
                        main_submission_data = {
                            "Respondent Name": final_responses.get("Identification-Identification-Name of the respondent", ""),
                            "Respondent Email ID": final_responses.get("Identification-Identification-Respondent Email ID", ""),
                            "BMC/ MCC Name": final_responses.get("Identification-Identification-BMC/ MCC Name", ""),
                            #"Date of response": str(final_responses.get("Identification-Identification-Date of response", date.today()))
                            # Add any other top-level identification fields you want in the main Submissions table
                        }
                        created_submission = submissions_table.create(main_submission_data)
                        submission_airtable_id = created_submission['id'] # Get the Airtable ID of the new submission

                        # 2. Prepare individual question answers for the 'Responses' table
                        responses_to_batch_create = []
                        for key, value in final_responses.items():
                            # Only save if there's a valid response
                            if value is not None and not (isinstance(value, str) and not value.strip()) and not (isinstance(value, list) and not value):
                                # Format list values (e.g., from multiselect) into a string
                                answer_str = "; ".join(map(str, value)) if isinstance(value, list) else str(value)

                                # Create a record for each question/answer pair
                                record = {
                                    "Submission": [submission_airtable_id], # Link to the main submission
                                    "Question": key, # The full question key as stored in your `responses` dict
                                    "Answer": answer_str
                                }
                                responses_to_batch_create.append(record)
                        
                        # 3. Batch create all individual responses in the 'Responses' table
                        if responses_to_batch_create:
                            # Airtable has a batch size limit (e.g., 10 records per batch).
                            # For a large survey, you might need to chunk this.
                            # pyairtable's batch_create handles this automatically if list is large.
                            responses_table.batch_create(responses_to_batch_create)

                        st.session_state["step"] = len(section_keys) + 3
                        st.rerun()

                    except Exception as e:
                        st.error(f"Failed to submit responses to Airtable. Please try again. Error: {e}")

elif st.session_state["step"] == len(section_keys) + 3:
    st.title("Thank you! 🙏")
    st.success("Your responses have been successfully submitted to Airtable.")
    st.balloons()
    if st.button("Start New Survey"):
        # Clear state for a new survey
        keys_to_clear = ["step", "responses", "section_keys"]
        for key in keys_to_clear:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()
