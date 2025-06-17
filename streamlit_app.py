import streamlit as st
import pandas as pd
import openai
import io

# Load API key from Streamlit secrets
client = openai.OpenAI(api_key=st.secrets["openai"]["api_key"])

# Function to process each row using OpenAI API
def process_with_openai(prompt_question, detail_text):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt_question},
            {"role": "user", "content": detail_text}
        ],
        max_tokens=100
    )
    return response.choices[0].message.content.strip()

# Streamlit UI
st.title("🧠 Report Summarizer")
# st.header("🧠 Intelligence/Incident Report Summarizer")  # Slightly smaller

st.markdown("""
### 📌 Instructions:
Please make sure your Excel file includes the following columns **with these exact names**:
- 🕒 `Reporting Timestamp` — for the date and time of the report
- 📍 `Location` — for the location of the event
- 📝 `Details` — for the full description you want summarized

You can rename your columns in Excel before uploading.
""")


uploaded_file = st.file_uploader("📄 Upload your Excel file", type=["xlsx"])

# if uploaded_file:
#     try:
#         df = pd.read_excel(uploaded_file, engine="openpyxl")
#         required_columns = ["Details", "Reporting Timestamp", "Location"]

#         if all(column in df.columns for column in required_columns):
#             df = df[required_columns]

#             st.info("⏳ Processing with OpenAI...")
#             prompt_question = "Summarize the following report in one sentence without mentioning any officers names"
#             df["OpenAI Response"] = df["Details"].apply(
#                 lambda detail: process_with_openai(prompt_question, detail)
#             )

#             # Prepare output
#             output_df = df[["Reporting Timestamp", "Location", "OpenAI Response"]]
#             output = io.BytesIO()
#             output_df.to_excel(output, index=False)
#             output.seek(0)

#             st.success("✅ Processing complete! Download your summarized report below.")
#             st.download_button(
#                 label="📥 Download Processed Report",
#                 data=output,
#                 file_name="Processed_Report.xlsx",
#                 mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
#             )
#         else:
#             st.error("❌ The uploaded file must contain the columns: 'Details', 'Reporting Timestamp', and 'Location'.")
#     except Exception as e:
#         st.error(f"❌ Error: {str(e)}")

# Add a Run button
run_button = st.button("▶️ Run")

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file, engine="openpyxl")
        required_columns = ["Details", "Reporting Timestamp", "Location"]

        if all(column in df.columns for column in required_columns):
            df = df[required_columns]

            if run_button:
                st.info("⏳ Processing with OpenAI...")
                prompt_question = "Summarize the following report in one sentence without mentioning any officers names"
                df["OpenAI Response"] = df["Details"].apply(
                    lambda detail: process_with_openai(prompt_question, detail)
                )

                # Prepare output
                output_df = df[["Reporting Timestamp", "Location", "OpenAI Response"]]
                output = io.BytesIO()
                output_df.to_excel(output, index=False)
                output.seek(0)

                st.success("✅ Processing complete! Download your summarized report below.")
                st.download_button(
                    label="📥 Download Processed Report",
                    data=output,
                    file_name="Processed_Report.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else:
                st.info("✅ File uploaded. Click 'Run' to start processing.")
        else:
            st.error("❌ The uploaded file must contain the columns: 'Details', 'Reporting Timestamp', and 'Location'.")
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")


st.markdown("""
<hr style="margin-top: 50px;">
<div style='text-align: center; font-size: 0.9em; color: gray;'>
    Built by Shahroz  |   Amulet   ❤️
</div>
""", unsafe_allow_html=True)

