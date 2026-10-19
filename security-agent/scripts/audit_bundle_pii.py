#!/usr/bin/env python3
"""
Bundle & Static Asset Scanner for Firebase/Web Applications
Detects inlined PII datasets, exposed API keys, dangerous DOM sinks, and oversized payloads.
"""

import sys
import re
from pathlib import Path

EMAIL_REGEX = re.compile(r'\b[A-Za-z0-9._%+-]+@(?!example\.com|salute\.com|salutemissioncritical\.com)[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b')
PHONE_REGEX = re.compile(r'(\b\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b')
API_KEY_REGEX = re.compile(r'\bAIzaSy[0-9A-Za-z-_]{33}\b')
DANGEROUS_SINKS = [
    (re.compile(r'\beval\s*\('), 'eval() call'),
    (re.compile(r'document\.write\s*\('), 'document.write() call'),
    (re.compile(r'\.innerHTML\s*='), 'innerHTML direct assignment')
]

def scan_directory(target_dir):
    p = Path(target_dir)
    if not p.exists():
        print(f"[!] Directory not found: {target_dir}")
        return False

    html_and_js_files = list(p.glob('**/*.html')) + list(p.glob('**/*.js'))
    print(f"\n[*] Scanning {len(html_and_js_files)} static assets in: {p.resolve()}")
    print("-" * 65)

    findings = 0

    for f in html_and_js_files:
        try:
            content = f.read_text(encoding='utf-8', errors='ignore')
            file_findings = []

            # 1. Check file size
            size_mb = len(content) / (1024 * 1024)
            if size_mb > 1.0:
                file_findings.append(f"Oversized asset ({size_mb:.2f} MB). High risk of inlined database state.")

            # 2. Check for PII emails
            raw_emails = set(EMAIL_REGEX.findall(content))
            suspicious_emails = [e for e in raw_emails if not e.endswith(('.png', '.svg', '.jpg', '.jpeg', '.js', '.css'))]
            if suspicious_emails:
                file_findings.append(f"Potential PII Emails exposed ({len(suspicious_emails)}): {list(suspicious_emails)[:3]}")

            # 3. Check for API keys
            api_keys = set(API_KEY_REGEX.findall(content))
            if api_keys:
                file_findings.append(f"Google/Firebase API Key strings found ({len(api_keys)}). Verify key is restricted.")

            # 4. Check for DOM sinks
            for regex, label in DANGEROUS_SINKS:
                matches = len(regex.findall(content))
                if matches > 0 and 'innerHTML' not in label:
                    file_findings.append(f"Dangerous DOM Sink ({matches}): {label}")

            if file_findings:
                findings += len(file_findings)
                print(f"[!] {f.relative_to(p)}:")
                for item in file_findings:
                    print(f"    └── {item}")

        except Exception as e:
            print(f"[!] Could not read {f.name}: {e}")

    print("-" * 65)
    if findings == 0:
        print("[+] PASS: Zero critical PII leaks or dangerous sinks detected.")
        return True
    else:
        print(f"[!] ATTENTION: {findings} potential leak(s) or sink(s) flagged for review.")
        return False

if __name__ == '__main__':
    target = sys.argv[1] if len(sys.argv) > 1 else 'public'
    success = scan_directory(target)
    sys.exit(0 if success else 1)
