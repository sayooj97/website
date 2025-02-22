import pandas as pd

def load_data():
    """Loads PC part data from CSV files."""
    cpu_df = pd.read_csv("data/cpu.csv")
    motherboard_df = pd.read_csv("data/motherboard.csv")
    ram_df = pd.read_csv("data/ram.csv")
    gpu_df = pd.read_csv("data/gpu.csv")
    psu_df = pd.read_csv("data/psu.csv")
    storage_df = pd.read_csv("data/storage.csv")
    case_df = pd.read_csv("data/case.csv")
    
    return cpu_df, motherboard_df, ram_df, gpu_df, psu_df, storage_df, case_df

def check_compatibility(selected_cpu, motherboard_df, ram_df, gpu_df, psu_df, case_df):
    """Checks component compatibility based on CPU choice."""
    compatible_motherboards = motherboard_df[motherboard_df['socket'] == selected_cpu['socket']]
    compatible_ram = ram_df[(ram_df['type'] == selected_cpu['memory_type']) & (ram_df['speed'] <= selected_cpu['max_memory_speed'])]
    compatible_gpus = gpu_df  # Assuming all GPUs work unless PSU is insufficient
    compatible_psus = psu_df[psu_df['wattage'] >= selected_cpu['tdp'] + 250]  # 250W buffer
    compatible_cases = case_df[case_df['form_factor'].isin(compatible_motherboards['form_factor'].unique())]
    
    return {
        "motherboards": compatible_motherboards,
        "ram": compatible_ram,
        "gpu": compatible_gpus,
        "psu": compatible_psus,
        "case": compatible_cases
    }

if __name__ == "__main__":
    cpu_df, motherboard_df, ram_df, gpu_df, psu_df, storage_df, case_df = load_data()
    selected_cpu = cpu_df[cpu_df['name'] == 'intel core i7-13700k'].iloc[0]
    compatible_parts = check_compatibility(selected_cpu, motherboard_df, ram_df, gpu_df, psu_df, case_df)
    
    for part, df in compatible_parts.items():
        print(f"\nCompatible {part.upper()}:")
        print(df[['name']])
