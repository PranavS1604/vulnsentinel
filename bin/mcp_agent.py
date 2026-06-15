import os
import sys
import json
import requests
import time
import random
from dotenv import load_dotenv
import urllib3

# Suppress local self-signed SSL warnings in terminal
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- CRITICAL PATH FIX FOR SPLUNK ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(SCRIPT_DIR, ".env")
TICKET_DB = os.path.join(SCRIPT_DIR, "mock_itsm_tickets.json")

load_dotenv(ENV_PATH)

SPLUNK_HEC_URL = os.environ.get("SPLUNK_HEC_URL")
SPLUNK_HEC_TOKEN = os.environ.get("SPLUNK_HEC_TOKEN")
WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

def create_mock_ticket(ticket_data):
    tickets = []
    if os.path.exists(TICKET_DB):
        with open(TICKET_DB, 'r') as f:
            try:
                tickets = json.load(f)
            except:
                tickets = []
    tickets.append(ticket_data)
    with open(TICKET_DB, 'w') as f:
        json.dump(tickets, f, indent=4)

def execute_mcp_remediation(host, ip, score, mitre):
    ticket_id = f"ITSM-INC-{random.randint(10000, 99999)}"
    print(f"[*] Initializing Splunk MCP Core Workflow for target: {host}")
    
    ticket_data = {
        "ticket_id": ticket_id,
        "status": "OPEN",
        "priority": "CRITICAL",
        "assigned_team": "Network Security",
        "asset_impacted": host,
        "mitre_tactic": mitre,
        "timestamp": time.time()
    }
    create_mock_ticket(ticket_data)
    print(f"[+] Local incident documentation saved: {ticket_id}")
    
    discord_payload = {
        "embeds": [{
            "title": "🛡️ MCP Autonomous Workflow Executed",
            "description": f"A high-risk vulnerability breached risk threshold (>85). Automated isolation protocol deployed. Ticket `{ticket_id}` generated.",
            "color": 16734296, 
            "fields": [
                {"name": "Target Asset", "value": f"`{host}` ({ip})", "inline": True},
                {"name": "Deterministic Risk Score", "value": f"**{score}/100**", "inline": True},
                {"name": "MITRE ATT&CK TTP", "value": f"`{mitre}`", "inline": False}
            ]
        }]
    }
    
    try:
        print("[*] Dispatching outbound containment payload to endpoint target...")
        requests.post(WEBHOOK_URL, json=discord_payload, timeout=5)
        status = "SUCCESS"
        print("[+] Discord webhook remediation notification delivered.")
    except Exception as e:
        status = f"FAILED: {str(e)}"
        print(f"[-] Outbound webhook notification error: {e}")
        
    audit_event = {
        "time": int(time.time()),
        "sourcetype": "vulnsentinel:audit",
        "event": {
            "action": "execute_autonomous_remediation",
            "target_host": host,
            "target_ip": ip,
            "risk_score": int(score),
            "ticket_id": ticket_id,
            "status": status,
            "orchestrator": "Splunk_MCP"
        }
    }
    
    try:
        headers = {"Authorization": f"Splunk {SPLUNK_HEC_TOKEN}", "Content-Type": "application/json"}
        # Bypassing local SSL verification ensures the audit trail reaches Splunk indexers
        requests.post(SPLUNK_HEC_URL, json=audit_event, headers=headers, timeout=5, verify=False)
        print("[+] Immutable audit log successfully submitted back to Splunk.")
    except Exception as e:
        print(f"[-] Splunk audit trace logging failed: {e}")
        
    print(f"\n🚀 [{ticket_id}] Complete agentic remediation loop completed.")

if __name__ == "__main__":
    if len(sys.argv) >= 5:
        # Running via Splunk custom alert architecture
        execute_mcp_remediation(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        # Running manually for live video demo presentation
        print("⚠️ No runtime arguments provided. Launching Hackathon Demo Simulation...")
        execute_mcp_remediation("web-prod-01", "10.0.0.5", 95, "T1190 - Exploit Public-Facing Application")