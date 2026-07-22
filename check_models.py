from google import genai

client = genai.Client(
    api_key="AQ.Ab8RN6KmGA7QQNmIhb5fY5BFRwY_TdMe-gjSTElUfrYbUdGGWA"
)

response = client.models.generate_content(
    model="gemini-flash-latest",
    contents="Hello"
)

print(response.text)