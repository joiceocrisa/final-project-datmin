from pathlib import Path

import pandas as pd

app_dir = Path(__file__).parent
df = pd.read_csv(app_dir / "diabetes_dataset.csv")

# Drop duplicates
df = df.drop_duplicates()

# Drop Age Under 1
df = df[df['age'] > 1]

# Combine race columns into a single column
df['race'] = df[['race:AfricanAmerican', 'race:Asian', 'race:Caucasian', 'race:Hispanic', 'race:Other']].idxmax(axis=1)
df['race'] = df['race'].str.replace('race:', '')

df = df.drop(columns=['race:AfricanAmerican', 'race:Asian', 'race:Caucasian', 'race:Hispanic', 'race:Other'])
