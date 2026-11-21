
import streamlit as st
import os
import json
import uuid
from io import BytesIO
from datetime import datetime
from xml.sax.saxutils import escape

from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors


# PAGE CONFIGURATION
st.set_page_config(
    page_title="AI Scene Investigator",
    page_icon="🎥",
    layout="wide",
    initial_sidebar_state="expanded"
)


# CUSTOM CSS
st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(ellipse at top left, #172554 0%, transparent 45%),
        linear-gradient(135deg, #080d1b, #111827 55%, #17112d);
    color: #f1f5f9;
}

header[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1400px;
}

.hero {
    padding: 38px;
    border-radius: 22px;
    background: linear-gradient(120deg, #172554, #312e81, #581c87);
    border: 1px solid #6366f1;
    box-shadow: 0 12px 35px rgba(79, 70, 229, 0.18);
    margin-bottom: 28px;
}

.hero h1 {
    color: white;
    font-size: 40px;
    font-weight: 800;
    margin-bottom: 10px;
}

.hero p {
    color: #c7d2fe;
    font-size: 16px;
}

.hero-tag {
    display: inline-block;
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.2);
    padding: 6px 13px;
    border-radius: 20px;
    color: #e0e7ff;
    font-size: 12px;
    margin-bottom: 15px;
}

.section-title {
    color: #e0e7ff;
    font-size: 23px;
    font-weight: 750;
    margin-top: 22px;
    margin-bottom: 14px;
}

.info-card {
    background: linear-gradient(145deg, #172033, #111827);
    padding: 20px;
    border-radius: 16px;
    border: 1px solid #334155;
    margin-bottom: 14px;
}

.stButton > button,
.stDownloadButton > button {
    background: linear-gradient(90deg, #4f46e5, #7c3aed);
    color: white;
    border: 1px solid #6366f1;
    border-radius: 11px;
    padding: 11px 20px;
    font-weight: 650;
    transition: 0.2s;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    background: linear-gradient(90deg, #6366f1, #9333ea);
    border: 1px solid #a78bfa;
    color: white;
}

[data-testid="stFileUploader"] {
    background: #172033;
    padding: 18px;
    border-radius: 15px;
    border: 1px dashed #6366f1;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a, #111827);
    border-right: 1px solid #29364f;
}

[data-testid="stMetric"] {
    background: linear-gradient(145deg, #1e293b, #172033);
    padding: 18px;
    border-radius: 15px;
    border: 1px solid #334155;
}

[data-testid="stMetricValue"] {
    color: #c4b5fd;
    font-weight: 800;
}

[data-testid="stMetricLabel"] {
    color: #cbd5e1;
}

div[data-testid="stExpander"] {
    background: #172033;
    border: 1px solid #334155;
    border-radius: 12px;
}

.stTextInput input {
    border-radius: 10px;
}

div[data-testid="stVideo"] {
    border: 1px solid #475569;
    border-radius: 15px;
    overflow: hidden;
}

hr {
    border-color: #334155;
}

.footer {
    text-align: center;
    color: #94a3b8;
    padding: 15px;
    font-size: 13px;
}

</style>
""", unsafe_allow_html=True)


# SESSION STATE
defaults = {
    "processed": False,
    "answer": None,
    "video_folder": None,
    "upload_id": None,
    "video_filename": None
}

for key, value in defaults.items():

    if key not in st.session_state:
        st.session_state[key] = value


# SIDEBAR
with st.sidebar:

    st.markdown("# 🎥 AI Investigator")

    st.caption("VIDEO INTELLIGENCE PLATFORM")

    st.divider()

    st.markdown("### 🧩 Project Modules")

    st.write("🔍 YOLO Object Detection")
    st.write("🧠 BLIP Scene Analysis")
    st.write("🎯 ByteTrack Tracking")
    st.write("📚 FAISS Semantic Search")
    st.write("🤖 Gemini RAG")
    st.write("📄 PDF Report Generation")

    st.divider()

    st.markdown("### ⚙️ System Status")

    st.success("Video Engine Ready")
    st.success("Vector Search Ready")

    st.divider()

    if st.button("🔄 New Investigation", use_container_width=True):

        st.session_state.processed = False
        st.session_state.video_folder = None
        st.session_state.answer = None
        st.session_state.upload_id = None
        st.session_state.video_filename = None

        st.rerun()

    st.divider()

    st.caption("Developed as a BCA AI & ML Project")


# HERO SECTION
st.markdown("""
<div class="hero">

    <div class="hero-tag">
        AI POWERED VIDEO INTELLIGENCE
    </div>

    <h1>🎥 AI Scene Investigator</h1>

    <p>
        Transform ordinary videos into searchable intelligence
        using Computer Vision, Deep Learning and
        Retrieval-Augmented Generation.
    </p>

</div>
""", unsafe_allow_html=True)


# UPLOAD SECTION
st.markdown(
    '<div class="section-title">📁 Video Investigation</div>',
    unsafe_allow_html=True
)

uploaded_video = st.file_uploader(
    "Upload a video to begin your investigation",
    type=["mp4", "avi", "mov", "mkv"]
)


if uploaded_video is not None:

    upload_id = uploaded_video.name + str(uploaded_video.size)

    if st.session_state.upload_id != upload_id:

        st.session_state.upload_id = upload_id
        st.session_state.processed = False
        st.session_state.video_folder = None
        st.session_state.answer = None
        st.session_state.video_filename = uploaded_video.name

    col1, col2 = st.columns([1.5, 1])

    with col1:

        st.markdown("### 🎬 Original Video")

        st.video(uploaded_video.getvalue())

    with col2:

        st.markdown("### 📋 Video Information")

        st.markdown('<div class="info-card">', unsafe_allow_html=True)

        st.write("**Filename**")
        st.write(uploaded_video.name)

        st.write("**File Size**")
        st.write(
            f"{uploaded_video.size / (1024 * 1024):.2f} MB"
        )

        st.write("**Supported Formats**")
        st.write("MP4, AVI, MOV, MKV")

        st.success("Video Ready for Investigation")

        st.markdown('</div>', unsafe_allow_html=True)

        if st.button("🚀 Start Video Investigation", use_container_width=True):

            os.makedirs("uploads", exist_ok=True)

            unique_name = (
                uuid.uuid4().hex[:8]
                + "_"
                + os.path.basename(uploaded_video.name)
            )

            video_path = os.path.join(
                "uploads",
                unique_name
            )

            with open(video_path, "wb") as file:
                file.write(uploaded_video.getvalue())

            try:

                progress = st.progress(0, text="Starting investigation...")

                with st.spinner(
                    "Running video analysis, object tracking and AI processing..."
                ):

                    progress.progress(20, text="Extracting video frames...")

                    from modules.video_pipeline import process_video_pipeline

                    progress.progress(40, text="Running AI analysis...")

                    video_id = process_video_pipeline(video_path)

                    progress.progress(100, text="Investigation completed!")

                if video_id:

                    st.session_state.video_folder = os.path.join(
                        "outputs",
                        video_id
                    )

                    st.session_state.processed = True
                    st.session_state.answer = None

                    st.success("Video investigation completed successfully!")

                    st.rerun()

                else:

                    st.error("Video processing failed.")

            except Exception as e:

                st.error("An error occurred during video processing.")
                st.exception(e)


# ANALYSIS SECTION
if st.session_state.processed:

    video_folder = st.session_state.video_folder

    events_path = os.path.join(
        video_folder,
        "events.json"
    )

    if os.path.exists(events_path):

        with open(events_path, "r") as file:
            events = json.load(file)

        if not isinstance(events, list):

            st.error("Invalid event data format.")
            st.stop()

        # ANNOTATED VIDEO
        st.divider()

        st.markdown(
            '<div class="section-title">🎯 AI Object Detection & Tracking</div>',
            unsafe_allow_html=True
        )

        annotated_video_path = os.path.join(
            video_folder,
            "annotated_video.mp4"
        )

        if os.path.exists(annotated_video_path):

            st.success("YOLO Object Detection and ByteTrack tracking completed!")

            st.video(annotated_video_path)

            st.caption(
                "Annotated video: bounding boxes, object labels, "
                "confidence scores and tracking IDs where available."
            )

        else:

            st.warning(
                "Annotated video was not found. "
                "Please process the video again."
            )

        # OBJECT ANALYTICS
        object_counts = {}

        for event in events:

            for name, count in event.get("objects", {}).items():

                object_counts[name] = (
                    object_counts.get(name, 0) + count
                )

        total_detections = sum(object_counts.values())

        st.divider()

        st.markdown(
            '<div class="section-title">📊 Video Analytics Dashboard</div>',
            unsafe_allow_html=True
        )

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Observations",
            len(events)
        )

        col2.metric(
            "Object Categories",
            len(object_counts)
        )

        col3.metric(
            "Total Detections",
            total_detections
        )

        col4.metric(
            "Video Status",
            "Processed"
        )

        st.caption(
            "Detection totals are summed across sampled video frames."
        )

        # OBJECT DETECTION STATISTICS
        st.markdown(
            '<div class="section-title">🔍 Detected Objects</div>',
            unsafe_allow_html=True
        )

        if object_counts:

            columns = st.columns(min(len(object_counts), 4))

            for i, (name, count) in enumerate(object_counts.items()):

                with columns[i % len(columns)]:

                    st.metric(
                        name.title(),
                        count
                    )

            st.markdown("### 📈 Object Distribution")

            st.bar_chart(
                object_counts,
                horizontal=True
            )

        else:

            st.info("No objects were detected in the sampled frames.")

        # EVENT TIMELINE
        st.divider()

        st.markdown(
            '<div class="section-title">⏱️ Event Investigation Timeline</div>',
            unsafe_allow_html=True
        )

        search_event = st.text_input(
            "🔎 Search scene observations",
            placeholder="Search for person, bottle, chair, etc."
        )

        filtered_events = []

        for event in events:

            description = str(event.get("description", ""))
            objects = str(event.get("objects", ""))

            if (
                search_event.lower() in description.lower()
                or search_event.lower() in objects.lower()
            ):

                filtered_events.append(event)

        st.caption(
            f"Showing {len(filtered_events)} of {len(events)} observations"
        )

        for event in filtered_events:

            with st.expander(
                f"⏱️ {event.get('timestamp', 'Unknown')} seconds"
            ):

                st.markdown("**📝 Scene Description**")

                st.write(
                    event.get(
                        "description",
                        "No description available"
                    )
                )

                st.markdown("**🔍 Detected Objects**")

                st.json(
                    event.get("objects", {})
                )

        # AI QUESTION ANSWERING
        st.divider()

        st.markdown(
            '<div class="section-title">🤖 AI Investigation Assistant</div>',
            unsafe_allow_html=True
        )

        st.caption(
            "Ask questions about the uploaded video using semantic search and RAG."
        )

        with st.form("question_form"):

            question = st.text_input(
                "Ask anything about your video",
                placeholder="Example: What objects are visible in this video?"
            )

            submitted = st.form_submit_button(
                "✨ Generate AI Answer",
                use_container_width=True
            )

        if submitted:

            if question.strip():

                try:

                    with st.spinner(
                        "Searching video evidence and generating AI response..."
                    ):

                        from modules.rag_pipeline import ask_video

                        answer = ask_video(
                            question,
                            video_folder
                        )

                    st.session_state.answer = answer

                except Exception as e:

                    st.error("Unable to generate an answer.")
                    st.exception(e)

            else:

                st.warning("Please enter a question.")

        if st.session_state.answer:

            st.markdown("### 💬 Investigation Result")

            st.markdown(
                '<div class="info-card">',
                unsafe_allow_html=True
            )

            st.markdown(st.session_state.answer)

            st.markdown('</div>', unsafe_allow_html=True)

        else:

            st.info(
                "Enter a question above to generate an AI investigation response."
            )

        # PDF REPORT
        st.divider()

        st.markdown(
            '<div class="section-title">📥 Investigation Report</div>',
            unsafe_allow_html=True
        )

        def create_pdf_report():

            pdf_buffer = BytesIO()

            doc = SimpleDocTemplate(
                pdf_buffer,
                pagesize=A4,
                rightMargin=40,
                leftMargin=40,
                topMargin=40,
                bottomMargin=40
            )

            styles = getSampleStyleSheet()

            cell_style = ParagraphStyle(
                "CellStyle",
                parent=styles["Normal"],
                fontSize=8,
                leading=11
            )

            content = []

            content.append(
                Paragraph(
                    "AI SCENE INVESTIGATOR",
                    styles["Title"]
                )
            )

            content.append(Spacer(1, 15))

            content.append(
                Paragraph(
                    f"Video: {escape(str(st.session_state.get('video_filename', 'Unknown')))}",
                    styles["Normal"]
                )
            )

            content.append(
                Paragraph(
                    f"Video ID: {escape(os.path.basename(video_folder))}",
                    styles["Normal"]
                )
            )

            content.append(
                Paragraph(
                    f"Report Date: {datetime.now().strftime('%d-%m-%Y %H:%M')}",
                    styles["Normal"]
                )
            )

            content.append(
                Paragraph(
                    f"Total Observations: {len(events)}",
                    styles["Normal"]
                )
            )

            content.append(
                Paragraph(
                    f"Total Detections Across Sampled Frames: {total_detections}",
                    styles["Normal"]
                )
            )

            content.append(Spacer(1, 20))

            content.append(
                Paragraph(
                    "VIDEO EVENT TIMELINE",
                    styles["Heading2"]
                )
            )

            content.append(Spacer(1, 10))

            table_data = [[
                Paragraph("<b>Timestamp</b>", cell_style),
                Paragraph("<b>Scene Description</b>", cell_style),
                Paragraph("<b>Detected Objects</b>", cell_style)
            ]]

            for event in events:

                objects = event.get("objects", {})

                object_text = ", ".join(
                    f"{count} {name}"
                    for name, count in objects.items()
                ) if objects else "None"

                table_data.append([
                    Paragraph(
                        escape(str(event.get("timestamp", ""))) + " sec",
                        cell_style
                    ),
                    Paragraph(
                        escape(str(event.get("description", ""))),
                        cell_style
                    ),
                    Paragraph(
                        escape(object_text),
                        cell_style
                    )
                ])

            table = Table(
                table_data,
                colWidths=[75, 250, 160],
                repeatRows=1
            )

            table.setStyle(
                TableStyle([
                    ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("PADDING", (0, 0), (-1, -1), 7)
                ])
            )

            content.append(table)

            content.append(Spacer(1, 25))

            content.append(
                Paragraph(
                    "AI QUESTION AND ANSWER",
                    styles["Heading2"]
                )
            )

            content.append(Spacer(1, 10))

            answer_text = st.session_state.get(
                "answer",
                "No AI answer available yet."
            )

            for line in str(answer_text).split("\n"):

                line = line.strip()

                if line:

                    content.append(
                        Paragraph(
                            escape(line),
                            styles["Normal"]
                        )
                    )

                    content.append(Spacer(1, 5))

            content.append(Spacer(1, 20))

            content.append(
                Paragraph(
                    "Report generated by AI Scene Investigator.",
                    styles["Italic"]
                )
            )

            doc.build(content)

            pdf_buffer.seek(0)

            return pdf_buffer.getvalue()

        try:

            pdf_data = create_pdf_report()

            st.download_button(
                label="📄 Download PDF Investigation Report",
                data=pdf_data,
                file_name="AI_Investigation_Report.pdf",
                mime="application/pdf",
                use_container_width=True
            )

        except Exception as e:

            st.error("Unable to create the PDF report.")
            st.exception(e)

    else:

        st.error(
            "Events file not found. Please process the video again."
        )

else:

    st.info(
        "Upload a video above and click Start Video Investigation to begin."
    )


# FOOTER
st.divider()

st.markdown("""
<div class="footer">
    🎥 AI Scene Investigator
    <br>
    Computer Vision • Deep Learning • NLP • RAG
    <br>
    BCA Artificial Intelligence & Machine Learning Project
</div>
""", unsafe_allow_html=True)
