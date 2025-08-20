<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>ATS Resume Analyzer</title>
</head>
<body>
<h1>ATS Resume Analyzer 🚀</h1>

<!-- Badges -->
<p>
  <img src="https://img.shields.io/badge/Python-3.11-blue" alt="Python">
  <img src="https://img.shields.io/badge/Streamlit-1.24-orange" alt="Streamlit">
  <img src="https://img.shields.io/badge/License-MIT-green" alt="License">
</p>

<!-- Demo Image -->
<p align="center">
  <img src="https://i.imgur.com/your-demo-image.png" alt="ATS Analyzer Demo" width="600">
</p>

<p><strong>ATS Resume Analyzer</strong> is a smart tool to optimize resumes for Applicant Tracking Systems (ATS). Analyze resumes against job descriptions, get missing keyword insights, strengths & weaknesses, and export detailed PDF/Excel reports. Also includes an interactive AI chat to answer questions about your resumes!</p>

<h2>🌟 Features</h2>
<ul>
  <li><strong>ATS Scoring:</strong> Evaluate resume-job fit.</li>
  <li><strong>Keyword Analysis:</strong> Identify missing skills/keywords.</li>
  <li><strong>Strengths & Weaknesses:</strong> Practical improvement suggestions.</li>
  <li><strong>Reports:</strong> Download professional PDF & Excel reports.</li>
  <li><strong>Charts:</strong> Visualize ATS scores, match percentages, and readability.</li>
  <li><strong>Interactive Chat:</strong> Ask questions and get AI-powered resume insights.</li>
  <li><strong>Multi-Resume Comparison:</strong> Rank resumes by ATS score.</li>
</ul>

<h2>🛠️ Technology Stack</h2>
<ul>
  <li>Python 3.11+</li>
  <li>Streamlit</li>
  <li>PyPDF2 & FPDF for PDF handling</li>
  <li>Pandas & Matplotlib for data analysis & visualization</li>
  <li>Google Gemini API (via google.generativeai)</li>
  <li>python-dotenv for environment management</li>
</ul>

<h2>⚡ Installation</h2>
<ol>
  <li>Clone the repository:
    <pre><code>git clone https://github.com/EsraaMeslam/your-repo-name.git
cd your-repo-name</code></pre>
  </li>
  <li>Create a virtual environment (recommended):
    <pre><code>python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows</code></pre>
  </li>
  <li>Install dependencies:
    <pre><code>pip install -r requirements.txt</code></pre>
  </li>
  <li>Add your Gemini API key in a <code>.env</code> file:
    <pre><code>GEMINI_API_KEY=your_gemini_api_key_here</code></pre>
  </li>
</ol>

<h2>🚀 Usage</h2>
<ol>
  <li>Run the Streamlit app:
    <pre><code>streamlit run app.py</code></pre>
  </li>
  <li>Upload one or more PDF resumes.</li>
  <li>Paste the job description.</li>
  <li>Click <strong>🚀 ANALYZE RESUME(S)</strong> to view ATS scores, charts, and recommendations.</li>
  <li>Use the <strong>Interactive Chat</strong> tab for personalized advice or resume comparison.</li>
</ol>

<h2>📄 Reports</h2>
<ul>
  <li>Professional <strong>PDF reports</strong> with ATS scores, missing keywords, strengths, weaknesses, and recommendations.</li>
  <li>Comprehensive <strong>Excel reports</strong> with summary and detailed metrics per resume.</li>
</ul>

<h2>🔗 Links</h2>
<ul>
  <li>🌐 <a href="https://smart-ats-analyzer.streamlit.app/" target="_blank">Live App</a></li>
  <li><a href="https://www.linkedin.com/in/esraa-meslam-873a20241" target="_blank">LinkedIn</a></li>
  <li><a href="https://github.com/EsraaMeslam" target="_blank">GitHub</a></li>
</ul>

<h2>💡 Notes</h2>
<ul>
  <li>Ensure a valid <strong>GEMINI_API_KEY</strong> in your <code>.env</code> file.</li>
  <li>Supports PDF resumes only.</li>
</ul>

<h2>📌 License</h2>
<p>MIT License © 2025 Esraa Meslam</p>

</body>
</html>
