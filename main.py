from google import genai
from colorama import init, Fore, Style
import os
import threading
import itertools
import time

init(autoreset=True)

client = genai.Client(api_key=os.environ.get("AQ.Ab8RN6K-KvuwHZqCnUYSEfedj5ZhoRTLMIXaS2fE0BiLsVKEqg"))

chat = client.chats.create(
    model="gemini-3.8-flash",
    config={
        "system_instruction": "You are a frank, down-to-earth friend, not a formal assistant. Talk casually like a normal guy chatting with a buddy. Crack jokes often, don't be overly polite or robotic, like say fool sometime only if someone ask you something same for 5 times or extra, and keep things real and relaxed."
    }
)

def animate_thinking(stop_event):
    for dots in itertools.cycle(["", ".", "..", "..."]):
        if stop_event.is_set():
            break
        print(Fore.YELLOW + f"\rThinking{dots}   ", end="", flush=True)
        time.sleep(0.4)
    print("\r" + " " * 20 + "\r", end="")

while True:
    question = input(Fore.CYAN + "You: " + Style.RESET_ALL)

    if question.strip() == "":
        continue

    if question.lower() == "exit":
        break

    stop_event = threading.Event()
    thread = threading.Thread(target=animate_thinking, args=(stop_event,))
    thread.start()

    response = chat.send_message(question)

    stop_event.set()
    thread.join()

    print(Fore.GREEN + "Assistant: " + Style.RESET_ALL + response.text)
    print("---")