
import streamlit as st
import pandas as pd
import openai
import io

# Set your OpenAI API key

client = openai.OpenAI(api_key="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")

def process_with_openai(prompt_question, detail_text):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": prompt_question},
            {"role": "user", "content": detail_text}
        ],
        max_tokens=100
    )
    return response.choices[0].message.content.strip()


# Streamlit UI
st.title("🧠 Intelligence Report Summarizer")

uploaded_file = st.file_uploader("📄 Upload your 'Intelligence report' Excel file", type=["xlsx"])

if uploaded_file:
    if "Intelligence report" in uploaded_file.name:
        try:
            df = pd.read_excel(uploaded_file, engine="openpyxl")
            columns_to_keep = [
                "Event ID",
                "Reporting Timestamp",
                "Location Name",
                "Site Name",
                "Location intel linked to",
                "Details of intelligence (Detailed)"
            ]
            df = df[columns_to_keep]

            st.info("⏳ Processing with OpenAI...")
            prompt_question = "Summarize the following intelligence report in one sentence:"
            df["OpenAI Response"] = df["Details of intelligence (Detailed)"].apply(
                lambda detail: process_with_openai(prompt_question, detail)
            )

            # Save to in-memory buffer
            output = io.BytesIO()
            df.to_excel(output, index=False)
            output.seek(0)

            st.success("✅ Processing complete! Download your summarized report below.")
            st.download_button(
                label="📥 Download Processed Report",
                data=output,
                file_name="Processed_Intelligence_Report.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
    else:
        st.error("❌ Please upload a file named 'Intelligence report'.")
