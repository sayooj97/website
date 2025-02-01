import pandas as pd
import glob
import os
# jsons = pd.read_json('csv_files/cpu.json')
mul = glob.glob("csv_files/*.csv")
# cpus = jsons.to_csv('cpu.csv', index=False)
count = 0

for muls in mul:
    df = pd.read_csv(muls)
    count += 1
    filename = os.path.basename(muls)
    print(f"File name : {filename}")
    print(f"{df.columns}")

print(f"total processed file{count}")