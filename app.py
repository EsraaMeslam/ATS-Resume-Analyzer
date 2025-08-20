import os
import re
import io
import json
from datetime import datetime
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import PyPDF2 as pdf
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF

#  Streamlit Page Config
st.set_page_config(page_title="ATS Analyzer")
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    st.error("Missing GEMINI_API_KEY in your .env")
genai.configure(api_key=GEMINI_API_KEY)

MODEL_NAME = "gemini-1.5-flash"
MODEL = genai.GenerativeModel(MODEL_NAME)

# Utility Functions
REPLACEMENTS = {
    "–": "-", "—": "-", "­": "-",
    "’": "'", "‘": "'", "“": '"', "”": '"',
    "•": "-", "…": "...", "\u00a0": " ",
}

def clean_text(text: str) -> str:
    for old, new in REPLACEMENTS.items():
        text = text.replace(old, new)
    return text.encode("utf-8", "ignore").decode("utf-8")

def read_pdf_bytes(uploaded_file) -> str:
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for i in range(len(reader.pages)):
        page = reader.pages[i]
        text += page.extract_text() or ""
        text += "\n"
    return text.strip()

def safe_int(x, default=None):
    try:
        return int(x)
    except Exception:
        return default

def list_to_csv(values):
    return ", ".join(map(str, values)) if values else ""

# Gemini API Call
JSON_PROMPT = """You are an ATS evaluator. Analyze the provided resume against the job description.
Return ONLY valid JSON (no markdown, no comments, no additional text).
JSON schema:
{
  "ats_score": 0-100,
  "match_percentage": 0-100,
  "text_readability": 0-100,
  "wrong_keywords_percent": 0-100,
  "wrong_skills_percent": 0-100,
  "missing_keywords": ["keyword", "..."],
  "strengths": ["..."],
  "weaknesses": ["..."],
  "profile_summary": "string",
  "recommendations": ["..."]
}
Resume:
---
{resume_text}
---
Job Description:
---
{job_description}
---"""

def analyze_with_gemini(resume_text: str, job_description: str) -> dict:
    clean_resume = clean_text(resume_text[:120000])
    clean_jd = clean_text(job_description[:20000])
    prompt = JSON_PROMPT.replace("{resume_text}", clean_resume).replace("{job_description}", clean_jd)

    try:
        resp = MODEL.generate_content(prompt)
        raw = resp.text or "{}"
        raw = raw.strip()
        if raw.startswith("```json"):
            raw = raw[7:]
        elif raw.startswith("```"):
            raw = raw[3:]
        if raw.endswith("```"):
            raw = raw[:-3]
        raw = raw.strip()
        json_match = re.search(r'\{[\s\S]*\}', raw)
        if json_match:
            raw = json_match.group(0)
        data = json.loads(raw)
    except Exception as e:
        st.error(f"Error analyzing resume: {str(e)}")
        return {}

    return data

# PDF Report Class
class ReportPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
        self.set_margins(15, 15, 15)

    def header(self):
        if self.page_no() > 1:
            self.set_font('Arial', 'I', 10)
            self.cell(0, 8, "Smart ATS Analyzer Report", 0, 0, 'R')
            self.ln(12)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def cover_page(self, title, candidate_name, job_title):
        self.add_page()
        self.set_font('Arial', 'B', 24)
        self.cell(0, 20, clean_text(title), 0, 1, 'C')
        self.ln(10)
        self.set_font('Arial', '', 14)
        self.cell(0, 10, f"Candidate: {clean_text(candidate_name)}", 0, 1, 'C')
        self.cell(0, 10, f"Target Role: {clean_text(job_title or 'N/A')}", 0, 1, 'C')
        self.cell(0, 10, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}", 0, 1, 'C')
        self.ln(10)
        self.set_font('Arial', 'I', 11)
        self.multi_cell(0, 8,
                        "This report summarizes ATS alignment, keyword coverage, and recommendations to improve resume-job fit.",
                        0, 'C')

    def section_title(self, text):
        self.set_font('Arial', 'B', 14)
        self.ln(6)
        self.cell(0, 10, clean_text(text), 0, 1)

    def safe_multi_cell(self, text, lh=7):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, lh, clean_text(text))
        self.ln(2)

    def bullet_list(self, items, max_width=180):
        if not items:
            return
        self.set_font('Arial', '', 12)
        for it in items:
            clean_item = clean_text(str(it))
            self.multi_cell(max_width, 6, "- " + clean_item)
            self.ln(1)

