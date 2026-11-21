
# 🎥 AI Scene Investigator

### An AI-powered video analysis and investigation system

AI Scene Investigator is a Python-based application that analyzes uploaded videos using computer vision, object detection, scene understanding, and Retrieval-Augmented Generation (RAG).

Users can upload a video, explore detected events, search scene information, and ask questions about the video through an interactive Streamlit dashboard.

## 🚀 Features

- Video upload and preview
- Object detection using YOLOv8
- Object tracking using ByteTrack
- Scene description using BLIP
- Automatic event extraction with timestamps
- Semantic search using Sentence Transformers
- FAISS vector database for similarity search
- RAG-based question answering
- Gemini API integration with offline fallback
- Interactive analytics dashboard
- Searchable event timeline
- Downloadable PDF investigation reports

## 🛠️ Technologies Used

- Python
- Streamlit
- OpenCV
- YOLOv8
- ByteTrack
- BLIP
- Hugging Face Transformers
- Sentence Transformers
- FAISS
- Google Gemini API
- ReportLab

## ⚙️ Project Architecture

1. Video Upload
2. Frame Extraction using OpenCV
3. Object Detection using YOLOv8
4. Object Tracking using ByteTrack
5. Scene Analysis using BLIP
6. Event Extraction
7. Text Embedding Generation
8. FAISS Vector Storage
9. Semantic Retrieval
10. RAG-based Question Answering
11. PDF Report Generation

## 📂 Project Structure

```text
AI-Scene-Investigator/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── modules/
│   ├── video_processor.py
│   ├── object_detector.py
│   ├── object_tracker.py
│   ├── scene_analyzer.py
│   ├── event_extractor.py
│   ├── nlp_processor.py
│   ├── embedding_generator.py
│   ├── vector_store.py
│   ├── semantic_search.py
│   ├── rag_pipeline.py
│   ├── video_pipeline.py
│   └── llm_provider.py
│
└── .env.example
```

## 💻 Installation

Clone the repository:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd AI-Scene-Investigator
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure your Gemini API key in a `.env` file:

```env
GEMINI_API_KEY=your_api_key_here
LLM_PROVIDER=auto
```

Run the application:

```bash
streamlit run app.py
```

## 🧠 AI Question Answering

The application uses a hybrid approach:

- Gemini API for AI-generated answers.
- Python-based offline fallback when the API is unavailable.

This improves reliability when external AI services experience temporary failures.

## ⚠️ Limitations

- Analysis is based on sampled video frames.
- Very short events may be missed.
- Tracking IDs do not identify real individuals.
- AI answers depend on the extracted scene information.

## 👨‍💻 Developer

**Abhishek Gupta**

BCA – Artificial Intelligence and Machine Learning

## 📌 Project Status

Developed as an AI and Machine Learning project.
