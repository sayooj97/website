import requests
import re
from gpt4all import GPT4All
import csv

# Load GPT4All model
model_name = "Meta-Llama-3-8B-Instruct.Q4_0.gguf"
model = GPT4All(model_name, allow_download=True)

# URL of AMD's processor listing page
AMD_URL = "https://www.amd.com/en/products/specifications/processors.html"

# Function to fetch and extract AMD processor details using GPT4All
def scrape_amd_processors():
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(AMD_URL, headers=headers)

    if response.status_code == 200:
        raw_text = response.text  # Get webpage content

        # Remove HTML tags and extra spaces
        clean_text = re.sub(r"<[^>]*>", " ", raw_text)
        clean_text = re.sub(r"\s+", " ", clean_text)

        # GPT4All prompt to extract only processor details
        prompt = (
            f"Extract only AMD processor details (name, specs, price) from the following text. "
            f"Return in comma-separated format (no explanations, no extra words). "
            f"Example output: AMD Ryzen 9 7950X, 16 Cores, 32 Threads, 5.7GHz Boost, $699\n\n"
            f"{clean_text}"
        )

        extracted_data = model.generate(prompt, max_tokens=200).strip()

        return extracted_data  # Only the extracted details

    return "Failed to scrape"

# Run the scraper
amd_cpus = scrape_amd_processors()

# Save to CSV
with open("amd_processors.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Processor Name", "Specifications", "Price"])

    # Split data into rows (assuming GPT4All follows the comma-separated format)
    for line in amd_cpus.split("\n"):
        writer.writerow(line.split(", "))

print("✅ AMD Processor data saved to amd_processors.csv")
