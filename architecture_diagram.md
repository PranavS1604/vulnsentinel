# 🗺️ VulnSentinel System Architecture Diagram

### 1. Diagram 1: The Refined Technical View 


```mermaid
graph TD
    subgraph Layer1 [Layer 1: Threat Intelligence]
        A[CISA KEV / NVD Feeds]
    end

    subgraph Layer2 [Layer 2: AI Reasoning & Splunk Core]
        B[Stateful Python Ingestor]
        E{fdtn-ai/Foundation-Sec-1.1-8B-Instruct}
        C[(Splunk Main Index & Asset Correlation)]
        D[Deterministic Risk Engine: CVSS + Context]
    end

    subgraph Layer3 [Layer 3: Agentic Response]
        F[🤖 Splunk MCP Agent]
        G[Network Isolation Webhook]
        H[Local ITSM Ticket DB]
    end

    subgraph Layer4 [Layer 4: Business Outcomes]
        I[VulnSentinel Command Dashboard]
        J[📉 Enterprise Risk Reduction Yield %]
    end

    A -->|Polls Data| B
    B -->|Sends Raw Text| E
    E -->|CTI-VSP: Predicts CVSS & MITRE| B
    B -->|HEC Token Post| C
    C -->|SPL Evaluation| D
    D -->|Risk > 85 Threshold| F
    F -->|Execute Remediation| G
    F -->|Generate Ticket| H
    F -->|Immutable Audit Log| C
    C -->|Realtime Metrics| I
    I -->|Executive Value| J

    classDef default fill:#1A2333,stroke:#4B5E78,color:#FFFFFF;
    classDef splunk fill:#241911,stroke:#FF7A00,stroke-width:2px,color:#FFFFFF;
    classDef ai fill:#22162B,stroke:#9333EA,stroke-width:3px,color:#FFFFFF;
    classDef mcp fill:#11251D,stroke:#10B981,stroke-width:3px,color:#FFFFFF;
    classDef value fill:#241911,stroke:#FF7A00,stroke-width:4px,color:#FFFFFF;

    class C,D,I splunk;
    class E ai;
    class F mcp;
    class J value;

```
### 2. Diagram 2: The Detailed closed-loop View 

This diagram maps out the closed-loop, data-driven agentic lifecycle of VulnSentinel. It displays the entire cycle from edge data discovery down to autonomous network isolation and dashboard business updates.

```mermaid
%%{init: {
  'theme': 'dark',
  'themeVariables': {
    'background': '#12161F',
    'primaryColor': '#1A2333',
    'primaryTextColor': '#FFFFFF',
    'primaryBorderColor': '#2A3B54',
    'lineColor': '#657D99',
    'secondaryColor': '#1F1A24',
    'tertiaryColor': '#152B24'
  }
}}%%
graph TD
    subgraph Ingestion [🌐 Global Threat Ingestion Layer]
        A[CISA KEV Public Feed] -->|Polls Live JSON Data| B(cve_ingestor.py Client)
        B -->|Deduplication Sync| C[(SQLite State DB)]
    end

    subgraph AI [🤖 AI Reasoning & Metric Prediction]
        B -->|Sends Raw CVE Text| D[Foundation-Sec-1.1-8B-Instruct]
        D -->|CTI-VSP Benchmark| E{Predict CVSS v3 & Map MITRE}
        E -->|Returns Structured JSON| B
    end

    subgraph Splunk [⚡ Splunk SIEM Processing Hub]
        B -->|HTTP Post Event| F[Splunk HTTP Event Collector HEC]
        F -->|Enriches via assets.csv| G[Splunk Core Processing Engine]
        G -->|Calculates Contextual Risk| H{Risk > 85 Threshold?}
    end

    subgraph Remediation [⚙️ Autonomous Remediation Agent Layer]
        H -->|Yes: Triggers Alert Action| I[Splunk MCP Agent Script]
        I -->|Outbound Webhook| J[Network Containment Firewall / Discord]
        I -->|Logs Immutable Case File| K[(mock_itsm_tickets.json)]
        I -->|Sends Remediation Audit Log| F
    end

    subgraph Metrics [📊 Executive Metrics Platform]
        G -->|Populates Realtime Metrics| L[VulnSentinel Command Center]
        K -->|Updates Recovery Progress| L
        L -->|Displays KPIs| M[Enterprise Risk Reduction Yield %]
    end

    %% Visual Styling Classes
    classDef intel fill:#1F2430,stroke:#4B5E78,stroke-width:1px,color:#E0E6ED;
    classDef engine fill:#1A2333,stroke:#3B82F6,stroke-width:1.5px,color:#FFFFFF;
    classDef splunk fill:#241911,stroke:#FF7A00,stroke-width:2px,color:#FFFFFF;
    classDef ai fill:#22162B,stroke:#9333EA,stroke-width:2.5px,color:#FFFFFF;
    classDef action fill:#11251D,stroke:#10B981,stroke-width:2.5px,color:#FFFFFF;
    classDef value fill:#241911,stroke:#FF7A00,stroke-width:4px,color:#FFFFFF;

    %% Node Assignments
    class A intel;
    class B,C engine;
    class D,E ai;
    class F,G,H,L splunk;
    class I,J,K action;
    class M value;

```

