import hashlib
from pathlib import Path

# === CONFIG ===
# Adjust these paths if needed
password_file = Path("O:\\Github\\website-login.txt")
template_file = Path("template.html")
output_file = Path("index.html")
print(f"Looking for password file at: {password_file.resolve()}")

# === STEP 1: Read the password ===
if not password_file.exists():
    print(f"❌ Password file not found at: {password_file}")
    exit(1)

password = password_file.read_text().strip()

# === STEP 2: Hash it using SHA-256 ===
hashed = hashlib.sha256(password.encode()).hexdigest()

# === STEP 3: Read HTML template and replace the placeholder ===
if not template_file.exists():
    print(f"❌ Template file not found at: {template_file}")
    exit(1)

html = template_file.read_text()
html = html.replace("{{PASSWORD_HASH}}", hashed)

# === STEP 4: Write to index.html ===
output_file.write_text(html)
print(f"✅ index.html generated successfully with hashed password.")
