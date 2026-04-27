import streamlit as st
from pypdf import PdfReader
from multi_agent_system import run_resume_analysis

st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄")

# Custom CSS for sci-fi violet dark blue aesthetics
st.markdown("""
    <style>
        /* Sci-Fi Grid Background */
        .stApp {
            background-color: #050A1F !important;
            background-image: 
                linear-gradient(rgba(139, 92, 246, 0.15) 1px, transparent 1px),
                linear-gradient(90deg, rgba(139, 92, 246, 0.15) 1px, transparent 1px);
            background-size: 40px 40px;
        }

        /* Main heading style - Neon Glowing */
        h1 {
            color: #ffffff !important;
            text-align: center;
            font-weight: 900;
            text-transform: uppercase;
            letter-spacing: 4px;
            text-shadow: 0 0 10px #8B5CF6, 0 0 20px #8B5CF6, 0 0 35px #8B5CF6;
            margin-bottom: 40px;
            margin-top: 10px;
        }

        /* Subheaders */
        h3 {
            color: #E2D6FF !important;
            text-transform: uppercase;
            letter-spacing: 2px;
            border-bottom: 2px solid #8B5CF6;
            padding-bottom: 5px;
            text-shadow: 0 0 5px rgba(139, 92, 246, 0.8);
            margin-top: 20px;
        }

        /* Inputs - Techy / Terminal look */
        .stTextArea textarea, .stFileUploader > div {
            background-color: rgba(11, 19, 54, 0.85) !important;
            border: 2px solid #8B5CF6 !important;
            border-radius: 4px !important;
            color: #ffffff !important;
            box-shadow: inset 0 0 10px rgba(139, 92, 246, 0.2);
            font-family: 'Courier New', Courier, monospace !important;
        }
        .stTextArea textarea:focus {
            box-shadow: 0 0 15px rgba(139, 92, 246, 0.8) !important;
            border-color: #A78BFA !important;
        }

        /* Button - Cyberpunk Glow */
        .stButton button {
            background: transparent !important;
            color: #ffffff !important;
            border: 2px solid #8B5CF6 !important;
            border-radius: 4px !important;
            text-transform: uppercase;
            letter-spacing: 2px;
            font-weight: bold !important;
            transition: all 0.3s ease !important;
            width: 100% !important;
            box-shadow: 0 0 10px rgba(139, 92, 246, 0.4), inset 0 0 10px rgba(139, 92, 246, 0.4) !important;
            padding: 10px !important;
            font-family: 'Courier New', Courier, monospace !important;
        }
        .stButton button:hover {
            background: #8B5CF6 !important;
            transform: scale(1.02);
            box-shadow: 0 0 20px #8B5CF6, 0 0 40px #8B5CF6 !important;
        }

        /* Output Boxes */
        .stSuccess, .stInfo, .stWarning {
            background-color: rgba(5, 10, 31, 0.9) !important;
            border: 1px solid #8B5CF6 !important;
            border-left: 5px solid #8B5CF6 !important;
            color: #ffffff !important;
            box-shadow: 0 0 10px rgba(139, 92, 246, 0.3);
        }
        
        /* Markdown / generic text styling */
        .stMarkdown p {
            color: #E2D6FF !important;
        }
    </style>
""", unsafe_allow_html=True)

st.title("NEURAL_RESUME_ANALYSIS//_")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### TARGET_PARAMETERS")
    jd = st.text_area("INPUT_JOB_DESCRIPTION_DATA", height=200)

with col2:
    st.markdown("### SUBJECT_DATA")
    uploaded_file = st.file_uploader("UPLOAD_DOCUMENT_MATRIX (PDF)", type=["pdf"])

def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

st.markdown("---")

# Button Area
_, center_col, _ = st.columns([1, 2, 1])
with center_col:
    analyze_btn = st.button("EXECUTE_ANALYSIS_PROTOCOL")

if analyze_btn:
    if not jd or not uploaded_file:
        st.warning("SYSTEM_ERROR: REQUIRE BOTH TARGET_PARAMETERS AND SUBJECT_DATA")
    else:
        resume_text = extract_text_from_pdf(uploaded_file)

        with st.spinner("INITIATING_NEURAL_PROCESSING..."):
            result = run_resume_analysis(jd, resume_text)

        st.markdown("---")
        
        st.subheader("SYSTEM_EVALUATION_SCORE")
        st.success(result["score"])

        st.subheader("OPTIMIZATION_SUGGESTIONS")
        st.info(result["suggestions"])

        st.subheader("PROJECT_DIRECTIVES")
        st.markdown(result["project_suggestions"])