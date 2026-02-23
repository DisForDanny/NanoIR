import pandas as pd
input_csv = "ALLSPECPS_S_N_py.csv"
df = pd.read_csv(input_csv)

species_list = [
    "FB16", "RO16", "DO1", "FB1", "RO1", "FB2", "RO2", "RO30",
    "DO30", "FB30", "FB4", "RO4", "FB8", "RO8"
]

wavenumber_cols = df.columns[1:]

for species in species_list:
    species_df = df[df["Species"] == species].reset_index(drop=True)
    for group_idx in range(3):
        start = group_idx * 10
        end = start + 10
        group = species_df.iloc[start:end]
        avg_spectrum = group[wavenumber_cols].mean(axis=0)
        output_df = pd.DataFrame([wavenumber_cols, avg_spectrum.values])
        output_csv = f"{species}_group{group_idx+1}_avg.csv"
        output_df.to_csv(output_csv, index=False, header=False)