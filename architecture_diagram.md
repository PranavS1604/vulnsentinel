# 🗺️ VulnSentinel System Architecture Diagram

### 1. Diagram 1: The Detailed closed-loop View 

This diagram maps out the closed-loop, data-driven agentic lifecycle of VulnSentinel. It displays the entire cycle from edge data discovery down to autonomous network isolation and dashboard business updates.

```mermaid
graph TD
    subgraph Global Threat Ingestion Layer
        A[CISA KEV Feed Feed] -->|Polls Live JSON Data| B(cve_ingestor.py Worker)
        B -->|Deduplication Sync| C[(SQLite State DB)]
    end

    subgraph AI Reasoning & Metric Prediction Layer
        B -->|Sends Raw CVE text| D[Foundation-Sec-1.1-8B Model]
        D -->|CTI-VSP Benchmark Capability| E{Predict CVSS v3 & Map MITRE}
        E -->|Returns Structured Security Context JSON| B
    end

    subgraph Splunk SIEM Processing Hub
        B -->|HTTP Post Event| F[Splunk HTTP Event Collector HEC]
        F -->|Enriches via asset.csv Lookup Table| G[Splunk Core Processing Engine]
        G -->|Calculates Contextual Business Risk Score| H{Risk > 85 Threshold?}
    end

    subgraph Autonomous Remediation Agent Layer
        H -->|Yes: Triggers Alert Alert Action| I[mcp_agent.py Execution Script]
        I -->|Outbound Webhook Execution| J[Network Containment Firewall API / Discord]
        I -->|Logs Immutable Case File| K[(mock_itsm_tickets.json)]
        I -->|Sends Remediation Audit Log| F
    end

    subgraph Executive Metrics Platform
        G -->|Populates Realtime Metrics| L[VulnSentinel Command Center View]
        K -->|Updates Recovery Progress| L
        L -->|Displays KPIs| M[Enterprise Risk Reduction Yield %]
    end

    %% Visual Styling
    style A fill:#f9f,stroke:#333,stroke-width:2px
    style D fill:#bbf,stroke:#333,stroke-width:2px
    style G fill:#fbb,stroke:#333,stroke-width:2px
    style I fill:#bfb,stroke:#333,stroke-width:2px
    style M fill:#ffb,stroke:#333,stroke-width:4px

```

### 2. Diagram 2: The Refined Technical View 


## ⚙️ Technical Architecture & Data Flow

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