def build_pdf_report(candidate_name: str, job_title: str, results: list) -> bytes:
    pdf_buf = io.BytesIO()
    pdf = ReportPDF()
    pdf.set_title("Smart ATS Analyzer Report")
    pdf.set_author(clean_text(candidate_name or "Candidate"))
    pdf.cover_page("ATS Evaluation Report", candidate_name or "Unknown", job_title or "")

    for R in results:
        pdf.add_page()
        pdf.section_title(f"Resume: {R.get('filename', '(uploaded)')}")
        pdf.safe_multi_cell(
            f"ATS Score: {R.get('ats_score', 0)}%\nMatch Percentage: {R.get('match_percentage', 0)}%\nText Readability: {R.get('text_readability', 0)}%")
        pdf.bullet_list(R.get("missing_keywords", []))
        pdf.bullet_list(R.get("strengths", []))
        pdf.bullet_list(R.get("weaknesses", []))
        if R.get("profile_summary"):
            pdf.section_title("Profile Summary")
            pdf.safe_multi_cell(R.get("profile_summary"))
        pdf.bullet_list(R.get("recommendations", []))
    pdf.output(pdf_buf)
    return pdf_buf.getvalue()


# Streamlit Interface
st.markdown("<h1 style='text-align: center;'>ATS Resume Analyzer</h1>", unsafe_allow_html=True)
st.caption("""ATS Resume Analyzer is a smart tool to optimize resumes for Applicant 
Tracking Systems (ATS). Analyze resumes against job descriptions, get missing keyword insights, 
strengths & weaknesses, and export detailed PDF/Excel reports. Also includes an interactive AI chat to answer 
questions about your resumes!.""")

tab1, tab2 = st.tabs(["Resume Analysis", "Interactive Chat"])

