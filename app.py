from google import genai
import streamlit as st
from PyPDF2 import PdfReader
import re

client = genai.Client(api_key=st.secrets["API_KEY"])

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🚀",
    layout="wide"
)

with st.sidebar:
    st.title("🚀 Features")

    st.write("✅ ATS Score")
    st.write("✅ Resume Analysis")
    st.write("✅ Missing Skills Detection")
    st.write("✅ Interview Questions")
    st.write("✅ Resume Summary")
    st.write("✅ Download Report")

st.title("🚀 AI Resume Analyzer")

st.caption(
    "Analyze resumes using Gemini AI and improve ATS performance"
)

uploaded_file = st.file_uploader(
    "📄 Upload Resume PDF",
    type=["pdf"]
)

if uploaded_file is not None:

    pdf_reader = PdfReader(uploaded_file)

    resume_text = ""

    for page in pdf_reader.pages:
        text = page.extract_text()

        if text:
            resume_text += text

    st.success("✅ Resume uploaded successfully!")

    with st.expander("📌 View Extracted Resume Text"):
        st.text_area(
            "Resume Content",
            resume_text,
            height=300
        )

    job_role = st.text_input(
        "🎯 Enter Target Job Role",
        placeholder="Example: AI Engineer, Data Analyst..."
    )

    if st.button(
        "🚀 Analyze Resume",
        use_container_width=True
    ):

        with st.spinner("Analyzing Resume with Gemini AI..."):

            prompt = f"""
            Analyze this resume for the role: {job_role}

            Give response in this format:

            1. ATS Score out of 100
            2. Skills Found
            3. Missing Skills
            4. Resume Improvements
            5. Strengths
            6. Weak Areas
            7. Duplicate Skills or Certifications
            8. Best Matching Job Roles
            9. Resume Summary
            10. Interview Preparation Tips

            Resume:
            {resume_text}
            """

            response = client.models.generate_content(
                model="gemini-3.5-flash",
                contents=prompt
            )

            analysis = response.text

            ats_match = re.search(
                r'(\d{1,3})\s*/\s*100',
                analysis
            )

            if ats_match:

                score = int(ats_match.group(1))

                st.subheader("📊 ATS Score")

                if score < 50:
                    st.error(f"{score}/100")

                elif score < 75:
                    st.warning(f"{score}/100")

                else:
                    st.success(f"{score}/100")

                st.progress(min(score, 100))

            st.divider()

            st.subheader("🤖 AI Resume Analysis")

            st.write(analysis)

            st.download_button(
                label="📥 Download Analysis Report",
                data=analysis,
                file_name="resume_analysis.txt",
                mime="text/plain",
                use_container_width=True
            )

            interview_prompt = f"""
            Based on this resume and role {job_role},

            Generate:

            1. HR Interview Questions
            2. Technical Interview Questions
            3. Project-Based Questions

            Resume:
            {resume_text}
            """

            interview_response = client.models.generate_content(
                model="gemini-3.5-flash",
                contents=interview_prompt
            )

            st.divider()

            st.subheader("🎤 AI Interview Questions")

            st.write(interview_response.text)

st.markdown("---")

st.caption(
    "Built with Streamlit + Gemini AI 🚀"
)