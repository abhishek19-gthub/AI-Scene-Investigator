
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
    background: linear-gradient(135deg, #0b1020, #111827);
}

header[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1300px;
}

.hero {
    padding: 30px;
    border-radius: 18px;
    background: linear-gradient(120deg, #172554, #312e81, #4c1d95);
    border: 1px solid #4338ca;
    margin-bottom: 25px;
}

.hero h1 {
    color: white;
    font-size: 38px;
    margin-bottom: 8px;
}

.hero p {
    color: #c7d2fe;
    font-size: 16px;
}

.section-title {
    color: #e0e7ff;
    font-size: 23px;
    font-weight: 700;
    margin-top: 20px;
    margin-bottom: 12px;
}

.info-card {
    background: #172033;
    padding: 20px;
    border-radius: 14px;
    border: 1px solid #29364f;
    margin-bottom: 12px;
}

.stButton > button {
    background: linear-gradient(90deg, #4f46e5, #7c3aed);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 10px 20px;
    font-weight: 600;
    width: 100%;
}

.stButton > button:hover {
    background: linear-gradient(90deg, #6366f1, #8b5cf6);
    color: white;
    border: none;
}

[data-testid="stFileUploader"] {
    background: #172033;
    padding: 18px;
    border-radius: 14px;
    border: 1px dashed #6366f1;
}

[data-testid="stSidebar"] {
    background: #0f172a;
}

[data-testid="stMetric"] {
    background: #172033;
    padding: 15px;
    border-radius: 12px;
    border: 1px solid #29364f;
}

</style>
""", unsafe_allow_html=True)


# SESSION STATE
if "processed" not in st.session_state:
    st.session_state.processed = False

if "answer" not in st.session_state:
    st.session_state.answer = None

if "video_folder" not in st.session_state:
    st.session_state.video_folder = None


# SIDEBAR
with st.sidebar:

    st.title("🎥 AI Investigator")

    st.caption("VIDEO INTELLIGENCE PLATFORM")

    st.divider()

    st.markdown("### Project Modules")

    st.write("🔍 YOLO Object Detection")
    st.write("🧠 BLIP Scene Analysis")
    st.write("🎯 ByteTrack Tracking")
    st.write("📚 FAISS Semantic Search")
    st.write("🤖 Gemini RAG")

    st.divider()

    st.markdown("### System Status")

    st.success("Video Engine Ready")
    st.success("Vector Search Ready")

    st.divider()

    if st.button("🔄 New Investigation"):

        st.session_state.processed = False
        st.session_state.video_folder = None
        st.session_state.answer = None
        st.session_state.upload_id = None
        st.session_state.video_filename = None

        st.rerun()

    st.caption("AI Scene Investigator | BCA AI & ML")


# HERO SECTION
st.markdown("""
<div class="hero">
    <h1>🎥 AI Scene Investigator</h1>
    <p>
        Understand videos using Computer Vision,
        Deep Learning and Retrieval-Augmented Generation.
    </p>
</div>
""", unsafe_allow_html=True)


# VIDEO UPLOAD
st.markdown(
    '<div class="section-title">📁 Upload Your Video</div>',
    unsafe_allow_html=True
)

uploaded_video = st.file_uploader(
    "Choose a video to investigate",
    type=["mp4", "avi", "mov", "mkv"]
)


if uploaded_video is not None:

    upload_id = uploaded_video.name + str(uploaded_video.size)

    if st.session_state.get("upload_id") != upload_id:

        st.session_state.upload_id = upload_id
        st.session_state.processed = False
        st.session_state.video_folder = None
        st.session_state.answer = None
        st.session_state.video_filename = uploaded_video.name

    col1, col2 = st.columns([1.5, 1])

    with col1:

        st.markdown("### 🎬 Video Preview")

        st.video(uploaded_video.getvalue())

    with col2:

        st.markdown("### 📄 Video Information")

        st.write("**Filename:**", uploaded_video.name)

        st.write(
            "**File size:**",
            round(uploaded_video.size / (1024 * 1024), 2),
            "MB"
        )

        st.write("**Status:** Ready for analysis")

        st.write("**Supported:** MP4, AVI, MOV, MKV")

        if st.button("🚀 Process Video"):

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

                with st.spinner(
                    "Analyzing video... Please wait."
                ):

                    from modules.video_pipeline import process_video_pipeline

                    video_id = process_video_pipeline(video_path)

                if video_id:

                    st.session_state.video_folder = os.path.join(
                        "outputs",
                        video_id
                    )

                    st.session_state.processed = True
                    st.session_state.answer = None

                    st.success(
                        "Video analysis completed successfully!"
                    )

                    st.rerun()

                else:

                    st.error("Video processing failed.")

            except Exception as e:

                st.error("An error occurred during processing.")
                st.exception(e)


# ANALYSIS SECTION
if st.session_state.get("processed", False):

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

        object_counts = {}

        for event in events:

            for name, count in event.get("objects", {}).items():

                object_counts[name] = (
                    object_counts.get(name, 0) + count
                )

        total_detections = sum(object_counts.values())

        # ANALYTICS
        st.divider()

        st.markdown(
            '<div class="section-title">📊 Video Analytics</div>',
            unsafe_allow_html=True
        )

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Observations", len(events))

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

        # OBJECT DETECTION
        st.markdown(
            '<div class="section-title">🔍 Detected Objects</div>',
            unsafe_allow_html=True
        )

        if object_counts:

            columns = st.columns(min(len(object_counts), 4))

            for i, (name, count) in enumerate(object_counts.items()):

                with columns[i % len(columns)]:

                    st.metric(name.title(), count)

            st.markdown("### 📈 Object Detection Statistics")

            st.bar_chart(
                object_counts,
                horizontal=True
            )

        else:

            st.info("No objects were detected in the sampled frames.")

        # EVENT TIMELINE
        st.divider()

        st.markdown(
            '<div class="section-title">⏱️ Event Timeline</div>',
            unsafe_allow_html=True
        )

        search_event = st.text_input(
            "🔎 Search scene observations",
            placeholder="Search for person, car, road, etc."
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

                st.write(
                    "**Scene:**",
                    event.get("description", "No description available")
                )

                st.write(
                    "**Detected objects:**",
                    event.get("objects", {})
                )

        # AI QUESTION ANSWERING
        st.divider()

        st.markdown(
            '<div class="section-title">🤖 Ask AI About Your Video</div>',
            unsafe_allow_html=True
        )

        with st.form("question_form"):

            question = st.text_input(
                "Ask anything about the video",
                placeholder="Example: Describe what is happening..."
            )

            submitted = st.form_submit_button(
                "✨ Generate AI Answer"
            )

        if submitted:

            if question.strip():

                try:

                    with st.spinner(
                        "Searching video evidence and generating answer..."
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

        # DISPLAY ANSWER
        if st.session_state.get("answer"):

            st.markdown("### 💬 AI Response")

            st.markdown(st.session_state.answer)

        else:

            st.info(
                "Ask a question above to generate an AI investigation response."
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
                label="📄 Download PDF Report",
                data=pdf_data,
                file_name="AI_Investigation_Report.pdf",
                mime="application/pdf",
                use_container_width=True
            )

        except Exception as e:

            st.error("Unable to create the PDF report.")
            st.exception(e)

    else:

        st.error("Events file not found. Please process the video again.")

else:

    st.info(
        "Upload a video above and click Process Video to begin your investigation."
    )


# FOOTER
st.divider()

st.caption(
    "AI Scene Investigator | Computer Vision + NLP + RAG"
)
