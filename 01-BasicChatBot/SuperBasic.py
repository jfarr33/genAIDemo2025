from openai import OpenAI


    # Config
TOKEN_LIMIT = 4096
MODEL_NAME = "gemma-3-4b-it"

client = OpenAI(
        base_url="http://localhost:1234/v1",
        api_key="lm-studio"
    )


while True:
    #print(messages)
    user_input = input("You: ")

        # Start of conversation
    messages = [
            {
                "role": "system",
                "content": (
                    "You are FarrBot1000, a witty AI that provides general assistance."
                )
            }
            ]
    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=.07,
        max_tokens=4096,
    )

    print("FarrBot1000: " + response.choices[0].message.content)
