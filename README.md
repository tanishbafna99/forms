Google Form Auto-Filler (AI-Powered)

An intelligent automation script that automatically fills Google Forms using your pre-saved profile data.
It uses AI/NLP (Sentence Transformers) to semantically match form labels (like Full Name, Email, Contact, etc.) with your stored personal information — even if the labels are written differently (e.g., Your full name, Contact details, Mail ID).

🚀 Features

✅ Automatically opens any Google Form in Chrome
✅ Detects all input fields (<input>, <textarea>, div[role=textbox])
✅ Uses AI sentence embeddings to match form labels to your profile data
✅ Supports synonyms (e.g., Phone, Contact, Mobile Number)
✅ Works without any API keys
✅ User-friendly CLI prompts
✅ Editable profiles stored in JSON files

🧩 Tech Stack & Libraries
Library	Purpose
Selenium	Automates the browser to open and fill Google Forms
Sentence Transformers	Provides the AI model (all-MiniLM-L6-v2) for semantic text similarity
Webdriver Manager	Automatically manages and installs ChromeDriver
Difflib (SequenceMatcher)	Provides fuzzy text comparison (backup matching method)
JSON & OS	Used to manage and load saved user profiles
Time, Re	Timing and pattern handling for DOM operations
⚙️ How It Works

Profile Loading

The script looks for a profiles folder.

If it doesn’t exist, it creates one and adds a default file: personal.json.

Example structure:

{
  "Full Name": "Tanish Bafna",
  "Email": "tanishbafna@gmail.com",
  "Phone Number": "1234567890",
  "Address": "Pune, Maharashtra",
  "Occupation": "Computer Engineer",
  "Age": "22"
}


Form Analysis

Opens your Google Form in Chrome.

Finds all text input boxes, textareas, and div-based input fields.

AI Matching

Extracts the label text near each input field.

Compares the label’s meaning to your profile keys using embeddings.

Example:

Label: “Enter your contact number”

Best match: “Phone Number”

Value filled: “9876543210”

Form Filling

Fills detected fields with the matched profile values.

Reports matched and unmatched fields in the terminal.

🧠 AI Model Explanation

Model Used: all-MiniLM-L6-v2
This model comes from the Sentence Transformers
 library.
It converts sentences into embeddings (dense vector representations of meaning).

When the script encounters a field label like "Contact Info", it:

Converts "Contact Info" and "Phone Number" into vectors.

Calculates cosine similarity between the two.

Chooses the profile field with the highest similarity (>0.45 confidence threshold).

This means it recognizes semantic meaning, not just literal words.

🖥️ How to Run
1. Clone or Download the Project
git clone https://github.com/yourusername/google-form-autofill.git
cd google-form-autofill

2. Install Requirements
pip install -r requirements.txt


requirements.txt

selenium
sentence-transformers
webdriver-manager

3. Run the Script
python main.py

4. Follow the Prompts

Select your saved profile.

Paste your Google Form URL.

Wait for the AI to fill it automatically.

Review and submit manually.

🧾 Example Output
Available Profiles:
1. personal.json

✅ Loaded profile: personal.json
{
  "Full Name": "Tanish",
  "Email": "tanishbafna@gmail.com",
  "Phone Number": "9836436346436",
  "Address": " Maharashtra",
  "Occupation": "Computer Engineer",
  "Age": "2"
}

Enter the Google Form URL: https://forms.gle/example

🔍 Opening form in Chrome...
🔍 Scanning for form fields...
🧾 Detected 8 potential input fields.
✅ 'Enter your name' matched → Full Name = Tanish Bafna
✅ 'Contact Number' matched → Phone Number = 9876543210
⚠️ No confident match for 'Feedback'

✅ Filled 6/8 fields.
Please review before submitting manually.

🧰 Folder Structure
📂 GoogleFormAutoFiller
 ┣ 📂 profiles
 ┃ ┗ personal.json
 ┣ 📜 main.py
 ┣ 📜 requirements.txt
 ┗ 📜 README.md

🔐 Notes

Works best on Chrome browser.

Doesn’t require Google API or authentication.

Avoid forms with file uploads or dropdowns (not supported yet).

You can add multiple profiles in the profiles/ folder.

🧑‍💻 Author

Tanish Bafna
📧 tanishbafna@gmail.com

💼 Computer Engineer | Automation Enthusiast
