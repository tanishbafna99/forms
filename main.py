import json
import os
import re
import time  # ← you missed this earlier
from sentence_transformers import SentenceTransformer, util
from difflib import SequenceMatcher
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


def load_profiles():
    """Load or create local profile JSON"""
    profiles_dir = "profiles"
    os.makedirs(profiles_dir, exist_ok=True)
    profiles = [f for f in os.listdir(profiles_dir) if f.endswith(".json")]

    if not profiles:
        sample = {
            "Full Name": "Tanish Bafna",
            "Email": "tanishbafna@gmail.com",
            "Phone Number": "9876543210",
            "Address": "Pune, Maharashtra",
            "Occupation": "Computer Engineer",
            "Age": "22"
        }
        with open(os.path.join(profiles_dir, "personal.json"), "w") as f:
            json.dump(sample, f, indent=2)
        profiles.append("personal.json")

    print("Available Profiles:")
    for i, p in enumerate(profiles, 1):
        print(f"{i}. {p}")

    choice = int(input("\nSelect profile number to use: "))
    profile_name = profiles[choice - 1]
    with open(os.path.join(profiles_dir, profile_name)) as f:
        data = json.load(f)

    print(f"\n✅ Loaded profile: {profile_name}")
    print(json.dumps(data, indent=2))
    return data


def fuzzy_match(a, b):
    """Return similarity ratio between two strings"""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def match_label_to_value(label_text, profile_data):
    """Use AI/NLP to find best match for a form label in user profile"""
    model = SentenceTransformer("all-MiniLM-L6-v2")
    keys = list(profile_data.keys())
    label_emb = model.encode(label_text, convert_to_tensor=True)
    key_emb = model.encode(keys, convert_to_tensor=True)
    similarities = util.cos_sim(label_emb, key_emb)[0]
    best_idx = similarities.argmax().item()
    if similarities[best_idx] > 0.45:  # confidence threshold
        return profile_data[keys[best_idx]]
    return None

def fill_google_form(profile):
    """Open a Google Form and auto-fill fields with NLP mapping"""
    form_url = input("\nEnter the Google Form URL: ").strip()
    print("\n🔍 Opening form in Chrome...")

    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(form_url)

    wait = WebDriverWait(driver, 15)
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "form")))

    print("🔍 Scanning for form fields...")
    # detect both div[role=textbox] and <input>/<textarea>
    fields = driver.find_elements(By.XPATH, "//div[@role='textbox'] | //input | //textarea")
    print(f"🧾 Detected {len(fields)} potential input fields.")

    filled_count = 0
    model = SentenceTransformer("all-MiniLM-L6-v2")
    profile_keys = list(profile.keys())
    key_embeddings = model.encode(profile_keys, convert_to_tensor=True)

    for idx, field in enumerate(fields):
        # try to get label/question text
        label_text = ""
        try:
            label_elem = field.find_element(By.XPATH, ".//preceding::div[@role='heading'][1]")
            label_text = label_elem.text.strip()
        except:
            try:
                label_elem = field.find_element(By.XPATH, ".//ancestor::div[contains(@class,'Qr7Oae')]/preceding-sibling::div//span")
                label_text = label_elem.text.strip()
            except:
                pass

        if not label_text:
            label_text = "Unknown"

        # semantic match using embeddings
        label_emb = model.encode(label_text, convert_to_tensor=True)
        similarities = util.cos_sim(label_emb, key_embeddings)[0]
        best_idx = similarities.argmax().item()
        best_key = profile_keys[best_idx]
        best_value = profile[best_key]
        confidence = similarities[best_idx].item()

        if confidence > 0.45:
            try:
                driver.execute_script("arguments[0].scrollIntoView(true);", field)
                time.sleep(0.2)
                driver.execute_script("""
                    if(arguments[0].tagName === 'DIV') {
                        arguments[0].innerText = arguments[1];
                    } else if(arguments[0].tagName === 'INPUT' || arguments[0].tagName === 'TEXTAREA') {
                        arguments[0].value = arguments[1];
                        arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
                    }
                """, field, best_value)
                print(f"✅ '{label_text}' matched → {best_key} = {best_value}")
                filled_count += 1
            except Exception as e:
                print(f"⚠️ Could not fill '{label_text}': {e}")
        else:
            print(f"⚠️ No confident match for '{label_text}'")

    print(f"\n✅ Filled {filled_count}/{len(fields)} fields.")
    print("Please review before submitting manually.")
    input("Press Enter to exit...")
    driver.quit()




if __name__ == "__main__":
    profile_data = load_profiles()
    fill_google_form(profile_data)

