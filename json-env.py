import json

with open("credential_practice.json", "r") as f:
    data = json.load(f)

with open(".env", "w") as f:
    for key, value in data.items():
        if isinstance(value, str):
            # Escape newlines in strings
            value = value.replace("\n", "\\n")
            f.write(f'{key.upper()}="{value}"\n')  # ✅ Wrap in double quotes
        else:
            f.write(f"{key.upper()}={value}\n")
