from openai import OpenAI


    # Config
TOKEN_LIMIT = 4096
#MODEL_NAME = "gemma-3-4b-it"
#MODEL_NAME = "llama-3.2-3b-instruct"
#MODEL_NAME = "mistral-7b-instruct-v0.3"  #Doesn't work with SYSTEM ROLE
MODEL_NAME = "deepseek-r1-distill-qwen-7b"

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

    ##Temperature is a value that the LLM uses to help it decide between the probable answers available.  
    # The lower the temperature the more consistent the answer.  
    # The higher the temperature the more variety and also high probability for hallucentations.

    #Prompt: Tell me a joke

    #Let's try asking our bot to tell us a joke with lower temparature and then high temperature

    #At temp of 2 Gemini starts alternate between atom joke and scarecrow joke

    #Llama likes Pavlov's dog and Schrodinger's cat, but idd get some variety at 1.0, lots of variety at 2.0


    
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=.02,
        max_tokens=4096,
    )

    print("FarrBot1000: " + response.choices[0].message.content)
