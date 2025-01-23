import requests
from bs4 import BeautifulSoup
import csv
import time

# URL of the website to scrape
url = 'https://www.amazon.in/Acer-1920x1080-Backlit-Monitor-Features/dp/B0CLY9HWHN/?_encoding=UTF8&pd_rd_w=eUqza&content-id=amzn1.sym.aff93425-4e25-4d86-babd-0fa9faf7ca5d%3Aamzn1.symc.36bd837a-d66d-47d1-8457-ffe9a9f3ddab&pf_rd_p=aff93425-4e25-4d86-babd-0fa9faf7ca5d&pf_rd_r=197AR0Y7A7Z1P4GAFJ6J&pd_rd_wg=q8ZEa&pd_rd_r=ae4c8483-9229-4505-b03e-20932d094d41&ref_=pd_hp_d_btf_ci_mcx_mr_hp_atf_m&th=1'

def fetch_webpage(url, retries=3, backoff_factor=0.3):
    for i in range(retries):
        response = requests.get(url)
        if response.status_code == 200:
            return response
        else:
            print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
            time.sleep(backoff_factor * (2 ** i))  # exponential backoff
    return None

response = fetch_webpage(url)

# Proceed only if the response is successful
if response:
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the container that holds the components data
    components_container = soup.find_all('div', class_='component')
    
    # List to store the scraped data
    components_data = []
    
    # Loop through each component container and extract details
    for component in components_container:
        name = component.find('h2', class_='name').text
        price = component.find('span', class_='price').text
        specs = component.find('p', class_='specs').text
        
        # Append the data to the list
        components_data.append([name, price, specs])
    
    # Write the data to a CSV file
    with open('components_data.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        # Write the headers
        writer.writerow(['Name', 'Price', 'Specifications'])
        # Write the component data
        writer.writerows(components_data)
    
    print("Data has been successfully scraped and saved to components_data.csv")
else:
    print("Failed to retrieve the webpage after multiple attempts.")