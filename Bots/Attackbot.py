from openai import OpenAI
import tiktoken
import json
import re


class Chatbot:
    def __init__(self, IP, overwriteContent = None):
        
        # Config
        self.TOKEN_LIMIT = 4096
        #self.MODEL_NAME = "Qwen2.5-Coder-3B-Instruct-GGUF"
        #self.MODEL_NAME = "llama-3.2-3b-instruct"
        #self.MODEL_NAME = "stable-code-instruct-3b"
        self.MODEL_NAME = "gemma-3-4b-it"

        self.client = OpenAI(
            base_url=f"http://{IP}:1234/v1",
            api_key="lm-studio"
        )
        # Start of conversation
        if overwriteContent:
            self.messages = [overwriteContent]
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

        self.function_call = ""

    def appendAssistantMessageResult(self, content):
        self.messages.append({"role": "assistant", "content": content})

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

    # Function to extract fake function call from plain text
    def extract_function_call(self, text):
        match = re.search(r"Function_call:\s*(\w+).*?Arguments:\s*(\{.*?\})", text, re.DOTALL)
        if match:
            func_name = match.group(1)
            try:
                args = json.loads(match.group(2))
                
                # Optional: extract smack talk (e.g. "Remark: ..." after the function call)
                remark_match = re.search(r"Remark:\s*(.*)", text)
                remark = remark_match.group(1).strip() if remark_match else ""
                
                return func_name, args, remark
            except json.JSONDecodeError:
                print("Failed to parse arguments.")
                return None, None, ""
        return None, None, ""


    def Message(self, bodytext):
        #print(self.messages)
        #user_input = input("You: ")
        self.messages.append({"role": "user", "content": bodytext})

        # Truncate to token limit
        self.messages = self.truncate_messages(self.messages, self.TOKEN_LIMIT)

        response = self.client.chat.completions.create(
            model=self.MODEL_NAME,
            messages=self.messages,
            temperature=1,
            max_tokens=4096
        )

        # Parse and execute function call
        func_name, args, remark = self.extract_function_call(response.choices[0].message.content)
        self.function_call = func_name

        # Send the result back
        self.messages.append({"role": "assistant", "content": response.choices[0].message.content})
        

        return remark, args, response.choices[0].message.content
    
   