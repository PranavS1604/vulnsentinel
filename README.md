# 🛡️ VulnSentinel
## Autonomous Vulnerability Discovery, Exposure Analysis & Remediation Agent for Splunk

**Splunk Agentic Ops Hackathon 2026 Submission**

VulnSentinel transforms vulnerability management from a manual, reactive process into an autonomous security workflow.

Instead of simply alerting security teams that a vulnerability exists, VulnSentinel continuously:

✅ Discovers newly exploited vulnerabilities

✅ Maps them against enterprise assets

✅ Calculates deterministic business risk

✅ Generates MITRE ATT&CK context

✅ Produces AI-driven remediation plans

✅ Triggers autonomous containment workflows

✅ Measures enterprise risk reduction

All natively inside Splunk Enterprise.

---

## 🎥 Demo Video

[![VulnSentinel Demo](https://img.shields.io/badge/▶%20Watch%20Demo-YouTube-red?style=for-the-badge&logo=youtube)](https://www.youtube.com/watch?v=YOUR_VIDEO_ID)

> **Judges:** The full end-to-end workflow — from CISA KEV ingestion to autonomous containment and risk reduction dashboard — is demonstrated in the video above.

---

## Why VulnSentinel?

Traditional vulnerability tools answer:

> "What vulnerabilities exist?"

VulnSentinel answers:

> "Which vulnerabilities affect MY organization, how dangerous are they, and what should we do right now?"

By combining real-time threat intelligence, asset context, deterministic risk scoring, and agentic AI workflows, VulnSentinel reduces the time between vulnerability disclosure and remediation from hours to seconds.

---

## Judge Summary

**Observe → Reason → Act**

VulnSentinel follows the core Agentic Operations paradigm:

### 👁️ Observe
- Ingests live CISA KEV intelligence
- Maintains enterprise asset awareness

### 🧠 Reason
- Calculates deterministic risk
- Maps MITRE ATT&CK techniques
- Generates remediation strategies using Foundation-Sec

### ⚡ Act
- Executes containment workflows
- Creates remediation tickets
- Produces immutable audit trails

### 📊 Measure
- Tracks exposure reduction
- Calculates enterprise risk reduction

---

## 🗺️ Architecture & Data Flow

Per hackathon requirements, the complete system architecture and MCP data flow diagram can be found in the root of this repository:

👉 [**View `architecture_diagram.md`**](./architecture_diagram.md)

VulnSentinel integrates threat intelligence, enterprise context, AI reasoning (Splunk Hosted Models), and autonomous remediation into a single closed-loop security workflow.

---

## Key Innovations

### 🔢 Deterministic Risk Engine

Unlike traditional tools that blindly surface raw CVSS scores, VulnSentinel calculates **Deterministic Contextual Risk** — a proprietary scoring model that translates technical vulnerabilities into measurable business exposure. See the [full methodology](#-risk-methodology--the-business-case) below.

### 🤖 Foundation-Sec Intelligence (Splunk Hosted Models)

Instead of relying on rate-limited, external NVD APIs for vulnerability severity, VulnSentinel leverages the **CTI-VSP (Vulnerability Score Prediction)** training of the `Foundation-Sec-1.1-8B-Instruct` model natively.

By passing the raw CISA threat description to the model via Splunk's API, the AI autonomously:
- Predicts the CVSS v3 Base Score directly from the text
- Classifies MITRE ATT&CK tactics
- Generates specific network remediation plans

### 🔄 Agentic Remediation

Through MCP-inspired workflows, VulnSentinel can:

- Trigger containment actions
- Generate remediation tickets
- Create immutable audit logs

### 📉 Enterprise Risk Reduction

Tracks measurable security outcomes rather than simply counting vulnerabilities.

---

## 📐 Risk Methodology — The Business Case

> **For judges with CISO or Director-level backgrounds:** This section explains why VulnSentinel produces business value that a standard alert pipeline cannot.

### The Problem with Standard CVSS

Most security tools alert on the raw CVSS score provided by the vendor. **CVSS exists in a vacuum.**

A server with a `9.8` CVSS score sitting safely behind three firewalls in a test lab is **not** the same risk as a `9.8` CVSS score on your public-facing customer database.

VulnSentinel fixes this by moving the conversation from:

| Standard Tools | VulnSentinel |
|---|---|
| "What vulnerabilities exist?" | "Which vulnerabilities threaten MY business right now?" |
| Technical severity (engineers) | Business risk (executives) |
| Raw CVSS score | Deterministic Contextual Risk Index |

---

### Phase 1 — Initial Risk Index (The "Before" State)

When a threat is ingested, Splunk SPL evaluates **four telemetry pillars** to generate a priority score capped at **100 points**:

| Pillar | Max Points | Logic |
|---|---|---|
| **Base Severity** | 50 pts | `CVSS × 5` — raw technical severity is exactly half the risk profile |
| **Environmental Exposure** | 20 pts | +20 if `is_internet_facing = true` — internet exposure drastically amplifies exploitability |
| **Business Criticality** | 20 pts | +20 if `High`, +10 if `Medium` — critical infrastructure is patched before internal wikis |
| **Threat Intel Exploitation** | 10 pts | +10 if CVE is on the CISA KEV list — adversaries are actively weaponizing it in the wild |

**Formula:**

```
Initial Risk = (CVSS × 5) + Exposure Score + Criticality Score + Exploitation Score
```

**Example — High-Risk Asset:**
```
CVE-2024-XXXX  |  CVSS: 9.8  |  Internet-Facing  |  High Criticality  |  CISA KEV: Yes

Initial Risk = (9.8 × 5) + 20 + 20 + 10 = 99 / 100
```

**Example — Low-Risk Asset (same CVE, different context):**
```
CVE-2024-XXXX  |  CVSS: 9.8  |  Internal Only  |  Low Criticality  |  CISA KEV: Yes

Initial Risk = (9.8 × 5) + 0 + 0 + 10 = 59 / 100
```

> Same CVE. Completely different business risk. CVSS alone cannot make this distinction.

---

### Phase 2 — Mitigated Risk Profile (The "After" State)

When the MCP Agent successfully executes a **network containment webhook**, the asset is logically isolated. It is no longer internet-facing, and adversaries can no longer reach it over the network.

The environmental modifiers therefore **drop to zero**. However, the vulnerability technically still exists on disk until a human applies the patch. To represent this residual risk mathematically, VulnSentinel applies a standard **60% suppression factor** to the base score:

```
Mitigated Risk = (CVSS × 5) × 0.4
```

**Example (same asset as above):**
```
Mitigated Risk = (9.8 × 5) × 0.4 = 19.6 / 100
```

---

### Phase 3 — Enterprise Risk Reduction (The Yield)

This is the **headline metric** displayed on the VulnSentinel dashboard. It calculates the exact percentage of business risk eliminated by the autonomous AI workflow:

```
Risk Reduction % = ((Initial Risk − Mitigated Risk) / Initial Risk) × 100
```

**Example (continued):**
```
Risk Reduction % = ((99 − 19.6) / 99) × 100 = 80.2% risk eliminated
```

This single number answers the question every CISO actually cares about:

> **"How much safer are we after this workflow ran?"**

---

### Why This Methodology Wins

| Property | Description |
|---|---|
| **Transparent** | Every point is traceable to a specific data source in Splunk |
| **Auditable** | No black-box AI scoring — math is fully reproducible |
| **Business-aligned** | Risk scores reflect asset value, not just vendor severity |
| **Measurable** | Before/after delta proves ROI of autonomous remediation |
| **Defensible** | Built on CVSS, CISA KEV, and CMDB — industry-standard data sources |

---

## 🔄 Example Workflow

1. CISA publishes a newly exploited vulnerability.
2. VulnSentinel's stateful agent ingests the raw threat description.
3. **AI Inference:** Foundation-Sec-1.1-8B analyzes the text, predicting the CVSS score and mapping the MITRE ATT&CK vector.
4. **Context Mapping:** Splunk maps the vulnerability to internal enterprise assets.
5. **Deterministic Math:** Splunk calculates the contextual Business Risk Score (0-100).
6. **Agentic Action:** If the risk breaches the critical threshold, the MCP agent initiates containment workflows (Discord Webhook/ITSM Ticket).
7. **Audit:** Immutable success events are written back into Splunk.
8. **Measurement:** The executive dashboard displays the updated Enterprise Risk Reduction Yield %.

---

## Business Impact

VulnSentinel helps organizations:

- Reduce vulnerability triage effort
- Prioritize remediation intelligently
- Improve incident response speed
- Maintain auditability
- Minimize exposure to actively exploited vulnerabilities

By focusing on risk reduction instead of alert volume, VulnSentinel enables security teams to spend less time investigating and more time remediating.

---

## Prerequisites

- Splunk Enterprise 9.x or later
- Python 3.9+
- Foundation-Sec-1.1-8B model access
- CISA KEV API access (free)

---

## Installation

```bash
# 1. Clone the repository
git clone https://github.com/your-org/vulnsentinel.git

# 2. Install dependencies into Splunk's Python
$SPLUNK_HOME/bin/splunk cmd python -m pip install requests python-dotenv

# 3. Configure environment
cp bin/.env.example bin/.env
# Edit .env with your HEC and Webhook tokens

# 4. Deploy to Splunk
mv vulnsentinel $SPLUNK_HOME/etc/apps/VULNSENTINEL
```

---

## ⚙️ Configuration (.env)

VulnSentinel uses a local `.env` file within the `bin/` directory to manage secrets securely without exposing them to version control.

| Variable | Description |
|---|---|
| `SPLUNK_HEC_URL` | Your Splunk HTTP Event Collector endpoint (e.g., `http://localhost:8088/services/collector`) |
| `SPLUNK_HEC_TOKEN` | Authentication token for the HEC input |
| `HF_API_TOKEN` | Token for Hugging Face to query the `Foundation-Sec` model |
| `DISCORD_WEBHOOK_URL` | Webhook endpoint for the autonomous containment simulation |
| `DEMO_MODE` | Set to `True` to bypass API sleep timers for rapid presentation displays |

---

## Tech Stack

| Component | Technology |
|---|---|
| SIEM Platform | Splunk Enterprise |
| Threat Intelligence | CISA Known Exploited Vulnerabilities (KEV) |
| AI Model | Foundation-Sec-1.1-8B |
| Threat Framework | MITRE ATT&CK |
| Agentic Workflow | MCP-inspired orchestration |
| Language | Python 3.9+ |

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

## Acknowledgements

- [CISA KEV Catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)
- [MITRE ATT&CK Framework](https://attack.mitre.org/)
- [Splunk Developer Platform](https://dev.splunk.com/)
- Foundation-Sec team for the cybersecurity-focused model