#!/usr/bin/env bash
# Test & Validate Firebase Security Rules via dry-run compilation

set -e

echo "[*] Testing Firebase Rules Compilation..."
if command -v firebase &> /dev/null; then
    CLI="firebase"
elif command -v npx &> /dev/null; then
    CLI="npx firebase-tools"
else
    echo "[!] Error: firebase CLI or npx not found in PATH."
    exit 1
fi

echo "[+] Executing: $CLI deploy --only firestore:rules,storage --dry-run"
$CLI deploy --only firestore:rules,storage --dry-run

echo "[+] All security rules compiled successfully without errors."
