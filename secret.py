from google.cloud import secretmanager

def access_secret(project_id: str, secret_id: str, version_id: str = "latest") -> str:
    client = secretmanager.SecretManagerServiceClient()

    # Use project **ID**, not number
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"

    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")

# Example usage
if __name__ == "__main__":
    secret_value = access_secret("az-hackathon2025-tcs-458822", "GOOGLE_API_KEY")
    print(f"The secret is: {secret_value}")
