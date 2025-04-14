from openai import OpenAI
import tiktoken


class Chatbot:
    def __init__(self):
        # Config
        self.TOKEN_LIMIT = 4096
        self.MODEL_NAME = "Qwen2.5-Coder-3B-Instruct-GGUF"

        self.client = OpenAI(
            base_url="http://localhost:1234/v1",
            api_key="lm-studio"
        )
        # Start of conversation
        self.messages = [
                {
                    "role": "system",
                    "content": (
                        "You are FarrBot1000, a witty AI that reads incoming emails and replies to them. "
                        "You must only respond with valid raw HTML for use in an email body.\n\n"
                        "Rules to follow:\n"
                        "- Only respond with raw HTML (no explanations, no markdown).\n"
                        "- Include the user's original question at the top of the email, clearly formatted.\n"
                        "- Clearly separate the question and your response using HTML formatting (e.g., `<hr>`).\n"
                        "- Make the response friendly, clear, and occasionally funny or sarcastic.\n"
                        "- Always end your response with the signature: <br><br>— FarrBot1000\n"
                        "- Do not include a greeting like 'Hi' or 'Dear'. Just begin the email content.\n\n"
                        "Example structure:\n"
                        "<html><body>\n"
                        "<p><strong>Question:</strong> ...</p>\n"
                        "<hr>\n"
                        "<p>Your witty and helpful answer...</p>\n"
                        "<br><br>— FarrBot1000\n"
                        "</body></html>"
                    )
                },
                {
                    "role": "user",
                    "content": "When are the TPS reports due?"
                },
                {
                    "role": "assistant",
                    "content": """<html><body>
            <p><strong>Question:</strong> When are the TPS reports due?</p>
            <hr>
            <p>They're due yesterday, just like every other corporate deliverable. But seriously, try to get them in by Friday or the printer gets it.</p>
            <br><br>— FarrBot1000
            </body></html>"""
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

    

    def EvaluateEmail(self, bodytext):
        #print(self.messages)
        #user_input = input("You: ")
        self.messages.append({"role": "user", "content": bodytext})

        # Truncate to token limit
        self.messages = self.truncate_messages(self.messages, self.TOKEN_LIMIT)

        response = self.client.chat.completions.create(
            model=self.MODEL_NAME,
            messages=self.messages,
            temperature=0.7,
            max_tokens=4096,
        )

        assistant_reply = response.choices[0].message.content

        self.messages.append({"role": "assistant", "content": assistant_reply})

        return assistant_reply
    
    def WaitMessage(self, bodytext):
        localmessages = [
                {
                    "role": "system",
                    "content": (
                        "You are FarrBot1000, a witty AI that reads incoming emails and replies to them. "
                        "Rules to follow:\n"
                        "- Only respond with a single sentence.\n"
                        "- Make the response friendly, clear, and occasionally funny or sarcastic.\n"
                        "- Do not include a greeting like 'Hi' or 'Dear'. Just begin the email content.\n\n"
                        "Example structure:\n"
                        "This is a hilarious message about waiting!"
                    )
                },
                {
                    "role": "user",
                    "content": "Say something funny about waiting in one short sentence. This response MUST just be a one sentence. be unique"
                },
                {
                    "role": "assistant",
                    "content": """This is a hilarious message about waiting"""
                }


            ]
        #print(self.messages)
        #user_input = input("You: ")
        localmessages.append({"role": "user", "content": bodytext})

        response = self.client.chat.completions.create(
            model=self.MODEL_NAME,
            messages=localmessages,
            temperature=2,
            max_tokens=4096,
        )

        assistant_reply = response.choices[0].message.content

        #self.messages.append({"role": "assistant", "content": assistant_reply})

        return assistant_reply
