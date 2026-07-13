# AI Flashcard Generator

🔗 **Live Demo:** [Click here to try the live web application!](https://ai-flashcard-generator-7imt.onrender.com)

The **AI Flashcard Generator** is a web app built to make studying a lot less painful. You simply upload a study PDF, pick how many flashcards you want, and the app uses Google's Generative AI to instantly turn that dense text into clean, bite-sized Q&A flashcards.

## Features

**File Uploads & Reading**
- You can easily drop your PDF directly onto the screen or click to upload it.
- You can type in exactly how many flashcards you want the AI to make.
- The app reads the raw text from your PDF quickly by ignoring all the heavy designs, colors, and complex layouts, keeping it lightweight.

**Creating the Flashcards**
- The AI will format everything into clear, direct questions and answers.
- It smart-checks your document to pull out the most important terms, math formulas, and main concepts so you don't miss anything.
- If something goes wrong on the server side (like an AI slowdown or a connection issue), the app catches the error quietly behind the scenes instead of freezing or throwing a messy page of code at you.


## Tech stack

| Layer | Choice |
|---|---|
| Core AI engine | Google GenAI SDK [`gemini-3.1-flash-lite`](https://ai.google.dev/gemini-api/docs/models/gemini#gemini-3.1-flash-lite) |
| Backend Framework | Python, Flask |
| PDF Parsing | [`pypdf`](https://pypi.org/project/pypdf/) (`PdfReader`) |
| Live Hosting | Render + Gunicorn |
| Frontend | Vanilla HTML + CSS (No massive JavaScript frameworks) |

### Why this stack

The app layout is intentionally built to stay completely inside free hosting constraints without losing performance.

Instead of using heavy, layout-focused parsing libraries like [`pdfplumber`](https://pypi.org/project/pdfplumber/) which load massive document font trees and instantly crash a strict 512MB RAM cloud container, I chose `pypdf`. It reads text directly as a raw stream, keeping memory flat.

For the AI orchestration, `gemini-3.1-flash-lite` was selected over `gemini-3.5-flash`. While the flagship model sounds better on paper, its public free tier suffers from intense global traffic spikes and caps users at 20 requests a day. The `lite` model bypasses these congestion roadblocks completely, speaks fluent JSON, and offers a massive ceiling of 1,000 free requests per day, making the app actually usable for continuous study sessions.

## Getting started

**Prerequisites**
- Python 3.x installed on your machine
- A free Gemini API key generated via Google AI Studio

**Run it**
```bash
git clone <this-repository-url>
cd AI-Flashcard-Generator
pip install -r requirements.txt
```
Set your API key variable in your terminal:

```bash
# Windows
set GEMINI_API_KEY="your_actual_key_here"

# Mac/Linux
export GEMINI_API_KEY="your_actual_key_here"
```

Start the development app:

```bash
python app.py
```


## How to use it

1. **Upload your file** — Click the file upload bubble and select your study guide or lecture PDF.
2. **Set your count** — Choose how many flashcards you want the AI to create.
3. **Generate** — Hit the generate button. The backend extracts the text, pushes it to the model pool, strips away hidden markdown formatting, and builds your interactive cards.


## Known limitations

- **Scanned Image PDFs** : The text extraction engine works entirely on digitally generated text layers. It doesn't use OCR, so it won't read handwritten notes or photographed documents.
- **English Language Only** : The application text processing pipeline and AI generation prompts are optimized strictly for English documents. Non-English PDFs may result in unpredictable formatting or mixed-language output.
- **Massive Textbooks** : Extremely large files (e.g., 50MB+ whole textbooks) will time out the request stream due to free cloud instance processing constraints.
- **Complex Multi-Column Tables** : Documents with dense nested tables or side-by-side text columns can sometimes have their sentence flow mixed up during raw stream extraction, which might slightly throw off the AI context.


*Disclaimer: This project is unlicensed and created solely for educational purposes.*
