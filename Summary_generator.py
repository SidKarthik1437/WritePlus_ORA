import openai

openai.api_key = "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"

def generate_summary(text):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=text+"\nGenerate a summary of the above text in about 2 to 3 sentences.",
        max_tokens=100,
        temperature=0.5,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        n=1,
        stop=None
    )
    summary = response.choices[0].text.strip()
    return summary
