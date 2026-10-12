import re
import streamlit as st

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="I2PE | AI Privacy Protection",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------- GRADIENT UI ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.stApp {
    background: linear-gradient(135deg, #0f1028 0%, #171b3d 50%, #25205a 100%);
    color: #f8fafc;
    font-family: 'Inter', sans-serif;
}

.block-container {
    max-width: 1150px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

header[data-testid="stHeader"] {
    background: transparent;
}

.hero {
    padding: 35px 30px;
    border: 1px solid rgba(255,255,255,.15);
    border-radius: 24px;
    background: linear-gradient(120deg,
        rgba(124,58,237,.35),
        rgba(37,99,235,.20));
    margin-bottom: 25px;
}

.eyebrow {
    color: #c4b5fd;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 2px;
}

.hero h1 {
    color: white;
    font-size: clamp(30px, 5vw, 48px);
    font-weight: 800;
    margin: 12px 0;
}

.hero p {
    color: #dbe4ff;
    font-size: 16px;
    line-height: 1.7;
}

.panel {
    background: rgba(255,255,255,.065);
    border: 1px solid rgba(255,255,255,.13);
    border-radius: 18px;
    padding: 22px;
    margin: 12px 0;
}

.section-title {
    font-size: 21px;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 8px;
}

.small-muted {
    color: #b9c3e5;
    font-size: 13px;
    line-height: 1.6;
}

.metric {
    padding: 20px;
    border-radius: 16px;
    background: linear-gradient(135deg,
        rgba(124,58,237,.25),
        rgba(59,130,246,.16));
    border: 1px solid rgba(167,139,250,.25);
    text-align: center;
}

.metric-number {
    font-size: 34px;
    font-weight: 800;
    color: #c4b5fd;
}

.metric-label {
    color: #dbe4ff;
    font-size: 13px;
    margin-top: 5px;
}

div[data-testid="stTextArea"] textarea {
    background: #11162f !important;
    color: #f8fafc !important;
    border: 1px solid #454b79 !important;
    border-radius: 12px !important;
    font-size: 14px !important;
    line-height: 1.7 !important;
}

div[data-testid="stFileUploader"] {
    background: rgba(255,255,255,.04);
    border: 1px dashed #7778c8;
    border-radius: 14px;
    padding: 12px;
}

.stButton > button,
.stDownloadButton > button {
    background: linear-gradient(100deg, #7c3aed, #2563eb);
    color: white !important;
    border: none;
    border-radius: 12px;
    padding: 12px 20px;
    font-weight: 700;
    min-height: 45px;
    width: 100%;
    transition: .2s ease;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    background: linear-gradient(100deg, #8b5cf6, #3b82f6);
    border: 1px solid #c4b5fd;
    transform: translateY(-1px);
}

div[data-testid="stAlert"] {
    border-radius: 12px;
}

.footer {
    text-align: center;
    color: #9ca9d1;
    font-size: 12px;
    padding: 24px 0 5px;
}

hr {
    border-color: rgba(255,255,255,.12);
}

@media (max-width: 700px) {
    .block-container {
        padding: 1rem;
    }
    .hero {
        padding: 23px 18px;
    }
    .panel {
        padding: 15px;
    }
}
</style>
""", unsafe_allow_html=True)


# ---------------- PII DETECTION ----------------
def redact_pii(text):
    """Detect and redact common PII patterns locally."""

    protected = text
    detected = {}

    patterns = [
        (
            "Aadhaar-like number",
            re.compile(
                r"(?<!\d)(?:\d{4}[\s-]\d{4}[\s-]\d{4}|\d{12})(?!\d)"
            ),
        ),
        (
            "Email address",
            re.compile(
                r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
            ),
        ),
        (
            "Phone number",
            re.compile(
                r"(?<!\w)(?:\+91[\s-]?)?[6-9]\d{9}(?!\d)"
            ),
        ),
        (
            "Name in Name field",
            re.compile(
                r"(?im)^(\s*Name\s*:\s*)"
                r"([A-Z][A-Za-z'-]*"
                r"(?:\s+[A-Z][A-Za-z'-]*)*)"
            ),
        ),
        (
            "Name in message",
            re.compile(
                r"\b(my\s+name\s+is\s+)"
                r"([A-Z][A-Za-z'-]*"
                r"(?:\s+[A-Z][A-Za-z'-]*)*)",
                re.IGNORECASE,
            ),
        ),
    ]

    for label, pattern in patterns:
        matches = list(pattern.finditer(protected))
        detected[label] = len(matches)

        if label in ("Name in Name field", "Name in message"):
            protected = pattern.sub(
                lambda match: match.group(1) + "[REDACTED]",
                protected,
            )
        else:
            protected = pattern.sub("[REDACTED]", protected)

    return protected, detected


# ---------------- HEADER ----------------
st.markdown("""
<div class="hero">
    <div class="eyebrow">I2PE • PRIVACY-FIRST TECHNOLOGY</div>
    <h1>🔐 AI Privacy Protection</h1>
    <p>
        Protect sensitive information before sharing your documents.
        Detect personal information, redact it, and download a safer
        version in seconds.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="small-muted">
    🛡️ Local text processing &nbsp; • &nbsp;
    📄 Document protection &nbsp; • &nbsp;
    ⚡ Instant scanning
</div>
""", unsafe_allow_html=True)

st.write("")

# ---------------- INPUT SECTION ----------------
left, right = st.columns([1, 1], gap="large")

with left:
    st.markdown('<div class="section-title">📄 Your Document</div>',
                unsafe_allow_html=True)
    st.markdown(
        '<div class="small-muted">Upload a TXT file or paste text below.</div>',
        unsafe_allow_html=True,
    )

    uploaded_file = st.file_uploader(
        "Upload a text document",
        type=["txt"],
        help="Only plain-text TXT files are supported.",
    )

    default_text = (
        "I2PE SAMPLE DOCUMENT\n"
        "--------------------\n\n"
        "Name: Priya Kumar\n"
        "Email: priya.kumar@example.com\n"
        "Phone: 9876543210\n"
        "Aadhaar-like number: 1234 5678 9012\n\n"
        "Message:\n"
        "Hello, my name is Priya Kumar. Please contact me at "
        "priya.kumar@example.com or call 9876543210 regarding my document.\n\n"
        "Note: These are fictional sample details for testing only."
    )

    if uploaded_file is not None:
        try:
            input_text = uploaded_file.getvalue().decode(
                "utf-8", errors="replace"
            )
        except Exception:
            input_text = ""
            st.error("Unable to read this file. Please upload a TXT file.")
    else:
        input_text = default_text

    source_text = st.text_area(
        "Original text",
        value=input_text,
        height=300,
        key="source_text",
        placeholder="Paste your document text here...",
    )

    scan_clicked = st.button(
        "🔍  Detect & Redact PII",
        use_container_width=True,
    )

with right:
    st.markdown('<div class="section-title">✨ How It Works</div>',
                unsafe_allow_html=True)

    st.markdown("""
    <div class="panel">
        <h3>01 &nbsp; Detect</h3>
        <p class="small-muted">
            Scan text for common personal identifiers such as emails,
            phone numbers, Aadhaar-like numbers and names.
        </p>
    </div>
    <div class="panel">
        <h3>02 &nbsp; Protect</h3>
        <p class="small-muted">
            Replace detected values with [REDACTED] while retaining
            the surrounding document text.
        </p>
    </div>
    <div class="panel">
        <h3>03 &nbsp; Download</h3>
        <p class="small-muted">
            Review the protected result and download it as a TXT file.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.info(
        "Tip: Use fictional sample data while testing your prototype."
    )


# ---------------- SCAN RESULTS ----------------
if scan_clicked:
    if not source_text.strip():
        st.warning("Please enter some text or upload a non-empty TXT file.")
    else:
        protected_text, detection_counts = redact_pii(source_text)
        total_detected = sum(detection_counts.values())

        st.session_state["protected_text"] = protected_text
        st.session_state["detection_counts"] = detection_counts
        st.session_state["total_detected"] = total_detected
        st.session_state["scanned"] = True

if st.session_state.get("scanned", False):
    protected_text = st.session_state["protected_text"]
    detection_counts = st.session_state["detection_counts"]
    total_detected = st.session_state["total_detected"]

    st.divider()
    st.markdown(
        '<div class="section-title">📊 Privacy Scan Results</div>',
        unsafe_allow_html=True,
    )

    metric1, metric2, metric3 = st.columns(3)

    with metric1:
        st.markdown(f"""
        <div class="metric">
            <div class="metric-number">{total_detected}</div>
            <div class="metric-label">Detected occurrences</div>
        </div>
        """, unsafe_allow_html=True)

    with metric2:
        st.markdown(f"""
        <div class="metric">
            <div class="metric-number">{sum(v > 0 for v in detection_counts.values())}</div>
            <div class="metric-label">PII categories found</div>
        </div>
        """, unsafe_allow_html=True)

    with metric3:
        st.markdown("""
        <div class="metric">
            <div class="metric-number">✓</div>
            <div class="metric-label">Scan completed</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.markdown("#### 🔎 Detection Breakdown")

    for label, count in detection_counts.items():
        if count:
            st.write(f"**{label}:** {count}")
        else:
            st.caption(f"{label}: 0")

    original_col, protected_col = st.columns(2, gap="large")

    with original_col:
        st.markdown("#### 📄 Original Text")
        st.text_area(
            "Original document preview",
            value=source_text,
            height=280,
            disabled=True,
            key="original_preview",
        )

    with protected_col:
        st.markdown("#### 🔐 Protected Text")
        st.text_area(
            "Redacted document preview",
            value=protected_text,
            height=280,
            disabled=True,
            key="protected_preview",
        )

    st.download_button(
        label="⬇️ Download Protected Text",
        data=protected_text.encode("utf-8"),
        file_name="protected_document.txt",
        mime="text/plain",
        use_container_width=True,
    )

    if total_detected:
        st.success("Privacy scan completed. Review the protected text before sharing.")
    else:
        st.info(
            "No supported PII patterns were detected. "
            "This does not guarantee that the text contains no sensitive data."
        )

    st.caption(
        "Important: This prototype uses regular expressions, not an AI model. "
        "Detection may miss unusual formats or redact text incorrectly. "
        "Review results before sharing."
    )

else:
    st.write("")
    st.markdown("""
    <div class="panel">
        <h3>🔒 Ready to protect your data?</h3>
        <p class="small-muted">
            Your scan results will appear here after you click
            Detect & Redact PII.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ---------------- FOOTER ----------------
st.markdown("""
<div class="footer">
    I2PE AI Privacy Protection • Privacy by Design<br>
    Built for secure document handling
</div>
""", unsafe_allow_html=True)