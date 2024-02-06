import secrets

def generate_api_key():
    return secrets.token_hex(16)  # Generates a 32-character hexadecimal string

if __name__ == "__main__":
    api_key = generate_api_key()
    print(f"Generated API Key: {api_key}")
