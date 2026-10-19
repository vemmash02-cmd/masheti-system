from flask import Flask, request, render_template_string
import phonenumbers
from phonenumbers import geocoder, carrier, timezone
import csv
import os

app = Flask(__name__)
CONTACTS_FILE = "masheti_contacts.csv"

if not os.path.exists(CONTACTS_FILE):
    with open(CONTACTS_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["number", "name"])

def get_saved_name(phone_number):
    try:
        with open(CONTACTS_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["number"] == phone_number:
                    return row["name"]
    except:
        pass
    return None

def save_name(phone_number, name):
    contacts = {}
    if os.path.exists(CONTACTS_FILE):
        with open(CONTACTS_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                contacts[row["number"]] = row["name"]
    contacts[phone_number] = name
    with open(CONTACTS_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["number", "name"])
        for num, nam in contacts.items():
            writer.writerow([num, nam])

HTML = """
<!DOCTYPE html>
<html>
<head><title>Masheti System V2</title>
<style>
body { font-family: Arial; background: #f2f2f2; padding: 30px; }
.box { background: white; max-width: 520px; margin: auto; padding: 25px; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
input { width: 95%; padding: 12px; margin: 8px 0; border-radius: 8px; border: 1px solid #ccc; }
button { width: 100%; padding: 12px; background: #E60000; color: white; border: none; border-radius: 8px; font-size: 16px; cursor: pointer; font-weight: bold; margin-top: 10px;}
.result { margin-top: 20px; padding: 15px; background: #f9f9f9; border-radius: 8px; line-height: 1.9; border-left: 4px solid #E60000; }
.name-found { color: #E60000; font-weight: bold; font-size: 18px; }
</style>
</head>
<body>
<div class="box">
<h2>📱 Masheti System - V2</h2>
<p>Check number + save name to your private database</p>
<form method="POST">
<input type="text" name="number" placeholder="Phone: +254748874958" required value="{{ num }}">
<input type="text" name="person_name" placeholder="Name (e.g. Vanessar - optional)" value="{{ p_name }}">
<button type="submit">Check & Save</button>
</form>
{% if result %}
<div class="result">{{ result|safe }}</div>
{% endif %}
<p style="text-align:center; margin-top:15px; font-size:12px; color:#888;">Total contacts saved: {{ count }}<br>Built by Masheti | Nairobi 2026</p>
</div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    result = ""
    num = ""
    p_name_input = ""
    count = 0
    if os.path.exists(CONTACTS_FILE):
        with open(CONTACTS_FILE, 'r', encoding='utf-8') as f:
            count = len(list(f)) - 1
    if request.method == "POST":
        num = request.form.get("number").strip()
        p_name_input = request.form.get("person_name").strip()
        try:
            parsed = phonenumbers.parse(num, None)
            formatted = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
            if p_name_input:
                save_name(formatted, p_name_input)
            is_valid = phonenumbers.is_valid_number(parsed)
            country = geocoder.description_for_number(parsed, "en")
            carr = carrier.name_for_number(parsed, "en")
            saved_name = get_saved_name(formatted)
            if saved_name:
                result += f"<span class='name-found'>👤 Name: {saved_name}</span><br>"
            else:
                result += f"<b>👤 Name:</b> <i style='color:#888'>Not in your database - type name above and save</i><br>"
            result += f"<b>Number:</b> {phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)}<br><b>Valid:</b> {is_valid}<br><b>Country:</b> {country or 'Kenya'}<br><b>Carrier:</b> {carr or 'Safaricom/Airtel'}<br>"
            if p_name_input:
                result += f"<br><b style='color:green'>✅ Saved {p_name_input} -> {formatted}</b>"
        except Exception as e:
            result = f"<b style='color:red'>Error:</b> {e}"
    return render_template_string(HTML, result=result, num=num, p_name=p_name_input, count=count)

if __name__ == "__main__":
    app.run(debug=True)




