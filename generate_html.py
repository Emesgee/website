import hashlib
from pathlib import Path

# === CONFIG ===
# Set these to your actual paths
password_file = Path(r"O:\Github\website-login.txt")     # Inside VeraCrypt
template_file = Path("template.html")
output_file = Path("index.html")
cached_hash_file = Path(".password_hash")                # Hidden file to store fallback hash

# === STEP 1: Get password hash ===
if password_file.exists():
    print("🔐 Reading password from VeraCrypt volume...")
    password = password_file.read_text().strip()
    hashed = hashlib.sha256(password.encode()).hexdigest()
    
    # Cache the hash for future use when volume isn't mounted
    cached_hash_file.write_text(hashed)
    print("✅ Password hashed and cached.")
elif cached_hash_file.exists():
    print("⚠️ VeraCrypt not mounted. Using cached password hash...")
    hashed = cached_hash_file.read_text().strip()
else:
    print("❌ No password file found, and no cached hash available.")
    exit(1)

# === STEP 2: Read template and inject hash ===
if not template_file.exists():
    print(f"❌ Template file not found at: {template_file}")
    exit(1)

html = template_file.read_text()
html = html.replace("{{PASSWORD_HASH}}", hashed)

# === STEP 3: Write to index.html ===
output_file.write_text(html)
print(f"✅ index.html generated successfully.")
