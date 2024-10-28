import openai
import os

# Aseta oma API-avaimesi ympäristömuuttujaan tai suoraan tähän.
openai.api_key = os.getenv("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")  # Varmista, että API-avain on asetettu oikein ympäristömuuttujaksi

def chat_with_gpt(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",  # Malliksi gpt-4 tai gpt-3.5-turbo tarpeen mukaan
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content'].strip()

if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit"]:
            break

        response = chat_with_gpt(user_input)
        print("Chatbot:", response)
