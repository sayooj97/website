from gpt4all import GPT4All

model_name = "Meta-Llama-3-8B-Instruct.Q4_0.gguf"
model = GPT4All(model_name, allow_download=True)  # Ensures the model is downloaded if missing

with model.chat_session():
    response = model.generate("how many columns can you process in a csv file at a time with max tokens as 500", max_tokens=512)
    print(response)
