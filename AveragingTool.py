import os
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)
import pandas as pd

#USER SETTINGS============================
input_csv = "corrected_S_N.csv"

species_list = []

#DO NOT EDIT BELOW THIS LINE=================

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
        # no data for this species, skip and warn
        print(f"skipping {species}: no rows found")
        continue

    for group_idx in range(3):
        start = group_idx * 10
        end = start + 10
        group = species_df.iloc[start:end]
        if group.empty:
            print(f"{species} group {group_idx+1} empty (rows {start}:{end}), skipping export")
            continue

        group_numeric = group[numeric_cols].apply(pd.to_numeric, errors='coerce')
        avg_spectrum = group_numeric.mean(axis=0)
        output_df = pd.DataFrame([numeric_cols, avg_spectrum.values])
        output_csv = os.path.join(output_dir, f"{species}_group{group_idx+1}_avg.csv")
        output_df.to_csv(output_csv, index=False, header=False)
