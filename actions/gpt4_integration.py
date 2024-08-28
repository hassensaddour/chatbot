import openai

# Set your OpenAI API key
openai.api_key = "sk-nCuG-HwfxKYmPJhA6t0rsBNMBl4vFN3p62wtzum2KDT3BlbkFJ6O8f7StdfIJxwSB_4sA1wIkB3bkQ6w0TSUzOVV4HsA"

# Function to get GPT-4 responses
def get_gpt4_response(prompt):
    response = openai.Completion.create(
        engine="gpt-3.5-turbo",  # Update this line if needed
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7,
    )

    return response.choices[0].text.strip()

# Example prompt incorporating CVE/MITRE data
prompt = "Considering the CVE database, how should one address a vulnerability in a telecom context?"
response = get_gpt4_response(prompt)
print(response)
