from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# user koyta course nice ? --> 4/5 ta box
#
# email >
# css >

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/", methods=["POST"])
def get_seat_status():
    course = request.form["course"].upper()
    section = request.form["section"]
    faculty = request.form["faculty"].upper()

    url = 'https://admissions.bracu.ac.bd/academia/admissionRequirement/getAvailableSeatStatus'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    cells_to_remove = soup.find_all(["td", "th"])
    rows = soup.find_all("tr")

    nimu = f"{course},{faculty},{section}"
    record = {}
    total = []
    i = 0
    for row in rows:
        p = row.text.split()
        total.append([p[0], p[2], p[4], p[-1]])
        t = f"{p[0]},{p[2]},{p[4]}"
        record[t] = i
        i += 1

    seat_status = total[record.get(nimu)]
    return jsonify(seat_status=seat_status)

if __name__ == "__main__":
    app.run(debug=True)