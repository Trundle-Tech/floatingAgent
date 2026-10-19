---
name: security-agent
description: >-
  Autonomous security auditing, vulnerability scanning, and remediation agent for
  Google Cloud and Firebase web applications. Inspects HTTP response headers (CSP,
  HSTS, X-Frame-Options, MIME nosniff), audits Cloud Firestore and Firebase Storage
  security rules for wildcard exploits, validates client-side authentication guards,
  and scans static assets for leaked private data or PII.
---

# Antigravity Security Agent 🛡️

Autonomous security auditor for Google Cloud & Firebase web applications.

## 🎯 Primary Purpose

When a developer asks to audit, harden, or scan their web application, the **Security Agent** runs a comprehensive, multi-phase assessment across:
1. **HTTP Security Headers:** CSP, HSTS, X-Frame-Options, X-Content-Type-Options: nosniff, Cache-Control.
2. **Cloud Firestore Rules:** Eliminates `allow read, write: if true;`, enforces RBAC, schema validations, and default deny-all.
3. **Firebase Storage Rules:** Audits bucket paths, enforces authenticated UID ownership, file size limits (<15MB), and MIME filters.
4. **Client-Side Auth Hardening:** Eliminates fail-open redirect traps (`if (!auth) redirect()`) and ensures server-side rules guard all data.
5. **Static Bundle PII Scanning:** Scans `public/` or `dist/` HTML/JS bundles to prevent inlined database records, leaked emails, or credentials.
6. **Automated Verification:** Runs dry-run syntax compilation and live curl exploits to ensure zero critical vulnerabilities remain.

---

## 🛠️ Step-by-Step Workflow

### Phase 1: Reconnaissance & Discovery
1. Check project root for `.firebaserc`, `firebase.json`, `firestore.rules`, and `storage.rules`.
2. Inspect the public build directory (e.g. `public/`, `dist/`, `build/`).
3. If a live target URL is provided (e.g. `https://my-app.web.app`), run the header auditor:
   ```bash
   python3 scripts/audit_headers.py <TARGET_URL>
   ```

### Phase 2: Static Bundle PII & Secret Audit
Run the automated bundle scanner:
```bash
python3 scripts/audit_bundle_pii.py <BUILD_DIR>
```
* **Flags:**
  - Raw email lists / candidate dossiers / customer records in static JS/HTML.
  - Inlined private keys or secrets.
  - Bundles over 5MB.
  - Dangerous DOM sinks (`innerHTML = userControlledData`).

### Phase 3: Firebase Rules Security Audit
Inspect `firestore.rules` and `storage.rules`:
* **CRITICAL FAIL:** Any `allow read, write: if true;` or catch-all wildcard read permissions.
* **CRITICAL FAIL:** Unauthenticated writes to collections.
* **HIGH RISK:** Missing schema/type validations on `create` or `update`.
* **HIGH RISK:** Missing file size or MIME type constraints on Storage uploads.

### Phase 4: Autonomous Remediation
1. **Update `firebase.json`:**
   Add strict security headers for all routes:
   - `Content-Security-Policy`: Restricts scripts and styles to trusted domains.
   - `X-Frame-Options`: `SAMEORIGIN` (prevents clickjacking).
   - `X-Content-Type-Options`: `nosniff`.
   - `Referrer-Policy`: `strict-origin-when-cross-origin`.
   - `Cache-Control`: `no-cache, no-store, must-revalidate` on HTML.
2. **Refactor `firestore.rules`:**
   - Author granular collection-level rules with helper functions (`isAuthenticated()`, `isOwner()`, `isAdmin()`, `isDomainUser()`).
   - Add catch-all `match /{document=**} { allow read, write: if false; }`.
3. **Refactor `storage.rules`:**
   - Enforce authenticated UID matching on upload paths.
   - Restrict file types (`application/pdf`, `image/*`) and size limits (`size < 15 * 1024 * 1024`).

### Phase 5: Verification & Syntax Testing
Validate rules with Firebase CLI:
```bash
bash scripts/test_rules.sh
```
Or:
```bash
npx firebase-tools deploy --dry-run
```

Output an executive summary scorecard detailing:
- Vulnerabilities Found & Fixed
- HTTP Security Headers Status
- Database Rules Status
- Storage Rules Status
- Static Bundle PII Status
- Final Security Score (e.g. 100/100)
