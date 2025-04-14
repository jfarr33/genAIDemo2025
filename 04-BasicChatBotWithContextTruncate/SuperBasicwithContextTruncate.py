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

    # Use tiktoken tokenizer – best guess if using non-OpenAI model
encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")  # Close approximation

def count_tokens(messages):
    tokens = 0
    for msg in messages:
        tokens += 4  # Base tokens per message
        tokens += len(encoding.encode(msg['content']))
    return tokens

def truncate_messages(messages, max_tokens):
    # Keep trimming from the top until under the limit
    while count_tokens(messages) > max_tokens and len(messages) > 1:
        # Don't remove the system prompt (usually index 0)
        if messages[0]['role'] == 'system':
            messages.pop(1)
        else:
            messages.pop(0)
    return messages

while True:
    #print(messages)
    user_input = input("You: ")
    messages.append({"role": "user", "content": user_input})

    # Truncate to token limit
    messages = truncate_messages(messages, TOKEN_LIMIT)

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=2,
        max_tokens=4096,
    )

    assistant_reply = response.choices[0].message.content

    messages.append({"role": "assistant", "content": assistant_reply})

    print("FarrBot1000: " + assistant_reply)
