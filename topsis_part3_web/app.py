from flask import Flask, request, render_template_string
import pandas as pd
import numpy as np
import re
import smtplib
from email.message import EmailMessage
import os

app = Flask(__name__)


SENDER_EMAIL = "YOUR_EMAIL"
SENDER_PASS = "Your_app_password"


def send_email(to_email, filepath):
    msg = EmailMessage()
    msg["Subject"] = "TOPSIS Result"
    msg["From"] = SENDER_EMAIL
    msg["To"] = to_email
    msg.set_content("Your TOPSIS result file is attached.")

    with open(filepath, "rb") as f:
        msg.add_attachment(
            f.read(),
            maintype="application",
            subtype="octet-stream",
            filename="result.csv"
        )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(SENDER_EMAIL, SENDER_PASS)
        smtp.send_message(msg)



def valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)



def run_topsis(df, weights, impacts):

    data = df.iloc[:, 1:].astype(float)

    norm = np.sqrt((data**2).sum())
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

    S_plus = np.sqrt(((V - best)**2).sum(axis=1))
    S_minus = np.sqrt(((V - worst)**2).sum(axis=1))
    score = S_minus / (S_plus + S_minus)

    df["Topsis Score"] = score
    df["Rank"] = score.rank(ascending=False)

    return df



HTML_FORM = """
<h2>TOPSIS Web Service</h2>
<form method="post" enctype="multipart/form-data">
File: <input type="file" name="file"><br><br>
Weights (comma separated): <input name="weights"><br><br>
Impacts (+,-): <input name="impacts"><br><br>
Email: <input name="email"><br><br>
<input type="submit">
</form>
"""


@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "GET":
        return render_template_string(HTML_FORM)

    file = request.files.get("file")
    weights_str = request.form.get("weights", "")
    impacts_str = request.form.get("impacts", "")
    email = request.form.get("email", "")

 
    if not file:
        return "File missing"

    if not valid_email(email):
        return "Invalid email format"

    weights = weights_str.split(",")
    impacts = impacts_str.split(",")

    try:
        weights = list(map(float, weights))
    except:
        return "Weights must be numeric"

    if any(i not in ["+", "-"] for i in impacts):
        return "Impacts must be + or -"

 
    try:
        if file.filename.endswith(".xlsx"):
            df = pd.read_excel(file)
        else:
            df = pd.read_csv(file)
    except:
        return "File read error"

    if df.shape[1] < 3:
        return "Need at least 3 columns"

    if len(weights) != df.shape[1] - 1:
        return "Weights count mismatch"

    if len(impacts) != df.shape[1] - 1:
        return "Impacts count mismatch"

 
    result = run_topsis(df, weights, impacts)

    out = "result.csv"
    result.to_csv(out, index=False)

  
    send_email(email, out)

    return "Result sent to your email!"


app.run(debug=True)
