#!/usr/bin/env python3
"""
HTTP Security Headers Auditor for Firebase Web Apps
Audits live URLs for modern security headers: CSP, HSTS, X-Frame-Options, nosniff, Referrer-Policy, Cache-Control.
"""

import sys
import urllib.request
import urllib.error

REQUIRED_HEADERS = {
    'content-security-policy': ('Content Security Policy', True),
    'x-frame-options': ('Clickjacking Protection (X-Frame-Options)', True),
    'x-content-type-options': ('MIME Sniffing Protection (nosniff)', True),
    'referrer-policy': ('Referrer-Policy', True),
    'strict-transport-security': ('HSTS Transport Security', True),
    'permissions-policy': ('Permissions-Policy', False),
    'cache-control': ('Cache-Control Directive', True)
}

def audit_url(url):
    print(f"\n[*] Auditing HTTP Security Headers for: {url}")
    print("-" * 65)

    req = urllib.request.Request(
        url,
        headers={'User-Agent': 'AntigravitySecurityAuditor/1.0'}
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            headers = {k.lower(): v for k, v in resp.headers.items()}
            status = resp.status
            print(f"[+] Connected: HTTP {status}\n")

            score = 0
            max_score = len(REQUIRED_HEADERS)

            for header_name, (label, is_critical) in REQUIRED_HEADERS.items():
                value = headers.get(header_name)
                crit_tag = "[CRITICAL]" if is_critical else "[RECOMMENDED]"

                if value:
                    score += 1
                    print(f"  [PASS] {label}:")
                    print(f"         └── {value[:80]}{'...' if len(value) > 80 else ''}")
                else:
                    print(f"  [FAIL] {crit_tag} Missing Header: {header_name}")

            print("-" * 65)
            compliance = round((score / max_score) * 100)
            print(f"[+] Security Header Compliance: {compliance}% ({score}/{max_score} checks passed)\n")
            return compliance >= 85

    except urllib.error.HTTPError as e:
        print(f"[!] HTTP Error {e.code}: {e.reason}")
        return False
    except Exception as e:
        print(f"[!] Connection failed: {e}")
        return False

if __name__ == '__main__':
    target = sys.argv[1] if len(sys.argv) > 1 else 'https://ta-rightfit.web.app/home.html'
    success = audit_url(target)
    sys.exit(0 if success else 1)
