# 🗺️ VulnSentinel System Architecture Diagram

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