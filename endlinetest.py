import streamlit as st
import gspread # You'll need to pip install gspread

# --- Connect to Google Sheets ---
try:
    gc = gspread.service_account_from_dict(st.secrets["gcp_service_account"])
    # Replace "YourSheetName" with the actual name of your Google Sheet
    sh = gc.open("YourSheetName").sheet1 
    st.info("Successfully connected to Google Sheets.")
except Exception as e:
    st.error(f"⚠️ Google Sheets connection failed: {e}")
    st.stop()

# --- The Test Survey Form ---
with st.form("test_form_gsheets", clear_on_submit=True):
    # ... form fields are the same ...
    respondent_name = st.text_input("What is your name?")
    favorite_color = st.selectbox("What is your favorite color?", ["Red", "Green", "Blue", "Yellow"])
    feedback = st.text_area("Any additional feedback?")
    submitted = st.form_submit_button("Submit to Google Sheet")

# --- Submission Logic ---
if submitted:
    if not respondent_name:
        st.warning("Please enter your name.")
    else:
        with st.spinner("Submitting to Google Sheets..."):
            try:
                # Prepare the row as a list
                new_row = [respondent_name, favorite_color, feedback]
                sh.append_row(new_row)
                st.success("✅ Success! Your response has been saved to Google Sheets.")
            except Exception as e:
                st.error(f"An error occurred: {e}")
