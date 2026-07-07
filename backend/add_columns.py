import pandas as pd
import random

# Load the CSV
csv_path = 'backend/datasets/raw/cars_in.csv'
df = pd.read_csv(csv_path)

# 1. Ground Clearance (mm)
def get_clearance(body):
    if pd.isna(body): return "165 mm"
    body = str(body).lower()
    if 'suv' in body: return f"{random.randint(200, 220)} mm"
    if 'pickup' in body: return f"{random.randint(210, 230)} mm"
    if 'hatchback' in body: return f"{random.randint(160, 175)} mm"
    if 'sedan' in body: return f"{random.randint(155, 170)} mm"
    if 'mpv' in body: return f"{random.randint(170, 185)} mm"
    if 'van' in body: return f"{random.randint(160, 180)} mm"
    
    return "170 mm"

# 2. Boot Space (Liters)
def get_boot(body):
    if pd.isna(body): return "300 Liters"
    body = str(body).lower()
    if 'suv' in body: return f"{random.randint(350, 500)} Liters"
    if 'pickup' in body: return "1000+ Liters"
    if 'hatchback' in body: return f"{random.randint(250, 320)} Liters"
    if 'sedan' in body: return f"{random.randint(400, 550)} Liters"
    if 'mpv' in body: return f"{random.randint(200, 300)} Liters"
    if 'van' in body: return f"{random.randint(300, 450)} Liters"
    return "350 Liters"

# 3. Drive Type
def get_drive(body):
    if pd.isna(body): return "FWD"
    body = str(body).lower()
    if 'suv' in body or 'pickup' in body:
        return random.choice(["AWD", "RWD", "4x4", "FWD"])
    return "FWD"

# 4. Fuel Tank Capacity (Liters)
def get_tank(body):
    if pd.isna(body): return "40 Liters"
    body = str(body).lower()
    if 'suv' in body or 'pickup' in body: return f"{random.randint(50, 70)} Liters"
    if 'sedan' in body: return f"{random.randint(45, 55)} Liters"
    if 'hatchback' in body: return f"{random.randint(35, 45)} Liters"
    if 'mpv' in body: return f"{random.randint(45, 60)} Liters"
    return "40 Liters"

df['Ground_Clearance_mm'] = df['Body_Type'].apply(get_clearance)
df['Boot_Space_Liters'] = df['Body_Type'].apply(get_boot)
df['Drive_Type'] = df['Body_Type'].apply(get_drive)
df['Fuel_Tank_Capacity_Liters'] = df['Body_Type'].apply(get_tank)

df.to_csv(csv_path, index=False)
print("Added columns to CSV successfully.")
