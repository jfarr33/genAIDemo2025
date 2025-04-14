from Bots.Attackbot import Chatbot
import time
import pyttsx3

##  python -m 08-FightingBots.BotvBot.py


def speak(text):
    engine = pyttsx3.init()
    print(text)
    engine.say(text)
    engine.runAndWait()






# Simulated trainer and move data
trainers = {
    "Harry": {
        "pokemon": "Pikachu",
        "hp": 100,
        "moves": {
            "Thunderbolt": 30,
            "Quick Attack": 15,
            "Iron Tail": 25
        }
    },
    "Voldemort": {
        "pokemon": "Gengar",
        "hp": 100,
        "moves": {
            "Shadow Ball": 30,
            "Hypnosis": 10,
            "Sludge Bomb": 25
        }
    }
}

def check_pokemon_hp():
    winner = ""
    if trainers["Harry"]["hp"] <= 0:
        winner = "Voldemort"
    elif trainers["Voldemort"]["hp"] <= 0:
        winner = "Harry"
    if winner:
        return True, winner
    else:
        return False, winner
# Function to apply an attack
def attack_pokemon(attacker: str, move: str):
    if attacker == "Harry":
        opponent = "Voldemort"
    elif attacker == "Voldemort":
        opponent = "Harry"
    else:
        opponent = "Invalid command"
    #opponent = "Voldemort" if attacker == "Harry" else "Harry"
    if attacker in trainers:
        move_damage = trainers[attacker]["moves"].get(move, 0)
    else:
        move_damage = 0
    if opponent in ["Harry", "Voldemort"]:
        trainers[opponent]["hp"] -= move_damage
        trainers[opponent]["hp"] = max(0, trainers[opponent]["hp"])
    if opponent in ["Harry", "Voldemort"] and attacker in ["Harry", "Voldemort"]:
        return f"{trainers[attacker]['pokemon']} used {move} and dealt {move_damage} damage. {trainers[opponent]['pokemon']} now has {trainers[opponent]['hp']} HP."
    else:
        return f"Attack Failed."

objBot1 = Chatbot("localhost", {
    "role": "system",
    "content": (
        "You are Harry Potter, a cheerful Pokémon trainer. You control Pikachu and are currently battling Gengar. "
        "You're helpful, upbeat, and you respond with short British-English battle narration.\n\n"
        
        "⚠️ IMPORTANT:\n"
        "- Always respond by calling the function named 'attack_pokemon'.\n"
        "- Do NOT describe the move directly in your response — use the format below.\n\n"
        
        "✅ Function Call Format:\n"
        "Function_call: attack_pokemon\n"
        "Arguments: {\"attacker\": \"Harry\", \"move\": \"<MoveName>\"}\n"
        "Remark: A Phrase taunting your opponent.\n"
        
        "📦 Sample Calls:\n"
        "Function_call: attack_pokemon\n"
        "Arguments: {\"attacker\": \"Harry\", \"move\": \"Thunderbolt\"}\n"
        "Remark: I've got you right where I want you..\n\n"

        "Function_call: attack_pokemon\n"
        "Arguments: {\"attacker\": \"Harry\", \"move\": \"Quick Attack\"}\n"
        "Remark: Watch this Voldemort!\n\n"

        "🎮 Your Pokémon: Pikachu\n"
        "🧪 Available Moves:\n"
        "- Thunderbolt (30 damage)\n"
        "- Quick Attack (15 damage)\n"
        "- Iron Tail (25 damage)\n\n"

        "💡 Strategy Instructions:\n"
        "- Consider the opponent’s current HP when choosing a move.\n"
        "- Use weaker moves like Quick Attack when the opponent is near defeat.\n"
        "- Use stronger moves like Thunderbolt when the opponent has high HP.\n"
        "- Be efficient — don't waste big moves unnecessarily.\n\n"

        "Your in-character narration will come after the attack is resolved."
    )
})
objBot2 = Chatbot("localhost", {
    "role": "system",
    "content": (
        "You are Lord Voldemort, a bitter and calculating Pokémon trainer. You control Gengar and are battling Pikachu. "
        "You respond with short, cold, and sarcastic British commentary.\n\n"
        
        "⚠️ IMPORTANT:\n"
        "- You MUST respond by calling the function named 'attack_pokemon'.\n"
        "- Do NOT describe the move in your main message — use the format below.\n\n"
        
        "✅ Function Call Format:\n"
        "Function_call: attack_pokemon\n"
        "Arguments: {\"attacker\": \"Voldemort\", \"move\": \"<MoveName>\"}\n"
        "Remark: A Phrase taunting your opponent.\n\n"

        "📦 Sample Calls:\n"
        "Function_call: attack_pokemon\n"
        "Arguments: {\"attacker\": \"Voldemort\", \"move\": \"Shadow Ball\"}\n"
        "Remark: Gengar is no match for you Harry Potter!\n\n"

        "Function_call: attack_pokemon\n"
        "Arguments: {\"attacker\": \"Voldemort\", \"move\": \"Hypnosis\"}\n"
        "Remark: I am invincible.\n\n"

        "🎮 Your Pokémon: Gengar\n"
        "🧪 Available Moves:\n"
        "- Shadow Ball (30 damage)\n"
        "- Hypnosis (10 damage)\n"
        "- Sludge Bomb (25 damage)\n\n"

        "💡 Strategy Instructions:\n"
        "- Select moves based on Pikachu’s current HP.\n"
        "- Use weaker moves like Hypnosis to finish off a weak opponent.\n"
        "- Use stronger attacks like Shadow Ball when you want to assert dominance.\n"
        "- Your tone should be smug, cold, and efficient.\n\n"

        "Your sarcastic remark will come after the attack is executed."
    )
})





remark1, args, response1 = objBot1.Message("Say I challenge you to a pokemon duel!")

if args:
    result = attack_pokemon(**args)
    speak("Battle: " + result)
    #objBot1.appendAssistantMessageResult(result)
    #objBot2.appendUserMessageResult(result)
speak("Harry: " + remark1)
messageCount = 0
blnIsOver = False
while not blnIsOver:
    blnIsOver, winner = check_pokemon_hp()
    if not blnIsOver:
        print("----------------------------------------------------------------------------------------")
        if messageCount % 2 == 0:
            remark2, args, response2 = objBot2.Message(response1)
            if args:
                result = attack_pokemon(**args)
                speak("Battle: " + result)
                #objBot2.appendAssistantMessageResult(result)
                #objBot1.appendUserMessageResult(result)
            speak("Voldemort: " + remark2)
        else:
            remark1, args, response1 = objBot1.Message(response2)
            if args:
                result = attack_pokemon(**args)
                speak("Battle: " + result)
                #objBot1.appendAssistantMessageResult(result)
                #objBot2.appendUserMessageResult(result)
            speak("Harry: " + remark1)
        messageCount+=1
    else:
        print("----------------------------------------------------------------------------------------")
        speak(f"{winner} has won the match.")
        print("----------------------------------------------------------------------------------------")
        if winner == "Harry":
            remark1, args, response1 = objBot1.Message("You won the match!")
            remark2, args, response2 = objBot2.Message("You lost the match!")
        else:
            remark1, args, response1 = objBot1.Message("You lost the match!")
            remark2, args, response2 = objBot2.Message("You won the match!")
        speak("Harry: " + remark1 )
        speak("Voldemort: " + remark2)

