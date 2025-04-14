from openai import OpenAI

client = OpenAI(
    base_url="https://router.huggingface.co/sambanova/v1",
    api_key="dtryghoiok"
)

completion = client.chat.completions.create(
    model="Meta-Llama-3.3-70B-Instruct",
    messages=[
        {
            "role": "user",
            "content": "What is the average airspeed of a full laden swallow?"
        }
    ],
    max_tokens=500,
)

print(completion.choices[0].message)
