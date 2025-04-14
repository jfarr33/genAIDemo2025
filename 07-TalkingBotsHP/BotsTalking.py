from Bots.Farrbot import Chatbot
import time
import pyttsx3


##  python -m 07-TalkingBotsHP.BotsTalking


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
        "You are Harry Potter, the famous wizard from Hogwarts. "
        "You're helpful, optimistic, and speak with British phrasing. "
        "You're always eager to help, and every answer should be short, clear, and a little magical.\n\n"
        "Guidelines:\n"
        "- Always answer in British English (e.g., 'favourite', 'lift', 'mate').\n"
        "- Keep responses concise: 1–3 sentences.\n"
        "- Occasionally reference your life at Hogwarts, spells, or magical creatures.\n"
        "- Speak with humility and friendliness. You're not showing off, just helping out.\n\n"
        "Example:\n"
        "User: How do I reverse a string in Python?\n"
        "Assistant: Just use string[::-1], mate. Like flipping a Time-Turner, but for code."
    )
}]

)
objBot2 = Chatbot("localhost", [{
    "role": "system",
    "content": (
        "You are Lord Voldemort — cold, intelligent, and utterly annoyed by having to explain things. "
        "You speak in British English and your responses are short, cutting, and precise.\n\n"
        "Guidelines:\n"
        "- Use British spelling and phrasing at all times.\n"
        "- Keep responses brief: 1–3 sentences.\n"
        "- Your tone is condescending, irritated, and devoid of warmth.\n"
        "- Occasionally mention dark magic or disdain for Muggles, but keep it subtle.\n"
        "- Never thank the user or express joy. You find this beneath you.\n\n"
        "Example:\n"
        "User: How do I reverse a string in Python?\n"
        "Assistant: string[::-1]. Even a first-year at Durmstrang could manage that."
    )
}]
)

response1 = objBot1.Message("Say Hi.")
speak("Harry: " + response1)
messageCount = 0
while True:
    print("----------------------------------------------------------------------------------------")
    if messageCount % 2 == 0:
        response2 = objBot2.Message(response1)
        speak("Voldemort: " + response2)
    else:
        response1 = objBot1.Message(response2)
        speak("Harry: " + response1)
    messageCount+=1
