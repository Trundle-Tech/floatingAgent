# floatingAgent 🛡️

> **Autonomous AI security auditing, vulnerability scanning, and hardening agent for Google Cloud & Firebase web applications.** Built for the **Google Antigravity** agentic ecosystem.

[![Antigravity](https://img.shields.io/badge/Google-Antigravity%20Ready-0891b2.svg)](https://antigravity.google)
[![Firebase](https://img.shields.io/badge/Firebase-v10%2B%20Hardened-FFA000.svg)](https://firebase.google.com)
[![GitHub Repo](https://img.shields.io/badge/GitHub-Trundle--Tech%2FfloatingAgent-181717.svg?logo=github)](https://github.com/Trundle-Tech/floatingAgent)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

---

## ⚡ The Problem

Developers building fast on Firebase often deploy prototype shortcuts straight to production:
1. **Wildcard database rules (`allow read, write: if true;`)** that expose the entire database to anyone on the internet.
2. **Open Cloud Storage buckets** allowing unauthenticated users to download or overwrite private documents and files.
3. **Static bundle PII baking**, where build scripts accidentally inline production database records into publicly downloadable HTML/JS assets.
4. **Client-side fail-open auth traps** (`if (!auth) redirect()`) easily bypassed via curl, DevTools, or disabling JavaScript.
5. **Missing HTTP security headers** (CSP, `X-Frame-Options: SAMEORIGIN`, `nosniff`), leaving apps vulnerable to Clickjacking and MIME sniffing.

---

## 🚀 How It Works

The **Antigravity Security Agent** runs autonomously inside your Antigravity IDE or terminal:

```
┌────────────────────────────────────────────────────────────────────────┐
│                   ANTIGRAVITY SECURITY AGENT PIPELINE                  │
├────────────────────────────────────────────────────────────────────────┤
│ 1. RECON   : Scans .firebaserc, firebase.json, firestore.rules, storage│
│ 2. HEADERS : Audits live HTTP response headers (CSP, HSTS, SAMEORIGIN) │
│ 3. PII     : Scans public/ & dist/ bundles for leaked customer data    │
│ 4. RULES   : Eliminates wildcard allows & writes granular RBAC schemas │
│ 5. VERIFY  : Executes dry-run compile & verifies 100/100 security score│
└────────────────────────────────────────────────────────────────────────┘
```

---

## 📦 Quick Installation
 
### Option 1: Clone into any Antigravity Project
```bash
# Inside your project's root:
git clone https://github.com/Trundle-Tech/floatingAgent.git .agent/skills/security-agent
```

### Option 2: Machine-Wide Install (Available Across All Workspaces)
```bash
git clone https://github.com/Trundle-Tech/floatingAgent.git ~/.gemini/config/skills/security-agent
```

---

## 📋 The One-Shot Antigravity Prompt

When opening any project in **Google Antigravity**, paste this prompt:

```text
@security-agent

Run a full security vulnerability audit on my web application:
Target URL: [ENTER YOUR URL, e.g. https://my-app.web.app]

Audit Scope:
1. HTTP Security Headers: Content-Security-Policy, X-Frame-Options, X-Content-Type-Options: nosniff, Cache-Control.
2. Firestore Security Rules: Verify zero wildcard allow rules. Enforce collection-level RBAC & schema constraints.
3. Firebase Storage Rules: Audit bucket paths, enforce verified auth tokens, max file size & MIME type limits.
4. Client-Side Security: Red-team against client-side bypasses (window.location redirect traps).
5. Static Bundle PII Leaks: Scan public/ and dist/ to ensure zero customer, private, or database records are baked in.
6. Verification: Output a clean remediation report with 0 critical vulnerabilities.
```

---

## 🛠️ Standalone CLI Tools

The project includes standalone Python scripts you can run in your terminal anytime:

### 1. HTTP Security Headers Auditor
Audits live response headers for CSP, HSTS, X-Frame-Options, nosniff, and Cache-Control:
```bash
python3 scripts/audit_headers.py https://my-app.web.app
```

### 2. Static Bundle PII & Secret Scanner
Scans your `public/` or `dist/` directory for inlined private emails, exposed credentials, oversized payloads (>5MB), and dangerous DOM sinks:
```bash
python3 scripts/audit_bundle_pii.py public/
```

### 3. Rules Dry-Run Compiler
Validates rule syntax against the Firebase CLI without deploying:
```bash
bash scripts/test_rules.sh
```

---

## 📦 Project Structure

```
security-agent/
├── .agent/
│   └── skills/
│       └── security-agent/
│           └── SKILL.md         # Antigravity skill manifest
├── scripts/
│   ├── audit_headers.py         # Live HTTP security header checker
│   ├── audit_bundle_pii.py      # Static asset scanner for PII / secrets
│   └── test_rules.sh            # Dry-run compiler script
├── templates/
│   ├── firebase.json            # Hardened security headers config
│   ├── firestore.rules          # Granular RBAC & field validator template
│   └── storage.rules            # MIME-type & UID-restricted storage template
├── index.html                   # Standalone showcase & download portal
├── SKILL.md                     # Root skill definition
├── LICENSE                      # MIT License
└── README.md                    # Documentation
```

---

## 📄 License

MIT. Built with Google Antigravity.
