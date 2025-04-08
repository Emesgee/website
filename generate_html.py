import hashlib
from pathlib import Path

# === CONFIG ===
password_file = Path("O://Github//website-login.txt")   # VeraCrypt-mounted path
template_file = Path("template.html")
output_file = Path("index.html")
cached_hash_file = Path(".password_hash")               # For fallback when volume is unmounted

# === DEBUG PATH ===
print(f"🔍 Looking for password file at: {password_file.resolve()}")

# === STEP 1: Get password hash ===
try:
    if password_file.exists():
        print("🔐 Reading password from VeraCrypt volume...")
        password = password_file.read_text(encoding="utf-8").strip()
        hashed = hashlib.sha256(password.encode()).hexdigest()
        cached_hash_file.write_text(hashed)
        print("✅ Password hashed and cached.")
    elif cached_hash_file.exists():
        print("⚠️ VeraCrypt not mounted. Using cached password hash...")
        hashed = cached_hash_file.read_text(encoding="utf-8").strip()
    else:
        print("❌ No password file found, and no cached hash available.")
        exit(1)
except Exception as e:
    print(f"❌ Error reading or hashing password: {e}")
    exit(1)

# === STEP 2: Read HTML template and replace hash ===
if not template_file.exists():
    print(f"❌ Template file not found: {template_file}")
    exit(1)

try:
    html = template_file.read_text(encoding="utf-8")
    html = html.replace("{{PASSWORD_HASH}}", hashed)
except Exception as e:
    print(f"❌ Error reading template or injecting hash: {e}")
    exit(1)

# === STEP 3: Write final index.html ===
try:
    output_file.write_text(html, encoding="utf-8")
    print(f"✅ index.html generated successfully at: {output_file.resolve()}")
except Exception as e:
    print(f"❌ Error writing index.html: {e}")
    exit(1)
