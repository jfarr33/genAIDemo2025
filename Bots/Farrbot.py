from openai import OpenAI
import tiktoken


class Chatbot:
    def __init__(self, IP, overwriteContent = None):
        # Config
        self.TOKEN_LIMIT = 4096
        #self.MODEL_NAME = "qwen2.5-coder-3b-instruct"
        self.MODEL_NAME = "gemma-3-4b-it"
        #self.MODEL_NAME = "llama-3.2-3b-instruct"

        self.client = OpenAI(
            base_url=f"http://{IP}:1234/v1",
            api_key="lm-studio"
        )
        # Start of conversation
        if overwriteContent:
            self.messages = overwriteContent
        else:
            self.messages = [
                    {
                        "role": "system",
                        "content": (
                            "You are an AI chat bot that needs to respond to all questions.  Even if they aren't questions."
                        )
                    }


            ]

        # Use tiktoken tokenizer – best guess if using non-OpenAI model
        self.encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")  # Close approximation

    def count_tokens(self, messages):
        tokens = 0
        for msg in messages:
            tokens += 4  # Base tokens per message
            tokens += len(self.encoding.encode(msg['content']))
        return tokens

    def truncate_messages(self, messages, max_tokens):
        # Keep trimming from the top until under the limit
        while self.count_tokens(messages) > max_tokens and len(messages) > 1:
            # Don't remove the system prompt (usually index 0)
            if messages[0]['role'] == 'system':
                messages.pop(1)
            else:
                messages.pop(0)
        return messages

    

    def Message(self, bodytext):
        #print(self.messages)
        #user_input = input("You: ")
        self.messages.append({"role": "user", "content": bodytext})

        # Truncate to token limit
        self.messages = self.truncate_messages(self.messages, self.TOKEN_LIMIT)

        response = self.client.chat.completions.create(
            model=self.MODEL_NAME,
            messages=self.messages,
            temperature=2,
            max_tokens=4096,
        )

        assistant_reply = response.choices[0].message.content

        self.messages.append({"role": "assistant", "content": assistant_reply})

        return assistant_reply
    
   