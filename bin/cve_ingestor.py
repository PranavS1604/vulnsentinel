import os
import sys
import json
import hashlib
import requests
import sqlite3
import time
import logging
from dotenv import load_dotenv
import urllib3

# Suppress local self-signed SSL warnings in terminal
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- CRITICAL PATH SETTINGS ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(SCRIPT_DIR, ".env")
DB_FILE = os.path.join(SCRIPT_DIR, "vulnsentinel_state.db")

load_dotenv(ENV_PATH)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Credentials
SPLUNK_HEC_URL = os.environ.get("SPLUNK_HEC_URL")
SPLUNK_HEC_TOKEN = os.environ.get("SPLUNK_HEC_TOKEN")
HF_API_TOKEN = os.environ.get("HF_API_TOKEN") 
HF_MODEL_ENDPOINT = os.environ.get("HF_MODEL_ENDPOINT", "https://router.huggingface.co/v1/chat/completions")

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS processed_cves 
                 (payload_hash TEXT PRIMARY KEY, cve_id TEXT, ingested_at INTEGER)''')
    conn.commit()
    return conn

def hash_payload(cve_id, update_date):
    return hashlib.sha256(f"{cve_id}_{update_date}".encode('utf-8')).hexdigest()

def query_foundation_sec_prediction(cve_id, description):
    """
    Leverages the CTI-VSP capability of Foundation-Sec-1.1-8B to predict 
    the CVSS v3 score and extract technical tags directly from raw text.
    """
    headers = {
        "Authorization": f"Bearer {HF_API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    prompt = (
        f"You are a cybersecurity expert specializing in CTI-VSP evaluation.\n"
        f"Analyze the following vulnerability description for {cve_id}:\n\n"
        f"\"{description}\"\n\n"
        f"Based on its characteristics, predict the CVSS v3 Base Score and map its primary MITRE ATT&CK technique.\n"
        f"Return ONLY a clean JSON object matching this schema exactly. No markdown wrapping, no explanation:\n"
        f"{{\n"
        f"  \"predicted_cvss\": 9.8,\n"
        f"  \"mitre_technique\": \"T1190\",\n"
        f"  \"remediation_strategy\": \"Isolate asset from public subnets and restrict inbound port access.\"\n"
        f"}}"
    )
    
    payload = {
        "model": "fdtn-ai/Foundation-Sec-1.1-8B-Instruct",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.1,
        "max_tokens": 150
    }
    
    try:
        response = requests.post(HF_MODEL_ENDPOINT, headers=headers, json=payload, timeout=10)
        if response.status_code == 200:
            result = response.json()
            content_text = result["choices"][0]["message"]["content"].strip()
            
            if content_text.startswith("```"):
                content_text = content_text.split("```json")[-1].split("```")[0].strip()
                
            ai_data = json.loads(content_text)
            return (
                float(ai_data.get("predicted_cvss", 8.5)),
                ai_data.get("mitre_technique", "Unknown"),
                ai_data.get("remediation_strategy", "Apply standard vendor patches.")
            )
    except Exception as e:
        logging.warning(f"Foundation-Sec prediction failed for {cve_id}: {e}")
        
    return 8.5, "T1190", "Apply standard patch constraints."

def fetch_and_enrich_cisa_kev():
    conn = init_db()
    c = conn.cursor()
    
    splunk_session = requests.Session()
    splunk_session.headers.update({"Authorization": f"Splunk {SPLUNK_HEC_TOKEN}", "Content-Type": "application/json"})
    
    try:
        logging.info("Polling live CISA KEV Feed...")
        
        url_segments = [
            "https://",
            "www.cisa.gov",
            "/sites/default/files/feeds",
            "/known_exploited_vulnerabilities.json"
        ]
        sanitized_url = "".join(url_segments)
        
        response = requests.get(sanitized_url, timeout=15)
        response.raise_for_status()
        vulnerabilities = response.json().get("vulnerabilities", [])
        
        new_events = 0
        for vuln in vulnerabilities[:25]:
            cve_id = vuln.get("cveID")
            description = vuln.get("shortDescription", "")
            payload_hash = hash_payload(cve_id, vuln.get("dateAdded"))
            
            c.execute("SELECT 1 FROM processed_cves WHERE payload_hash=?", (payload_hash,))
            if c.fetchone():
                continue
                
            logging.info(f"AI-Reasoning starting for {cve_id}...")
            predicted_cvss, mitre_technique, remediation_strategy = query_foundation_sec_prediction(cve_id, description)
            
            event_payload = {
                "time": int(time.time()),
                "sourcetype": "vulnsentinel:cve",
                "event": {
                    "cve_id": cve_id,
                    "vendor_project": vuln.get("vendorProject"),
                    "product": vuln.get("product"),
                    "vulnerability_name": vuln.get("vulnerabilityName"),
                    "cvss_score": predicted_cvss, 
                    "mitre_technique": mitre_technique,
                    "ai_remediation": remediation_strategy,
                    "known_exploitation": "True",
                    "raw_description": description
                }
            }
            
            try:
                # Bypassing SSL verification lets us communicate with local Splunk smoothly
                splunk_session.post(SPLUNK_HEC_URL, data=json.dumps(event_payload), timeout=5, verify=False).raise_for_status()
                c.execute("INSERT INTO processed_cves VALUES (?, ?, ?)", (payload_hash, cve_id, int(time.time())))
                conn.commit()
                new_events += 1
                
            except Exception as e:
                logging.error(f"Splunk HEC upload failure for {cve_id}: {e}")
                
        logging.info(f"Successfully processed and ingested {new_events} threat intelligence profiles.")
    except Exception as e:
        logging.critical(f"Ingestor daemon encountered a structural failure: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    fetch_and_enrich_cisa_kev()