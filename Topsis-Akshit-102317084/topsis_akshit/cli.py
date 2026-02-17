import sys
import pandas as pd
import numpy as np


def error(msg):
    print("Error:", msg)
    sys.exit(1)


def run():
    if len(sys.argv) != 5:
        error("Usage: topsis-run <InputFile> <Weights> <Impacts> <OutputFile>")

    input_file = sys.argv[1]
    weights_str = sys.argv[2]
    impacts_str = sys.argv[3]
    output_file = sys.argv[4]

    # -------- read file ----------
    try:
        if input_file.endswith(".xlsx"):
            df = pd.read_excel(input_file)
        else:
            df = pd.read_csv(input_file)
    except:
        error("File not found")

    if df.shape[1] < 3:
        error("Minimum 3 columns required")

    data = df.iloc[:, 1:]

    for col in data.columns:
        if not pd.api.types.is_numeric_dtype(data[col]):
            error("All criteria columns must be numeric")

    weights = list(map(float, weights_str.split(",")))
    impacts = impacts_str.split(",")

    if len(weights) != data.shape[1] or len(impacts) != data.shape[1]:
        error("Weights/Impacts count mismatch")

    for i in impacts:
        if i not in ["+", "-"]:
            error("Impacts must be + or -")

    # -------- TOPSIS ----------
    norm = np.sqrt((data ** 2).sum())
    R = data / norm
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

    if output_file.endswith(".xlsx"):
        df.to_excel(output_file, index=False)
    else:
        df.to_csv(output_file, index=False)

    print("TOPSIS completed. Output saved:", output_file)
