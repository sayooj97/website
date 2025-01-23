import requests
import pandas as pd

url = "https://www.reddit.com/r/GadgetsIndia/comments/1i79zwb/best_phone_at_47k/"
page = requests.get(url)

# print(page.text)
print(page)
fetched_url = pd.DataFrame()