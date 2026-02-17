import sys
import pandas as pd
import numpy as np


def error(msg):
    print("Error:", msg)
    sys.exit(1)


# ---------------- ARGUMENT CHECK ----------------
if len(sys.argv) != 5:
    error("Usage: python topsis.py <InputFile> <Weights> <Impacts> <OutputFile>")

input_file = sys.argv[1]
weights_str = sys.argv[2]
impacts_str = sys.argv[3]
output_file = sys.argv[4]

# ---------------- FILE READ ----------------
try:
    if input_file.endswith(".xlsx"):
        df = pd.read_excel(input_file)
    else:
        df = pd.read_csv(input_file)
except FileNotFoundError:
    error("File not found")

# ---------------- BASIC CHECKS ----------------
if df.shape[1] < 3:
    error("File must contain at least 3 columns")

data = df.iloc[:, 1:]

# numeric check
for col in data.columns:
    if not pd.api.types.is_numeric_dtype(data[col]):
        error(f"Column '{col}' must be numeric")

# ---------------- WEIGHTS & IMPACTS ----------------
try:
    weights = list(map(float, weights_str.split(",")))
except:
    error("Weights must be numeric and comma separated")

impacts = impacts_str.split(",")

if len(weights) != data.shape[1]:
    error("Number of weights must equal number of criteria columns")

if len(impacts) != data.shape[1]:
    error("Number of impacts must equal number of criteria columns")

for i in impacts:
    if i not in ["+", "-"]:
        error("Impacts must be + or - only")

# ---------------- TOPSIS ----------------

# normalize
norm = np.sqrt((data ** 2).sum())
R = data / norm

# weighted matrix
V = R * weights

best = []
worst = []

for i in range(len(impacts)):
    if impacts[i] == "+":
        best.append(V.iloc[:, i].max())
        worst.append(V.iloc[:, i].min())
    else:
        best.append(V.iloc[:, i].min())
        worst.append(V.iloc[:, i].max())

best = np.array(best)
worst = np.array(worst)

S_plus = np.sqrt(((V - best) ** 2).sum(axis=1))
S_minus = np.sqrt(((V - worst) ** 2).sum(axis=1))

score = S_minus / (S_plus + S_minus)

df["Topsis Score"] = score
df["Rank"] = score.rank(ascending=False)

# ---------------- SAVE OUTPUT ----------------
if output_file.endswith(".xlsx"):
    df.to_excel(output_file, index=False)
else:
    df.to_csv(output_file, index=False)

print("✅ TOPSIS completed successfully")
print("Output saved to:", output_file)