with tab1:
    left, right = st.columns([2, 1])
    with left:
        job_description = st.text_area("Job Description", placeholder="Paste the job description here...", height=180)
    with right:
        candidate_name = st.text_input("Candidate Name ", value="Esraa Meslam")
        target_role = st.text_input("Target Role/Job Title ")

    uploaded_files = st.file_uploader("Upload one or more resumes (PDF)", type=["pdf"], accept_multiple_files=True)

    opt_cols = st.columns(3)
    with opt_cols[0]:
        show_charts = st.checkbox("Show Charts", value=True)
    with opt_cols[1]:
        export_pdf = st.checkbox("Export PDF", value=True)
    with opt_cols[2]:
        export_excel = st.checkbox("Export Excel", value=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        analyze_btn = st.button("ANALYZE RESUME(S)", use_container_width=True)

    if analyze_btn:
        if not uploaded_files:
            st.warning("⚠️ Please upload at least one PDF resume.")
            st.stop()

        results = []
        table_rows = []

        progress = st.progress(0)
        step = 0

        for uf in uploaded_files:
            step += 1
            progress.progress(step / max(1, len(uploaded_files)))

            resume_text = read_pdf_bytes(uf)
            data = analyze_with_gemini(resume_text, job_description)

            table_rows.append({
                "File": uf.name,
                "ATS Score": data.get("ats_score", 0),
                "Match %": data.get("match_percentage", 0),
                "Readability %": data.get("text_readability", 0),
                "Wrong Keywords %": data.get("wrong_keywords_percent", 0),
                "Wrong Skills %": data.get("wrong_skills_percent", 0),
            })

            results.append({
                "filename": uf.name,
                "ats_score": data.get("ats_score", 0),
                "match_percentage": data.get("match_percentage", 0),
                "text_readability": data.get("text_readability", 0),
                "missing_keywords": data.get("missing_keywords", []),
                "strengths": data.get("strengths", []),
                "weaknesses": data.get("weaknesses", []),
                "profile_summary": data.get("profile_summary", ""),
                "recommendations": data.get("recommendations", []),
            })

        st.session_state.results = results
        st.session_state.job_description = job_description
        st.success("Analysis completed")

        df = pd.DataFrame(table_rows)
        st.subheader("Summary Table")
        st.dataframe(df, use_container_width=True)

        best_idx = df["ATS Score"].astype(int).idxmax() if not df.empty else None
        if best_idx is not None:
            best_file = df.loc[best_idx, "File"]
            best_score = df.loc[best_idx, "ATS Score"]
            st.info(f"🏆 Best Resume: **{best_file}** with ATS Score **{best_score}%**")

        # =========================
        # Display Missing Keywords, Strengths, Weaknesses, Recommendations
        # =========================
        st.subheader("Detailed Resume Insights")
        for r in results:
            st.markdown(f"### {r.get('filename', '(uploaded)')}")
            st.write(f"- **ATS Score:** {r.get('ats_score', 0)}%")
            st.write(f"- **Match Percentage:** {r.get('match_percentage', 0)}%")
            st.write(f"- **Text Readability:** {r.get('text_readability', 0)}%")
            st.write(f"- **Missing Keywords:** {', '.join(r.get('missing_keywords', [])) or 'None'}")
            st.write(f"- **Strengths:** {', '.join(r.get('strengths', [])) or 'None'}")
            st.write(f"- **Weaknesses:** {', '.join(r.get('weaknesses', [])) or 'None'}")
            st.write(f"- **Recommendations:** {', '.join(r.get('recommendations', [])) or 'None'}")
            if r.get("profile_summary"):
                st.write(f"- **Profile Summary:** {r.get('profile_summary')}")
            st.markdown("---")

        if show_charts and not df.empty:
            chart_cols = st.columns(2)
            with chart_cols[0]:
                st.markdown("**Overall ATS Scores**")
                fig1, ax1 = plt.subplots()
                ax1.bar(df["File"], df["ATS Score"])
                ax1.set_ylabel("ATS Score")
                ax1.set_xticklabels(df["File"], rotation=30, ha='right')
                st.pyplot(fig1)
            with chart_cols[1]:
                st.markdown("**Match % by Resume**")
                fig2, ax2 = plt.subplots()
                ax2.bar(df["File"], df["Match %"])
                ax2.set_ylabel("Match %")
                ax2.set_xticklabels(df["File"], rotation=30, ha='right')
                st.pyplot(fig2)

        if export_pdf:
            pdf_bytes = build_pdf_report(candidate_name, target_role, results)
            st.download_button(
                label="⬇️ Download PDF Report",
                data=pdf_bytes,
                file_name=f"ATS_Report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                mime="application/pdf"
            )

        if export_excel:
            out = io.BytesIO()
            with pd.ExcelWriter(out, engine="openpyxl") as writer:
                df.to_excel(writer, sheet_name="Summary", index=False)
                for r in results:
                    details = {
                        "Metric": ["ATS Score", "Match %", "Readability %", "Missing Keywords", "Strengths",
                                   "Weaknesses", "Recommendations"],
                        "Value": [
                            r["ats_score"],
                            r["match_percentage"],
                            r["text_readability"],
                            list_to_csv(r["missing_keywords"]),
                            list_to_csv(r["strengths"]),
                            list_to_csv(r["weaknesses"]),
                            list_to_csv(r["recommendations"]),
                        ],
                    }
                    pd.DataFrame(details).to_excel(writer, sheet_name=(r["filename"][:28] or "Resume"), index=False)
            st.download_button(
                label="⬇️ Download Excel (Summary + Details)",
                data=out.getvalue(),
                file_name=f"ATS_Results_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )

with tab2:
    st.header("Interactive Chat with ATS Analyzer")
    st.markdown("Ask any question about the analysis results or request a comparison between resumes")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask about resume analysis or request a comparison..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.rerun()

    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        last_user_message = st.session_state.messages[-1]["content"]
        response = "No resumes have been analyzed yet. Please analyze resumes first in the Analysis tab."

        if "results" in st.session_state and "job_description" in st.session_state:
            # Compare resumes if requested
            if any(word in last_user_message.lower() for word in ["compare", "rank", "best"]):
                sorted_results = sorted(st.session_state.results, key=lambda x: x['ats_score'], reverse=True)
                if sorted_results:
                    response = "Comparison of resumes based on ATS analysis:\n\n"
                    for i, res in enumerate(sorted_results):
                        response += f"{i+1}. {res.get('filename','Unknown')} - Score: {res['ats_score']}%\n"
                        response += f"   Strengths: {', '.join(res['strengths'][:2])}\n"
                        response += f"   Areas for improvement: {', '.join(res['weaknesses'][:2])}\n\n"
                    response += f"Best resume: {sorted_results[0].get('filename', 'Unknown')} with {sorted_results[0]['ats_score']}% score"
            else:
                # General response using Gemini API
                context = f"Job Description:\n{st.session_state.job_description[:5000]}\nAnalysis Results:\n"
                for i, res in enumerate(st.session_state.results):
                    context += f"Resume {i+1}: {res.get('filename', 'Unknown')}\n"
                    context += f"- ATS Score: {res['ats_score']}%\n"
                    context += f"- Match %: {res['match_percentage']}%\n"
                    context += f"- Missing Keywords: {', '.join(res['missing_keywords'][:5])}\n"
                    context += f"- Strengths: {', '.join(res['strengths'][:3])}\n"
                    context += f"- Weaknesses: {', '.join(res['weaknesses'][:3])}\n"
                chat_prompt = f"""You are a smart assistant for resume analysis.\n{context}\nQuestion: {last_user_message}\nBriefly and clearly on the required question.
                Be as brief as possible
If the question is general or greeting, respond normally and ask if help with CV is needed.
If out of context, say: I'm sorry, I'm here to help you answer anything related to your CV."""
                try:
                    resp = MODEL.generate_content(chat_prompt)
                    response = resp.text
                except Exception as e:
                    response = f"Error generating response: {str(e)}"

        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

# Footer

st.markdown("""
<hr/>
<div style="text-align:center; font-size: 13px; opacity: 0.8; color: white;">
  Developed by <b style="color:red;">Esraa Meslam</b><br>
  <a href="https://www.linkedin.com/in/esraa-meslam-873a20241" target="_blank" style="text-decoration: none; color: white;">
    <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="18" height="18" style="vertical-align: middle; margin-right: 5px;">
    LinkedIn
  </a> | 
  <a href="https://github.com/EsraaMeslam" target="_blank" style="text-decoration: none; color: white;">
    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/github/github-original.svg" width="18" height="18" style="vertical-align: middle; margin-right: 5px; filter: invert(1);">
    GitHub
  </a>
</div>
""", unsafe_allow_html=True)
