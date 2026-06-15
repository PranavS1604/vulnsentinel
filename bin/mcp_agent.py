import os
import sys
import json
import requests
import time
import random
from dotenv import load_dotenv

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
            tickets = json.load(f)
    tickets.append(ticket_data)
    with open(TICKET_DB, 'w') as f:
        json.dump(tickets, f, indent=4)

def execute_mcp_remediation(host, ip, score, mitre):
    ticket_id = f"ITSM-INC-{random.randint(10000, 99999)}"
    
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
    
    discord_payload = {
        "embeds": [{
            "title": "🛡️ MCP Autonomous Workflow Executed",
            "description": f"A high-risk vulnerability triggered an automated isolation protocol. Ticket `{ticket_id}` generated.",
            "color": 16734296, 
            "fields": [
                {"name": "Target Asset", "value": f"`{host}` ({ip})", "inline": True},
                {"name": "Deterministic Risk", "value": f"**{score}/100**", "inline": True},
                {"name": "MITRE TTP", "value": f"{mitre}", "inline": False}
            ]
        }]
    }
    
    try:
        requests.post(WEBHOOK_URL, json=discord_payload, timeout=5)
        status = "SUCCESS"
    except Exception as e:
        status = f"FAILED: {str(e)}"
        
    audit_event = {
        "time": int(time.time()),
        "sourcetype": "vulnsentinel:audit",
        "event": {
            "action": "execute_autonomous_remediation",
            "target_host": host,
            "target_ip": ip,
            "risk_score": score,
            "ticket_id": ticket_id,
            "status": status,
            "orchestrator": "Splunk_MCP"
        }
    }
    
    headers = {"Authorization": f"Splunk {SPLUNK_HEC_TOKEN}", "Content-Type": "application/json"}
    requests.post(SPLUNK_HEC_URL, json=audit_event, headers=headers, timeout=5)
    print(f"[{ticket_id}] MCP workflow completed.")

if __name__ == "__main__":
    if len(sys.argv) >= 5:
        execute_mcp_remediation(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])