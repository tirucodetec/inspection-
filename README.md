# 🔍 InspectAI --- AI-Powered Image Inspection

InspectAI is an AI-powered image inspection and problem-identification
application. Users can upload an image and ask questions about it. The
AI analyzes visible details and returns a text-based inspection summary
highlighting possible damage, defects, or unusual features.

> **Important:** InspectAI provides visual observations, not a certified
> professional inspection. Hidden damage and uncertain findings should
> be verified by a qualified person.

## ✨ Features

-   📸 Upload images in JPG, JPEG, or PNG format
-   🔍 Analyze images for visible damage, defects, and unusual features
-   📝 Generate clear, conversational inspection summaries
-   💬 Ask questions about an uploaded image
-   ⚠️ Explain possible concerns and suggest next steps when supported
    by the image
-   ✅ State when no obvious visible issue is identified instead of
    inventing defects
-   🧠 Uses a Gemini vision-capable model to interpret image input

## 🧰 Tech Stack

-   **Python** --- application logic
-   **Streamlit** --- chat interface and image upload
-   **Google Gemini API** --- image understanding and response
    generation

## 📁 Project Structure

A typical project structure may look like this:

``` text
inspection-/
├── app.py              # Streamlit application
├── requirements.txt    # Python dependencies
├── .env                # API key (keep private; do not commit)
├── .gitignore
└── README.md
```

Your actual filenames may differ. Update this section to match the files
in your repository.

## 🚀 Getting Started

### 1. Clone the repository

``` bash
git clone https://github.com/tirucodetec/inspection-.git
cd inspection-
```

### 2. Create and activate a virtual environment (recommended)

**Windows**

``` bash
python -m venv .venv
.venv\Scripts\activate
```

**macOS / Linux**

``` bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

If the repository contains `requirements.txt`, run:

``` bash
pip install -r requirements.txt
```

If you have not created the dependency file yet, the core packages for a
Streamlit app using the Google Gen AI SDK are typically:

``` bash
pip install streamlit google-genai python-dotenv
```

Make sure the installed SDK matches the imports used in your source
code.

### 4. Configure your Gemini API key

Create an API key through Google AI Studio, then store it as an
environment variable. For example, create a `.env` file in the project
root:

``` env
GEMINI_API_KEY=your_api_key_here
```

Load the key in Python using your chosen environment-variable method.
Never publish your real API key, place it in frontend code, or commit
the `.env` file to GitHub.

If your code expects a different environment-variable name, use that
exact name consistently.

### 5. Run the application

If your Streamlit entry file is `app.py`, run:

``` bash
streamlit run app.py
```

Streamlit will show a local URL in the terminal. Open it in your
browser.

## 🧪 How to Test InspectAI

Try uploading clear images of:

1.  🚗 A car with a small dent or scratch
2.  💡 A damaged or cracked headlight
3.  📦 A crushed cardboard parcel
4.  📦 A torn package
5.  ⚙️ A rusty machine component
6.  📱 A phone with a cracked screen
7.  🧱 A wall with a visible crack
8.  🚘 An apparently undamaged car
9.  📦 An intact parcel
10. 🌫️ A blurry or poorly lit image

Check whether the AI: - Describes what is visible - Identifies the
location of any apparent problem - Separates visible observations from
possible causes - Acknowledges uncertainty when the image is unclear -
Avoids inventing damage in normal images

## 🛡️ Responsible Use

-   AI results are estimates based on the image provided.
-   A photograph may not reveal hidden, internal, or safety-critical
    defects.
-   Image quality, lighting, angle, and occlusion can affect results.
-   Do not treat the output as a substitute for a qualified mechanic,
    engineer, or other relevant professional.
-   Avoid uploading sensitive personal information or images without
    permission.

## 🔐 Security

Ensure `.env` is listed in `.gitignore`:

``` gitignore
.env
.venv/
__pycache__/
*.pyc
.streamlit/secrets.toml
```

If an API key is accidentally committed, revoke it and create a
replacement.

## 🗺️ Future Improvements

-   🖍️ Highlight suspected problem areas on the image
-   📊 Add a dashboard for findings and severity labels
-   🗂️ Save inspection history
-   📄 Export reports as PDF
-   📱 Add WhatsApp sharing
-   🔄 Compare before-and-after images
-   🧪 Build a labeled test dataset and evaluate false positives and
    missed defects

## 🤝 Contributing

Suggestions, bug reports, and improvements are welcome. Test changes
with both damaged and undamaged images so that the app is checked for
false alarms as well as missed issues.

## 📄 License

No license has been specified here. Add a `LICENSE` file and update this
section if you choose to publish the project under a particular license.
