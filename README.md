<h1>📄 Smart ATS Resume Analyzer</h1>

<p>
  Optimize your resume for <strong>Applicant Tracking Systems (ATS)</strong> with AI-powered analysis.
  The Smart ATS Analyzer evaluates resumes against job descriptions, highlights missing keywords,
  identifies strengths and weaknesses, and provides actionable recommendations to improve your chances of landing interviews.
</p>

<p>
  🚀 <strong>Live Demo:</strong>
  <a href="https://smart-ats-analyzer.streamlit.app/" target="_blank" rel="noopener noreferrer">
    https://smart-ats-analyzer.streamlit.app/
  </a>
</p>

<hr/>

<h2>✨ Features</h2>
<ul>
  <li>📑 <strong>Multi-Resume Upload</strong> – Upload multiple PDF resumes for side-by-side analysis.</li>
  <li>🤖 <strong>AI-Powered ATS Scoring</strong> – Uses Google Gemini to compute ATS Score, Match %, Readability, and Skill Alignment.</li>
  <li>🔍 <strong>Deep Insights</strong> – Missing keywords, strengths, weaknesses, and tailored recommendations.</li>
  <li>📊 <strong>Visual Analytics</strong> – Interactive charts for ATS scores and match percentages per resume.</li>
  <li>📥 <strong>Export Reports</strong> – Download professional PDF and detailed Excel summaries.</li>
  <li>💬 <strong>Interactive Chat Assistant</strong> – Ask the bot to compare resumes, explain gaps, and suggest improvements.</li>
</ul>

<h2>🛠️ Tech Stack</h2>
<ul>
  <li><strong>Frontend/UI:</strong> Streamlit</li>
  <li><strong>AI Model:</strong> Google Gemini API</li>
  <li><strong>Backend Processing:</strong> Python (PyPDF2, re, json)</li>
  <li><strong>Data & Charts:</strong> Pandas, Matplotlib</li>
  <li><strong>Reporting:</strong> FPDF, Excel (openpyxl)</li>
</ul>

<h2>📥 Installation & Setup</h2>
<ol>
  <li>
    <p><strong>Clone the repository:</strong></p>
    <pre><code>git clone https://github.com/your-username/smart-ats-analyzer.git
cd smart-ats-analyzer
</code></pre>
  </li>
  <li>
    <p><strong>Create and activate a virtual environment:</strong></p>
    <pre><code>python -m venv venv
# Linux/Mac
source venv/bin/activate
# Windows
venv\Scripts\activate
</code></pre>
  </li>
  <li>
    <p><strong>Install dependencies:</strong></p>
    <pre><code>pip install -r requirements.txt
</code></pre>
  </li>
  <li>
    <p><strong>Set environment variables:</strong></p>
    <p>Create a <code>.env</code> file in the project root and add your Gemini API key:</p>
    <pre><code>GEMINI_API_KEY=your_api_key_here
</code></pre>
  </li>
  <li>
    <p><strong>Run the app:</strong></p>
    <pre><code>streamlit run app.py
</code></pre>
  </li>
</ol>

<h2>📊 How It Works</h2>
<ol>
  <li>Upload one or more resumes in <strong>PDF</strong> format.</li>
  <li>Paste the target job description.</li>
  <li>The AI analyzes and scores each resume.</li>
  <li>Review insights: missing keywords, strengths, weaknesses, readability, and recommendations.</li>
  <li>Export a <strong>PDF report</strong> and an <strong>Excel</strong> file (summary + details).</li>
  <li>Use the <strong>Interactive Chat</strong> to ask questions or compare resumes.</li>
</ol>

<h2>📈 Example Use Cases</h2>
<ul>
  <li>Job seekers optimizing resumes for ATS compliance.</li>
  <li>Career coaches providing data-driven feedback.</li>
  <li>Recruiters assessing alignment with job descriptions.</li>
</ul>

<h2>🧭 Recommended Questions for the Chat Assistant</h2>
<ul>
  <li>“Which uploaded resume has the highest ATS score and why?”</li>
  <li>“What general recommendations can improve all uploaded resumes?”</li>
  <li>“What keywords are missing in <em>Resume_B.pdf</em> compared to the job description?”</li>
</ul>

<h2>👤 Author</h2>
<p>
  <strong>Esraa Meslam</strong><br/>
  <a href="https://www.linkedin.com/in/esraa-meslam-873a20241" target="_blank" rel="noopener noreferrer">LinkedIn</a> |
  <a href="https://github.com/EsraaMeslam" target="_blank" rel="noopener noreferrer">GitHub</a>
</p>

<h2>⭐ Contribute</h2>
<p>
  Contributions, issues, and feature requests are welcome. Please open an issue or a pull request.
  If you find this project helpful, consider giving it a ⭐ on GitHub.
</p>

<hr/>

<p>
  <em>Tip:</em> Add screenshots or a short GIF preview of the Streamlit app to make the README more engaging for visitors.
</p>
