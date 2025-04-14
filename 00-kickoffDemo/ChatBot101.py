import time


while True:
    inputtext = input("You:").lower()

    if "hi" in inputtext and "you" in inputtext:
        time.sleep(3)
        print("Assistant: Hi, I am an AI large language model, so I do not have feelings.  How can I assist you today?")
    elif "weather" in inputtext:
        time.sleep(3)
        print("Assistant: Oh NO! Unfortunately, I am an AI large language model and unable to determine details about the weather in real-time.  Is there anything else I could assist you with?")
    elif "529" in inputtext and "squareroot" in inputtext:
        time.sleep(3)
        print("Assistant: The square of 529 is 23. The calculation 23^2 = 529.  Would you like some python code to calculate the square root of an input number?")
        newinputtext = input("You:").lower()
        if "sure" in newinputtext:
            time.sleep(3)
            print("Assistant: Excellent.  Here is some code you can try.\n")
            print("import Math\n")
            print("def CalcSquareRoot(value):")
            print("\treturn Math.sqrt(value)\n")
            print("")
            print("CalcSquareRoot(529)")
            print("")
            print("I hope that helps!")
    elif "pokemon" in inputtext:
        time.sleep(3)
        print("Assistant: I am an AI large language model, so I am not able to generate an opinion about Pokemon.  There are 791 pokemon in the official Pokemon Pokedex and of those Pikachu, Squirrtle, and Voldemort are popular options.  Would you like to learn more information about Pokemon? ")
    elif "harry" in inputtext:
        time.sleep(3)
        print("Assistant: Harry Potter is one of my favorite books!  I would watch the movies, but I haven't been given them yet. Would you like to know more about a specific book or scene?")
    elif "strawberry" in inputtext:
        time.sleep(3)
        print("Assistant: There are 3 Rs in the word strawberry.")
    else:
        time.sleep(3)
        print("Timeout...  Please try again.")