import pandas as pd
import numpy as np

np.random.seed(42)
n = 200

data = {
    'Name': [f'Person_{i}' for i in range(n)],
    'Age': np.random.randint(18, 80, n),
    'ZipCode': np.random.choice([10001, 10002, 10003, 10004, 10005], n),
    'Gender': np.random.choice(['M', 'F'], n),
    'Income': np.random.randint(20000, 150000, n),
    'Disease': np.random.choice(['Diabetes', 'Hypertension', 'Asthma', 'None', 'None', 'None'], n)
}

df = pd.DataFrame(data)
df.to_csv('sample_data.csv', index=False)
print("✅ sample_data.csv created with 200 rows")
print("\nFirst 5 rows:")
print(df.head())
