from openai import OpenAI
import tiktoken

    # Config
TOKEN_LIMIT = 4096
#MODEL_NAME = "Qwen2.5-Coder-3B-Instruct-GGUF"
MODEL_NAME = "gemma-3-4b-it"
#MODEL_NAME = "llama-3.2-3b-instruct"
#MODEL_NAME = "mistral-7b-instruct-v0.3"  #Doesn't work with SYSTEM ROLE
#MODEL_NAME = "deepseek-r1-distill-qwen-7b"

client = OpenAI(
        base_url="http://localhost:1234/v1",
        api_key="lm-studio"
    )
    # Start of conversation
messages = [
            {
                "role": "system",
                "content": (
                    "You are FarrBot1000, a witty AI that provides general assistance."
                )
            }
            ]


while True:
    #print(messages)
    user_input = input("You: ")
    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=.05,
        max_tokens=4096,
    )

    assistant_reply = response.choices[0].message.content

    messages.append({"role": "assistant", "content": assistant_reply})

    print("FarrBot1000: " + assistant_reply)
