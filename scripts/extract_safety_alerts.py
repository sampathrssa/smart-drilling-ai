import os
import re
import json
from datetime import datetime
from pdfminer.high_level import extract_text

RAW_ALERTS_DIR = "../data/raw_alerts"
OUTPUT_FILE = "../data/safety_alerts.json"

def extract_date(full_text):
    published_match = re.search(r'Published:\s*(\d{1,2}/\d{1,2}/\d{4})', full_text)
    if published_match:
        raw_date = published_match.group(1)
        try:
            parsed_date = datetime.strptime(raw_date, "%m/%d/%Y")
            return parsed_date.strftime("%Y-%m-%d")
        except Exception:
            pass

    md_match = re.search(r'([A-Z][a-z]+ \d{1,2}, \d{4})', full_text)
    if md_match:
        raw_date = md_match.group(1)
        try:
            parsed_date = datetime.strptime(raw_date, "%B %d, %Y")
            return parsed_date.strftime("%Y-%m-%d")
        except Exception:
            pass

    return None

def extract_data_from_pdf(filepath):
    record = {}
    try:
        full_text = extract_text(filepath)

        # Extract ID
        match_id = re.search(r'SA_(\d+)', filepath)
        record["id"] = int(match_id.group(1)) if match_id else None

        # Title (use first line)
        lines = full_text.splitlines()
        lines = [line.strip() for line in lines if line.strip()]
        record["title"] = lines[0] if lines else "Unknown Title"

        # Date extraction
        record["date"] = extract_date(full_text)

        # Description extraction
        if len(lines) > 1:
            description = "\n".join(lines[1:]).strip()
        else:
            description = ""

        record["description"] = description

    except Exception as e:
        print(f"Error processing {filepath}: {e}")
    return record

def process_all_alerts():
    records = []
    for file in os.listdir(RAW_ALERTS_DIR):
        if file.endswith(".pdf"):
            filepath = os.path.join(RAW_ALERTS_DIR, file)
            data = extract_data_from_pdf(filepath)
            if data:
                records.append(data)
    return records

if __name__ == "__main__":
    results = process_all_alerts()
    with open(OUTPUT_FILE, "w") as f:
        json.dump(results, f, indent=4)
    print(f"✅ Extracted {len(results)} safety alerts into {OUTPUT_FILE}")
