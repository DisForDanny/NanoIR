import os
import random
import pandas as pd

output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

#USER SETTINGS============================
#change what is in the quotes below to match exactly what your CSV is called
input_csv = "ALL_S_N.csv"

#set to True to randomly reorder each species before splitting into three groups
optimize_grouping = True

#DO NOT EDIT BELOW THIS LINE=================

species_list = []

for f in os.listdir(output_dir):
    if f.endswith("_avg.csv"):
        try:
            os.remove(os.path.join(output_dir, f))
        except OSError:
            pass

df = pd.read_csv(input_csv)

if not species_list:
    species_list = list(df["Species"].dropna().unique())
    print("Species list inferred from input CSV:", species_list)

available_species = set(df["Species"].dropna())
for sp in species_list:
    if sp not in available_species:
        print(f"WARNING: requested species '{sp}' not found in {input_csv}")

numeric_cols = [col for col in df.columns if col not in ["Label", "Species"]]

for species in species_list:
    species_df = df[df["Species"] == species].reset_index(drop=True)
    if species_df.empty:
        print(f"skipping {species}: no rows found")
        continue

    row_count = len(species_df)
    if row_count % 3 != 0:
        print(f"ERROR: species '{species}' has {row_count} rows; expected a multiple of 3. Skipping this species.")
        continue

    block_size = row_count // 3
    print(f"processing {species}: {row_count} rows, {block_size} rows per group")

    if optimize_grouping and row_count >= 3:
        species_df = species_df.sample(frac=1, random_state=random.randint(0, 2**32 - 1)).reset_index(drop=True)
        print(f"randomly reordered {species} before grouping")

    for group_idx in range(3):
        start = group_idx * block_size
        end = start + block_size
        group = species_df.iloc[start:end]
        group_numeric = group[numeric_cols].apply(pd.to_numeric, errors='coerce')
        avg_spectrum = group_numeric.mean(axis=0)
        output_df = pd.DataFrame([numeric_cols, avg_spectrum.values])
        output_csv = os.path.join(output_dir, f"{species}_group{group_idx+1}_avg.csv")
        output_df.to_csv(output_csv, index=False, header=False)

