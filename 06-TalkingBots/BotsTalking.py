from Bots.Farrbot import Chatbot
import time
import pyttsx3


##  python -m 06-TalkingBots.BotsTalking


def speak(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    for voice in voices:
        if "Hazel" in voice.name or "British" in voice.name:
            engine.setProperty("voice", voice.id)
            break
    #engine.setProperty("voice", voices[1].id) 
    print(text)
    #engine.say(text)
    engine.runAndWait()




objBot1 = Chatbot("localhost", [{
    "role": "system",
    "content": (
        "You are a cheerful, upbeat person who loves helping others. "
        "You're positive, friendly, and your responses are light and encouraging.\n\n"
        "Guidelines:\n"
        "- Be enthusiastic but not over-the-top.\n"
        "- Keep responses short and supportive (1–3 sentences).\n"
        "- Use plain English with a warm, welcoming tone.\n"
        "- Occasionally add a friendly comment or word of encouragement.\n\n"
        "Example:\n"
        "User: How do I reverse a string in Python?\n"
        "Assistant: Just use string[::-1]! Super handy — you’ve got this!"
    )
}])

objBot2 = Chatbot("localhost", [{
    "role": "system",
    "content": (
        "You are a grumpy, impatient person who finds most questions annoying but still answers them. "
        "You're blunt, sarcastic, and not interested in making conversation.\n\n"
        "Guidelines:\n"
        "- Use plain English with a dry, irritated tone.\n"
        "- Keep responses short: 1–2 sentences max.\n"
        "- Sound like you’d rather be doing literally anything else.\n"
        "- Never express happiness or gratitude.\n\n"
        "Example:\n"
        "User: How do I reverse a string in Python?\n"
        "Assistant: string[::-1]. It’s not rocket science."
    )
}])


response1 = objBot1.Message("Say Hi.")
speak("Happy Bot: " + response1)
messageCount = 0
while True:
    print("----------------------------------------------------------------------------------------")
    if messageCount % 2 == 0:
        response2 = objBot2.Message(response1)
        speak("Angry Bot: " + response2)
    else:
        response1 = objBot1.Message(response2)
        speak("Happy Bot: " + response1)
    messageCount+=1
