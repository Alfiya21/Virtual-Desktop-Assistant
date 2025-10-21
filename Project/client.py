from openai import OpenAI
client =OpenAI(
    api_key="Your open api key"
    )
completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content":" you are a virtual assistant named jarvis, skilled in general tasks like alexa and google cloud"},
        {"role": "user", "content": "what is coding"}
    ]
)
print(completion.choices[0].message)

