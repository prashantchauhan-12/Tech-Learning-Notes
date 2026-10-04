# BigID – Data Security, Privacy & Governance Platform (Detailed Notes)

> **Source:** "R6 Show – Demo Day" transcript (`txt_file/bigId.txt`, ~57 min).
> **Speakers:** Dimitri Sirota (Co-founder & CEO, BigID), Chris Hosley (Director, Security Solution Engineering, BigID), Trey Ford (CISO, Bugcrowd – interviewer), Robert (host).
> **Note:** The video is a conversational demo (no CLI/config code). Code blocks in this file are **illustrative examples** I added to explain concepts (regex, IAM, API, SOAR, retention). They are *not* BigID's actual product code unless stated.

---

## Table of Contents
1. [What is BigID? (Quick Summary)](#1-what-is-bigid-quick-summary)
2. [Company Facts](#2-company-facts)
3. [Key Terminology / Glossary](#3-key-terminology--glossary)
4. [Platform Overview – The Big Picture](#4-platform-overview--the-big-picture)
5. [Step 1 – Discovery & Connectivity](#5-step-1--discovery--connectivity)
6. [Step 2 – Classification & Identification](#6-step-2--classification--identification)
7. [Entity-Based Data Model & Graph](#7-entity-based-data-model--graph)
8. [Use Case A – Breach Investigation (Reactive)](#8-use-case-a--breach-investigation-reactive)
9. [Use Case B – Prevention / Posture (Proactive)](#9-use-case-b--prevention--posture-proactive)
10. [Risk Prioritisation of Findings (Passwords example)](#10-risk-prioritisation-of-findings-passwords-example)
11. [Remediation, Retention & Deletion](#11-remediation-retention--deletion)
12. [Architecture & Deployment Models](#12-architecture--deployment-models)
13. [Security of BigID Itself ("master key" concern)](#13-security-of-bigid-itself-master-key-concern)
14. [Scan Types](#14-scan-types)
15. [MSP Support](#15-msp-support)
16. [AI / GenAI in BigID](#16-ai--genai-in-bigid)
17. [Differentiators vs Other Vendors](#17-differentiators-vs-other-vendors)
18. [Roadmap Mentioned](#18-roadmap-mentioned)
19. [Illustrative Code Examples](#19-illustrative-code-examples)
20. [Interview Q&A](#20-interview-qa)
21. [Revision Cheat Sheet](#21-revision-cheat-sheet)

---

## 1. What is BigID? (Quick Summary)

**BigID** = a **next-generation, AI-powered, cloud-native Data Security, Privacy, Compliance and Governance platform**.

It answers four questions about an organisation's data:

| Question | BigID capability |
|---|---|
| **Where** is my data? | Discovery across 160+ data sources |
| **What** is it? | Classification (PII, PCI, secrets, custom) |
| **Whose** is it? | Entity / identity correlation (graph) |
| **What do I do about it?** | Remediate, retain, delete, label, ticket, SOAR, access revoke |

Positioned in the **DSPM** (Data Security Posture Management) space, but the speakers say DSPM only covers *part* of what BigID does (also overlaps with **DLP**, **DAG – Data Access Governance**, privacy, AI data prep, insider risk).

---

## 2. Company Facts

- Started **selling in 2018**.
- ~**600 employees**, globally distributed (Miami, Wisconsin, Latin America, etc.).
- **Hundreds of customers**, mostly enterprise (Fortune 500 → Global 2000).
- Valuation **> $100M ARR** claim: *"both a unicorn and a centaur"* (unicorn = $1B valuation; centaur = $100M revenue).
- Awards: Cloud 100 (several years), Inc. 1000 (4 yrs), Deloitte Fast 500 (4 yrs).
- Won the **first data identification & classification competition** run by *Intuit* (the transcript says "it ran" – 20 DSPM & DLP vendors from Bay Area & Israel; BigID came out on top).
- ~**6–7 patents** on classification AI (graph, NLP, deep learning, random forest); later says **a dozen patents** for AI use overall.
- Certifications: **PCI, ISO 27001, SOC 2** (and others).
- Recognised by **Marsh** (insurance broker) – "Marsh Catalyst" – using BigID can lower cyber-insurance premiums.
- Contact: `bigid.com`, `info@bigid.com`, Twitter/X handle "secure bigid".

---

## 3. Key Terminology / Glossary

| Term | Meaning |
|---|---|
| **DSPM** | Data Security Posture Management – find & assess risky data in cloud/hybrid |
| **DLP** | Data Loss Prevention – older tech; fingerprint/regex based |
| **DAG** | Data Access Governance – who can access which data |
| **PII** | Personally Identifiable Information |
| **Structured / Semi / Unstructured** | DB tables / JSON, XML / docs, emails, chats |
| **Entity** | A real-world subject (person, customer) assembled from scattered attributes |
| **Referential integrity** | Keys that link tables (BigID graph follows these) |
| **Pseudonymization / Anonymization** | De-identifying records (mostly structured data) |
| **False positive / False negative** | Wrong hit / missed hit; BigID claims low rate of both (tunable) |
| **Scanner / Outpost** | Local component that reads data in customer environment |
| **Push-down** | Policy executed inside Snowflake / Databricks using their native engine |
| **SOAR** | Security Orchestration, Automation & Response (Palo Alto Cortex, Torq) |
| **PAM / Vault** | CyberArk, HashiCorp Vault, Delinea (Thycotic), BeyondTrust |
| **BYOC** | Bring Your Own Cloud (deploy into customer VPC) |
| **MSP** | Managed Service Provider |
| **Tombstoning** | Marking a record/file as deleted/archived without immediate physical removal |
| **ROT data** | Redundant, Obsolete, Trivial data |
| **RAG** | Retrieval-Augmented Generation (AI uses company data) |
| **Zero Trust** | "Trust but verify" – never implicitly trust identities/devices |
| **Tokenization / Obfuscation / Redaction** | Replace/hide sensitive values |

---

## 4. Platform Overview – The Big Picture

```mermaid
flowchart LR
    A[Data Sources<br/>Cloud / SaaS / On-Prem / Mainframe / Vector DB] --> B[Discovery]
    B --> C[Classification<br/>PII, PCI, Secrets, Custom]
    C --> D[Entity Correlation<br/>Graph]
    D --> E[Inventory / Catalog / Registry]
    E --> F1[Security<br/>Risk, Secrets, Access]
    E --> F2[Privacy<br/>DSAR, GDPR, CCPA]
    E --> F3[Governance<br/>Retention, Stewardship]
    E --> F4[AI Data Prep<br/>Curate, Cleanse, Govern]
    F1 --> G[Action:<br/>Ticket / SOAR / Revoke / Encrypt / Delete]
    F2 --> G
    F3 --> G
    F4 --> G
```

**Core idea:** *Discover → Classify → Understand (entities, risk) → Act.*

Value is **two lenses**:
1. **Reduce risk** (security, regulatory, compliance).
2. **Create value** (BI, personalisation, curated datasets for AI/RAG, LLM enrichment).

---

## 5. Step 1 – Discovery & Connectivity

**Goal:** automatically onboard *every* data source with minimal effort.

### 5.1 Cloud auto-discovery
- Connect to **AWS, Azure, GCP** (and NetApp ONTAP) with a **single account**.
- Uses **read-only service accounts**.
- From then on, every **new data repository** that spins up in these clouds is **automatically discovered**.

### 5.2 Vault / PAM integration
Credential storage integrations: **CyberArk, HashiCorp Vault, Delinea (Thycotic), BeyondTrust**. Privileges stay in the customer's vault and can be lifecycle-managed.

### 5.3 160+ additional data sources
- Structured, semi-structured, unstructured.
- Business apps, email, collaboration (Confluence, Jira, ServiceNow, Teams, SharePoint, OneDrive).
- Code repos (GitHub, GitLab).
- Data platforms (Snowflake, Databricks, S3).
- **Mainframes → Vector databases** (for AI).
- On-prem file shares (SMB), hybrid cloud, Dev Cloud.

```mermaid
flowchart TD
    S[Read-only Service Account / IAM Role] --> D{Discovery Engine}
    D --> P[Public Cloud: AWS / Azure / GCP]
    D --> SA[SaaS: M365, Salesforce, ServiceNow...]
    D --> DV[Dev: GitHub, GitLab, Jira, Confluence]
    D --> OP[On-Prem: SMB, NetApp, Mainframe, DBs]
    D --> AI[AI: Vector DBs, chatbots]
    D --> DP[Data Platforms: Snowflake, Databricks]
```

---

## 6. Step 2 – Classification & Identification

### 6.1 Why old DLP struggled
- DLP relied on **fingerprinting / patterns**.
- Easy for highly structured: credit card numbers, SSN, driver's licence, account numbers.
- Hard for context, custom IDs, documents, unstructured text.

### 6.2 Why LLMs alone are not the answer
- LLMs are **trained on public web scrapes** (Reddit, Twitter), *not* sensitive/commercial data.
- They don't inherently know requirements around many ID formats.
- **Large** → you must **copy data to the model** (customers don't want that).
- **Expensive and slow**; can't scan 100 PB (exfiltration cost is crazy).

### 6.3 BigID's approach: *mix of technologies*
| Task | AI/technique type |
|---|---|
| Watermarking code | one kind of AI |
| Strings of text / JSON | NLP-style |
| Classify a document (e.g., mortgage origination doc) | document classifier (deep learning) |
| Correlating attributes / identity | **Graph** |
| General | NLP, deep learning, **random forest** |

### 6.4 Tunability – the "onion" model
- **Easy button out of the box** (quick start).
- **Peel the onion**: tailor – add custom classifiers, exclude noise.
- Example: Zoom passcode (expired meeting → low value) vs privileged DB password or cloud service account (huge value). You tune accordingly.

### 6.5 Accuracy
- **Low false positives** (accuracy).
- Also **low false negatives** (find *everything*, e.g., every fragment that could be PII – *uniquely identifiable* or *textually identifiable*).
- Can use **positive and negative attribute logic**: "look for these 4 things **and** exclude that".

### 6.6 Attribute-level breakdown
BigID breaks data to **attribute level**, then re-assembles by **entity**. Customer-specific IDs (member ID, customer ID) are supported alongside standard compliance data.

### 6.7 Context-aware classification
Example from the talk: *"this is an IP address, but it's in proximity to a session key"* → higher meaning than a bare IP.

---

## 7. Entity-Based Data Model & Graph

**Key difference:** not "we lost 1M credit card numbers" but *"credit card numbers plus all data tied to the person who owns each card."*

- **Registry / inventory / catalog** built at **entity level**.
- Answer questions like:
  - "Everyone who lives in California" (one query).
  - "Everyone in California **who was part of this breach**" (very different, much more powerful).
- **Graph IP**: follows referential integrity, **score-ranks attributes**, connects attributes together at scale.
- Use cases: locate all data for **Dimitri Sirota** / a given customer (DSAR – Data Subject Access Request).
- **Combinations of attributes** logic → identify **toxic data combos** and **partially randomised / partially pseudonymised** data.

### Anonymization notes
- Pseudonymised/anonymised data usually applies to **structured** data (spreadsheets, DB, data warehouses for BI), not human-generated docs/emails.
- "If anonymisation is done correctly it should stay anonymised" – depends on the method.

```mermaid
flowchart LR
    A1[Name in CRM] --> G((Graph<br/>Correlation))
    A2[Email in Support Tickets] --> G
    A3[Card # in DB] --> G
    A4[Address in S3 CSV] --> G
    A5[Chat in Slack] --> G
    G --> E[Entity: Person X<br/>all locations + risk + residency]
```

---

## 8. Use Case A – Breach Investigation (Reactive)

**Scenario:** A breach happened. What was in scope?

```mermaid
flowchart TD
    B[Breach detected on Source X] --> I[Open BigID Inventory]
    I --> F[Filter / select the compromised data source]
    F --> V[See entity count, types, residency, risk]
    V --> X[Export via UI or API]
    X --> R[Impact analysis]
    R --> L[Legal / SEC materiality decision]
    R --> N[Notify affected individuals per state/country rules]
    V --> S[Check other places same data exists<br/>low-and-slow / land-and-expand]
```

**Demo highlights**
- Select e.g. an **old network file share** → **435,000 individual entities** reside there.
- Data can be **exported** or pulled via **APIs**.
- Shows where entities reside, number of records, level of risk.
- Checks **where else** the data lives (important for slow lateral-movement breaches).

**SEC angle:** Under new SEC rules, companies have **~4 days** to determine **materiality** of an incident. BigID gives the *"impact crater"* – what & whose data was taken – plus state-level breach regulations.

**Exact view not sample view:** BigID emphasises *exact* data inventory (not just an assessment) so you can piece together data lineage: which file server/data lake/bucket it came from, **who** and **which residency**.

---

## 9. Use Case B – Prevention / Posture (Proactive)

Customers use BigID **before** (prevention) and **after** (response). Typical prevention searches:

- **Loose credentials**: passwords, tokens, keys, secrets in repos.
- **Excessive / over-privileged access** (e.g., OneDrive/SharePoint over-sharing after migration).
- **Data crossing boundaries**, unusual access.
- Sensitive data in the wrong place.

### 9.1 Password example from demo
| Location | Verdict |
|---|---|
| SQL table (encrypted) | Expected place → fine, maybe check encryption |
| Confluence page | ❌ Why? |
| **Vector database** (AI) | ❌ Why? |
| Old SMB drive | ❌ Zero reason |
| Jira attachment / ServiceNow ticket / Teams chat / hardcoded in code | Common real-world leak spots |
| Backup | Often forgotten |

> "Probably **zero malicious intent** – it's just how data evolved across the corporate landscape."
> Classic cause: migration from home drives to OneDrive → easily shared with anyone.

### 9.2 Who leaks credentials
- **Support teams** – pass customer environment passwords via Teams.
- **Developers** – hardcode API keys / service accounts.

### 9.3 Action workflow

```mermaid
flowchart LR
    F[Finding:<br/>Password in Vector DB] --> T[Ticket<br/>ServiceNow / Jira]
    F --> SO[SOAR Playbook<br/>Palo Alto Cortex / Torq]
    F --> RV[Revoke / change permissions<br/>OneDrive, SharePoint]
    F --> RM[Remediate: move / encrypt / delete]
    F --> NT[Notify app owner<br/>decentralised]
```

- Context passed along: violation, recommended remediation steps, how it got there (ingestion process uncontrolled?), permissions.
- Everything works **via UI or API/automation**.

---

## 10. Risk Prioritisation of Findings (Passwords example)

How do you know how dangerous a given password is?

1. **Format / type** – privileged DB password vs service account for whole cloud vs Zoom passcode.
2. **Context** – how is it described (e.g., in a Confluence epic about app architecture).
3. **Location** – open S3 bucket shared with partners = high risk; private on-prem Bitbucket = lower; SaaS app protected only by customer password = medium.
4. **Environment variables** – exposure, who has access (developers hired/fired).
5. **Who owns it** → push to responsible team.

```mermaid
flowchart TD
    A[Secret found] --> B{Type?}
    B -->|Cloud admin / privileged DB| H[High severity]
    B -->|Expired meeting passcode| L[Low severity]
    H --> C{Location exposure?}
    C -->|Public / Partner bucket| CR[Critical]
    C -->|Private segmented repo| MD[Medium]
    CR --> D{Remediation model}
    MD --> D
    D -->|Central| SOC[SOC handles]
    D -->|Decentral| OWN[Push to App / Project owner + track]
```

**Both remediation models supported:** centralised (SOC) and decentralised (app owners, e.g., Confluence admin pushes to project teams) with **accountability tracking**.

---

## 11. Remediation, Retention & Deletion

### 11.1 Remediation options
- **Move** data.
- **Encrypt / obfuscate / tokenize** through integrations (Microsoft encryption suite, **Thales**, **Baffle**-type tools; the transcript names "Baffle/Thales"). Keys stay with the customer.
- **Delete** data (reduce attack surface).
- **Revoke access** (OneDrive, SharePoint).
- **Label** data (e.g., sensitivity labels).

### 11.2 Push-down in cloud
For **Snowflake** and **Databricks**, BigID pushes the policy down to use the platform's native capabilities.

### 11.3 Native capabilities (roadmap)
- **Redaction** and **tokenization** natively (early the following year).
- Full chain for **AI data cleansing**.

### 11.4 Retention & governance
Example thresholds from the talk:
| Rule | Retention |
|---|---|
| PCI-related | ~7 years (example) |
| GDPR beyond-specific regulation | ~10 years (example) |
| Customer from 1979 no longer exists in CRM | Delete **all** their records everywhere |

- Business users see records matching a retention schedule across **CRM, files, extracts, ticketing system**.
- Policies: **file destruction**, **ROT policy**, **tombstone**, **archive**.
- Example: stale `password.txt` → violates multiple policies → move/tombstone/archive/delete.

```mermaid
flowchart LR
    P[Retention Policy<br/>e.g. 7 yrs] --> Q[Query inventory:<br/>records older than policy]
    Q --> R[Review by data owner / business user]
    R --> A{Action}
    A --> T[Tombstone]
    A --> AR[Archive]
    A --> D[Delete everywhere<br/>by entity]
    A --> M[Move]
```

---

## 12. Architecture & Deployment Models

### 12.1 Core architecture
- **Containerised** platform; scales up/out.
- Can run **Kubernetes** *or* fully **cloud-native/serverless** (spun up when needed, spun down after).
- **No agents** installed on data systems.
- **Scanner / Outpost** placed **close to the data**; talks to each source via **native protocols** using **read-only** accounts.
- *Not* a web crawler ("we're not Google").

### 12.2 Deployment options (same product in all)

| Model | Description | Notes |
|---|---|---|
| **Multi-tenant SaaS** | Default; ~**90%** of customers | Regional SaaS in **28 countries** (e.g., Germany, Japan) |
| **Single-tenant cloud** | Fully isolated tenant; BigID manages backend | Small, "very inexpensive" premium |
| **BYOC – Bring Your Own Cloud** | Deploy into customer's VPC / private cloud | e.g., G42 (Saudi/UAE), Alibaba (China) |

```mermaid
flowchart LR
    subgraph Customer Environment
      DS[(Data Sources)] <-->|native protocol<br/>read-only| SC[Scanner / Outpost]
    end
    SC -->|Tokenized + salted metadata<br/>NO raw data| CP[BigID Control Plane<br/>SaaS / Single-tenant / BYOC]
    CP --> UI[UI / API / Integrations]
```

### 12.3 "GPS for your data"
- BigID stores a **map** (location), not the world.
- Location info is **tokenised and salted**; a bit of **encrypted metadata**.
- **Data itself never leaves** the organisation (privacy, data-processor reasons).
- UI shows "password present" – **not** the actual password.
- **Never makes a copy** of data. Doesn't lock or block users.

---

## 13. Security of BigID Itself ("master key" concern)

Trey's challenge: *"How do I sleep at night giving a partner the master key?"*

| Control | Detail |
|---|---|
| **Read-only by default** | Not required to write |
| **Vault segmentation** | Privileges stored in external vault, lifecycle-managed |
| **Narrow-scope permissions** | Avoids vendor getting admin rights |
| **AWS temporary IAM role** | Co-developed with **AWS** (patent filing) – BigID creates a **temporary account it itself has no direct access to**; proxy accounts block BigID from direct action |
| **Local scanning** | Data stays in customer environment |
| **Metadata only to cloud** | Tokenised, salted, encrypted |
| **Certifications** | PCI, ISO 27001, SOC 2 |
| **Fit for regulated industries** | Government, financial |

Zero-trust angle (separate question about geo conflict / untrusted machines): "**trust but verify**" – even approved identities (human, machine, LLM agent) should be monitored for unusual activity, policy violations, baseline deviations.

---

## 14. Scan Types

| Scan type | What it does | Pros | Cons |
|---|---|---|---|
| **Metadata / Assessment scan** | Finds a couple examples, then skips to next | Fast, contour view (yes/no) | Cannot compare sources |
| **Sample scan** | Samples portions | Compare & **prioritise** (e.g., 25,000 S3 buckets) | Not complete |
| **Full scan** | Reads everything | Complete picture (regulatory) | Slow, compute heavy |
| **Maintenance / Delta scan** | After baseline, only rescans **changed** schemas/files/folders | Very efficient, low compute | Needs baseline |

> BigID supports **all four** – start with contour, prioritise, then full scan only where needed.

```mermaid
flowchart LR
    M[Metadata/Assessment] --> S[Sample: prioritise]
    S --> F[Full scan on high-risk targets]
    F --> D[Delta / Maintenance scans<br/>only changes]
```

---

## 15. MSP Support

- BigID **has an MSP architecture** built natively since inception.
- Rolled out in peripheral regions: **Asia, Latin America** (Brazil/Argentina, ~20 people there, 100+ customers).
- Considering US rollout for commercial customers; **worldwide expected in 2025**.
- Multi-tenancy concept retained for MSP model.

---

## 16. AI / GenAI in BigID

### 16.1 Two roles of GenAI
1. **Inside BigID** (small/large language models, can be local):
   - Summarisation.
   - Extraction (tables, data owner).
   - Labelling by **business semantics** → **data glossary**, not just risk/sensitivity.
   - Part of the **AI co-pilot** strategy ("first in category").
   - *Not* used for mass scanning (too large/slow/expensive).
2. **Helping customers' GenAI journey:**
   - **Data categorisation** → curate datasets.
   - **Cleansing** → redaction & tokenization.
   - **Access management** at **prompt level** and **model level**.
   - Holistic risk (security + **legal** practitioner view → compliance, assessments).

### 16.2 AI-related risks highlighted
- Passwords found in **vector databases**.
- Old chatbot models from former developers lying around.
- Enriching a commercial LLM with company data needs prior **cleaning**.

```mermaid
flowchart LR
    RAW[Raw enterprise data] --> CL[Classify]
    CL --> CU[Curate dataset<br/>categorisation]
    CU --> CN[Cleanse<br/>redact / tokenize]
    CN --> AI[LLM / RAG / Fine-tune]
    AI --> AC[Prompt & model access control]
```

---

## 17. Differentiators vs Other Vendors

| Area | Typical vendor | BigID claim |
|---|---|---|
| **Coverage** | 1–2 sources; "3 S's" – **S3, Snowflake, SQL** | Everything: native & non-native public cloud, SaaS, Dev, on-prem, **mainframe** |
| **Data types** | Mostly one | Unstructured + structured, data at rest + in motion |
| **Classification** | "PII" yes/no | Drill to **exact type** with **context** |
| **Scan** | Assessment only | Assessment, sample, full, delta |
| **Location accuracy** | Cursory | **Exact location** (GPS metaphor) |
| **After finding** | Noise / overwhelm | **App platform** (like iPhone/Android apps) – snap-in "Lego-like" modules |
| **Modules** | – | Reporting, prioritisation, remediation, retention, deletion, regulatory reporting, data stewardship |
| **Audience** | Security only | Security + Privacy + Data governance |
| **Insurance** | – | Marsh recognition, brokers & insurers as customers |

**Biggest difference (said by CEO):** *what you do once you find the data – operationalising without being overwhelmed.*

---

## 18. Roadmap Mentioned
- Native **redaction** and **tokenization** (early next year).
- Expanded **AI co-pilot**.
- GenAI journey: categorisation, cleansing, prompt/model-level access.
- Compliance/legal assessment view.
- Worldwide **MSP** offering in **2025**.

---

## 19. Illustrative Code Examples

> ⚠️ Examples below are **conceptual**, written to help learning. Check BigID docs for the real API.

### 19.1 Regex-based DLP style detection (what old DLP did)
```python
import re

PATTERNS = {
    "credit_card": r"\b(?:\d[ -]*?){13,16}\b",
    "ssn_us": r"\b\d{3}-\d{2}-\d{4}\b",
    "aws_access_key": r"\bAKIA[0-9A-Z]{16}\b",
}

def scan(text):
    return {k: re.findall(p, text) for k, p in PATTERNS.items() if re.search(p, text)}

print(scan("key=AKIAABCDEFGHIJKLMNOP ssn=123-45-6789"))
```
**Limitation:** no context, many false positives (e.g., random 16 digits) → why BigID adds context + ML + graph.

### 19.2 Luhn check to cut credit-card false positives
```python
def luhn_ok(num: str) -> bool:
    digits = [int(d) for d in num if d.isdigit()][::-1]
    total = 0
    for i, d in enumerate(digits):
        if i % 2:
            d *= 2
            if d > 9: d -= 9
        total += d
    return total % 10 == 0
```

### 19.3 Attribute combination logic (positive + negative attributes)
```python
def is_customer_record(cols):
    positive = {"name", "email", "dob", "address"}
    negative = {"test_flag", "synthetic_id"}
    return len(positive & cols) >= 3 and not (negative & cols)
```

### 19.4 Read-only AWS IAM policy (principle of least privilege for a scanner)
```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Action": [
      "s3:ListAllMyBuckets",
      "s3:ListBucket",
      "s3:GetObject",
      "s3:GetBucketLocation",
      "rds:Describe*",
      "dynamodb:ListTables",
      "dynamodb:Describe*"
    ],
    "Resource": "*"
  }]
}
```

### 19.5 Cross-account role with ExternalId (temporary role pattern)
```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": { "AWS": "arn:aws:iam::<scanner-account-id>:role/scanner" },
    "Action": "sts:AssumeRole",
    "Condition": { "StringEquals": { "sts:ExternalId": "<unique-id>" } }
  }]
}
```
```bash
aws sts assume-role \
  --role-arn arn:aws:iam::111122223333:role/data-scan-readonly \
  --role-session-name scan-session \
  --external-id <unique-id> \
  --duration-seconds 3600
```

### 19.6 Tokenised + salted location metadata (concept)
```python
import hashlib, os
salt = os.urandom(16)
def token(value: str) -> str:
    return hashlib.sha256(salt + value.encode()).hexdigest()

finding = {
  "source": "s3://corp-share/hr/",
  "class": "password",
  "location_token": token("s3://corp-share/hr/creds.txt:line42"),
  # NOTE: the actual secret value is NEVER stored
}
```

### 19.7 Ticket creation for a finding (ServiceNow-style REST example)
```bash
curl -X POST "https://<instance>.service-now.com/api/now/table/incident" \
  -u "$SN_USER:$SN_PASS" \
  -H "Content-Type: application/json" \
  -d '{
    "short_description": "Password found in Confluence space ENG",
    "description": "Classifier: password | Source: confluence | Risk: High | Owner: eng-lead",
    "urgency": "1"
  }'
```

### 19.8 SOAR playbook (pseudo-YAML)
```yaml
playbook: bigid-secret-exposed
trigger: bigid.finding.created
conditions:
  - classifier in ["password","api_key","private_key"]
  - risk >= high
steps:
  - enrich: { fetch: [owner, permissions, location] }
  - ticket: { system: servicenow, priority: P1 }
  - if: location.is_public
    then:
      - revoke_access: { target: location }
  - notify: { channel: "#sec-ops" }
```

### 19.9 Retention policy evaluation (concept)
```python
from datetime import datetime, timedelta

POLICIES = {"pci": 7*365, "gdpr_marketing": 10*365}

def expired(record_date, policy):
    return datetime.utcnow() - record_date > timedelta(days=POLICIES[policy])

# delete by ENTITY: all records of that person across systems
def delete_entity(entity_id, locations):
    for loc in locations[entity_id]:
        print(f"Tombstone {loc}")
```

### 19.10 Generic REST pattern for exporting findings (illustrative)
```bash
curl -H "Authorization: Bearer $TOKEN" \
     "https://<bigid-host>/api/v1/<findings-or-catalog-endpoint>?filter=source:old-file-share" \
     -o breach_scope.json
```
*(Endpoint names are placeholders – see BigID API docs.)*

---

## 20. Interview Q&A

**Q1. What problem does BigID solve?**
It discovers, classifies, and correlates sensitive data across all environments, then enables action (remediate, retain, delete, govern) for security, privacy and AI.

**Q2. Is BigID an agent-based tool?**
No. A scanner/outpost uses native protocols with read-only accounts. Nothing installed on sources.

**Q3. Does BigID copy my data?**
No. Only tokenised, salted, encrypted metadata is sent to the control plane; the data stays local.

**Q4. Why not just use LLMs for classification?**
Large (need to copy data), expensive, slow, not pre-trained on sensitive/commercial formats. Used for summarisation/extraction/glossary instead.

**Q5. What are the deployment options?**
Multi-tenant SaaS (default, 28 countries), single-tenant cloud, BYOC.

**Q6. Difference between assessment, sample, full, delta scans?**
See [Scan Types](#14-scan-types).

**Q7. How does BigID help after a breach?**
Inventory per source → entity count, residency, risk → export/API → SEC materiality & breach notification.

**Q8. How does BigID reduce risk of its own privileged access?**
Read-only default, vault integration, narrow permissions, AWS-co-developed temporary roles, local scanning.

**Q9. What is entity-based inventory?**
Attributes stitched via graph into per-person records, enabling DSARs and impact analysis.

**Q10. How are findings prioritised?**
Type, context, location exposure, ownership, access.

**Q11. What integrations were mentioned?**
CyberArk, HashiCorp, Delinea, BeyondTrust; ServiceNow, Jira; Palo Alto Cortex, Torq (SOAR); Microsoft encryption, Thales, Baffle-type tools; Snowflake, Databricks (push-down); Confluence, GitHub, GitLab, OneDrive, SharePoint.

**Q12. How does BigID help with AI?**
Finds secrets in vector DBs, curates/cleanses datasets (redaction, tokenization), controls prompt/model access.

---

## 21. Revision Cheat Sheet

### One-liner
> **BigID = Discover → Classify → Correlate (entities) → Act**, without copying your data.

### Memory hooks
- **GPS for data** – a map, not the territory.
- **Onion** – start simple, peel for custom.
- **Before & After** – prevention + incident response.
- **Impact crater** – blast radius after a breach.
- **3 S's** – S3, Snowflake, SQL (what other vendors cover).
- **Lego apps** – modular snap-in app platform.

### Numbers to remember
| Item | Value |
|---|---|
| Selling since | 2018 |
| Employees | ~600 |
| Data sources | 160+ |
| Regional SaaS countries | 28 |
| Multi-tenant SaaS share | ~90% |
| Demo file share entities | 435,000 |
| SEC reporting window | ~4 days |
| Patents | 6–7 (classification) / a dozen (AI overall) |
| Certifications | PCI, ISO 27001, SOC 2 |

### Deployment cheat table
| Need | Choose |
|---|---|
| Default | Multi-tenant SaaS |
| Isolation, BigID-managed | Single-tenant |
| Full control / sovereignty | BYOC |
| No data haul-back | Local scanner / Outpost |

### Flow to recall
```mermaid
flowchart LR
    A[Connect<br/>read-only] --> B[Discover] --> C[Classify] --> D[Entity graph] --> E[Prioritise risk] --> F[Act:<br/>ticket / SOAR / encrypt / delete / revoke] --> G[Maintain:<br/>delta scans]
```

### Gotchas
- DSPM ≠ everything BigID does.
- Anonymisation mostly for **structured** data.
- "UI shows *password*" ≠ it stores the password.
- Native redaction/tokenization were **roadmap**, not GA at time of talk.
- MSP rollout US/worldwide = **planned 2025**.
- Some product/vendor names in the auto-generated transcript are garbled (e.g., "Intuit", "banic", "Talis", "tows"); verify against official docs.
