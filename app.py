from flask import Flask, render_template, request, session
import pandas as pd
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'secret'

formData = {}

def fetchData(name, fromDate, toDate, givenFrom):
  df = pd.read_csv("Raw Materials Database.csv")
  df = df[df["Name"] == name]
  if (fromDate != None and toDate != None) and (fromDate != "" and toDate != ""):
    df['\tDate'] = pd.to_datetime(df['\tDate'])
    df = df[(df['\tDate'] >= fromDate) & (df['\tDate'] <= toDate)]
  if givenFrom != "###" and givenFrom != None:
    df = df[df["Given From"] == givenFrom]
  date, due, given, remaining, givenFrom = [], [], [], [], []
  for row in df.iloc():
    date.append(row[1])
    due.append(row[2])
    given.append(row[3])
    remaining.append(row[4])
    givenFrom.append(row[5])
  allData = [date, due, given, remaining, givenFrom]
  return allData, len(date)

@app.route("/", methods = ["GET", "POST"])
def home():
    return render_template("login.html")

@app.route("/verifyLogin", methods = ["GET", "POST"])
def verifyLogin():
  if session.get("username", None) is not None:
    username = session.get("username", None)
    password = session.get("password", None)
  else:
    username = request.form.get("username")
    password = request.form.get("password")
  envUsername = os.environ["MantoesUsername"]
  envPassword = os.environ["MantoesPassword"]
  if username == envUsername and password == envPassword:
    session["username"] = username
    session["password"] = password
    return render_template("index.html")
  else:
    return render_template("login.html", message = "Incorrect credentials.")

@app.route("/addNewVendor", methods = ["GET", "POST"])
def addNew():
    return render_template("addNew.html")

@app.route("/getVendorData", methods = ["GET", "POST"])
def getVendorData():
  name = request.form.get("vName")
  product = request.form.get("product")
  text = f"{name} - {product}"
  with open("Vendors.txt", "a") as f:
    f.write(f"{text}\n")
  return render_template("index.html", message = "Vendor added successfully.")

@app.route("/listAllVendors", methods = ["GET", "POST"])
def listAllVendors():
  vendors = []
  with open("Vendors.txt", "r") as f:
    for line in f:
      vendors.append(line[:-1])
  return render_template("listAllVendors.html", vendors = vendors)

@app.route("/getOneVendor", methods = ["GET", "POST"])
def getOneVendor():
  name = request.form.get("name")
  fromDate = request.form.get("from")
  toDate = request.form.get("to")
  givenFrom = request.form.get("givenFrom")
  allData, length = fetchData(name, fromDate, toDate, givenFrom)
  return render_template("getOneVendor.html", allData = allData, name = name, length = length)

@app.route("/resetTable", methods = ["GET", "POST"])
def resetTable():
  name = request.form.get("name")
  allData, length = fetchData(name, None, None, None)
  return render_template("getOneVendor.html", allData = allData, name = name, length = length)

@app.route("/updateVendor", methods = ["POST"])
def updateVendor():
  global formData
  name = request.form.get("name")
  if formData == dict(request.form):
    allData, length = fetchData(name)
    return render_template("getOneVendor.html", allData = allData, name = name, length = length)
  date = datetime.strptime(request.form.get("date"), '%Y-%m-%d')
  date = date.strftime('%d/%m/%Y')
  amount = request.form.get("amount")
  givenFrom = request.form.get("from")
  paymentType = request.form.get("type")
  df = pd.read_csv("Raw Materials Database.csv")
  due = df[df["Name"] == name].iloc[[-1]]
  due = list(due["\tRemaining"])[0]
  if paymentType == "paid":
    remaining = int(due) - int(amount)
    newRow = {"Name" : name,
              "\tDate" : date,
              "\tDue" : due,
              "\tGiven" : amount,
              "\tRemaining" : remaining,
              "Given From" : givenFrom}
  else:
    due = int(due) + int(amount)
    newRow = {"Name" : name,
              "\tDate" : date,
              "\tDue" : due,
              "\tGiven" : 0,
              "\tRemaining" : due,
              "Given From" : "New Bill"}
  df.loc[len(df)] = newRow
  df.to_csv("Raw Materials Database.csv", index = False)
  formData = dict(request.form)
  allData, length = fetchData(name)
  return render_template("getOneVendor.html", allData = allData, name = name, length = length)

if __name__ == "__main__":
    app.run(debug = True, host = "0.0.0.0")
