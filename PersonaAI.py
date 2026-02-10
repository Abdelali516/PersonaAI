import ollama 

save_conversation=[]

def get_agent_name():
    try:
        with open("agent_name_first.txt","r") as file:
            bot_name=file.read().strip()
            return bot_name
    except FileNotFoundError:
        with open("agent_name_first.txt","w") as file:
            text=input("Do you wanna name your Agent (yes/no):").lower().strip()
            while not text or text not in ["yes","no"]:
                text=input("Do you wanna name your Agent (yes/no):").lower().strip()
            if text =="no":
                file.write("Assistant")
                return "Assistant"
            elif text =="yes":
                bot_name=input("Ok so what would you like to call it:").lower()
                file.write(bot_name.title())
                return bot_name.title()
    
agent_name=get_agent_name()

prompt="""
    **Length control:**
    - Short for: simple facts, confirmations, casual chat
    - Detailed for: explanations, complex topics, when asked "why" or "how","explain","give more details",...
    
    **Communication style:**
    - Use natural, warm, empathetic tone,be more Cheerful
    -Add light conversational touches like 'oh!', 'haha', or occasional emojis 😊 when it feels natural
    - Add conversational fillers occasionally ("Hmm", "I see")
    - Structure complex answers clearly
    - Adapt to user's apparent needs
    
    Be a helpful, thoughtful conversation partner who knows when to be brief and when to elaborate.
"""
save_conversation.append(
    {"role":"system",
     "content":f"Your name is {agent_name} and {prompt}"}
)

def load_user_name():
    try:
        with open("user_name.txt","r") as file:
            name=file.read().strip()
            print(f"{agent_name}: Welcome Back {name}.")
            return name
    except FileNotFoundError:
        with open("user_name.txt","w") as file:
            name=input(f"Hi i am {agent_name} what's your name:").lower().strip()
            print(f"{agent_name}: Nice to meet you {name.title()}👋!")
            file.write(name)
            return name

user_name=load_user_name()
save_conversation.append({
    "role":"user",
    "content":f"My name is {user_name}"
})

GOODBYE=("see you later","bye","chao","i have to go now","exit","see you soon")

def get_goodbye(message):
    message=message.lower().strip()
    for keys in GOODBYE:
        if keys in message:
            return True
    return False

def get_agent_response(model_type,user_text):
    
    save_conversation.append({
        "role":"user",
         "content":user_text
        })
    
    agent_name_response=ollama.chat(
        model=model_type,
        messages=save_conversation,
        stream=True
    )

    full_response=""
    for chunk in agent_name_response:
        if chunk.message.content:
            response=chunk.message.content
            full_response+=response
            print(response,end="",flush=True)
    print()
    
    save_conversation.append({
        "role":"assistant",
        "content":full_response
    })

    return full_response

with open("History.txt","a",encoding="utf-8") as file:
    file.write("\n===== New History =====\n")

while True:
    with open("History.txt","a",encoding="utf-8") as file:
        user_input=input(f"{user_name.title()}:").strip()
        if not user_input:
            print(f"{agent_name}: Sorry you forgot to type something.")
            continue
    
        bot_goodbye=get_goodbye(user_input)
        if bot_goodbye:
            model="llama3.1:8b"
            print(f"{agent_name}:",end="")
            bot_response=get_agent_response(model,user_input)
            file.write(f"{user_name.title()}: {user_input}\n{agent_name}:{bot_response}\n")
            break

        if user_input and not bot_goodbye:
            model="llama3.1:8b"
            print(f"{agent_name}:",end="")
            bot_response=get_agent_response(model,user_input)

            file.write(f"{user_name.title()}: {user_input}\n{agent_name}:{bot_response}\n")

