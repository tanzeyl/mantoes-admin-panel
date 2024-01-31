from flask import Flask, render_template, request, session
import pandas as pd
from datetime import datetime
import os
from utility import fetchData, fetchCustomerData

app = Flask(__name__)
app.secret_key = 'secret'

formData = {}

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

@app.route("/newCustomer", methods = ["GET", "POST"])
def newCustomer():
  return render_template("newCustomer.html")

@app.route("/getCustomerData", methods = ["GET", "POST"])
def getCustomerData():
  name = request.form.get("name")
  city = request.form.get("city")
  text = f"{name} - {city}"
  with open("Customers.txt", "a") as f:
    f.write(f"{text}\n")
  return render_template("index.html", message = "Customer added successfully.")

@app.route("/listAllCustomers", methods = ["GET", "POST"])
def listAllCustomers():
  customers = []
  with open("Customers.txt", "r") as f:
    for line in f:
      customers.append(line[:-1])
  return render_template("listAllCustomers.html", customers = customers)

@app.route("/getOneCustomer", methods = ["GET", "POST"])
def getOneCustomer():
  name = request.form.get("name")
  fromDate = request.form.get("from")
  toDate = request.form.get("to")
  givenTo = request.form.get("givenTo")
  allData, length = fetchCustomerData(name, fromDate, toDate, givenTo)
  return render_template("getOneCustomer.html", allData = allData, name = name, length = length)

@app.route("/updateCustomer", methods = ["POST"])
def updateCustomer():
  global formData
  name = request.form.get("name")
  if formData == dict(request.form):
    allData, length = fetchCustomerData(name, None, None, None)
    return render_template("getOneCustomer.html", allData = allData, name = name, length = length)
  date = datetime.strptime(request.form.get("date"), '%Y-%m-%d')
  date = date.strftime('%d/%m/%Y')
  amount = request.form.get("amount")
  givenTo = request.form.get("to")
  paymentType = request.form.get("type")
  df = pd.read_csv("Customers Database.csv")
  due = df[df["Name"] == name].iloc[[-1]]
  due = list(due["\tRemaining"])[0]
  if paymentType == "paid":
    remaining = int(due) - int(amount)
    newRow = {"Name" : name,
              "\tDate" : date,
              "\tDue" : due,
              "\tGiven" : amount,
              "\tRemaining" : remaining,
              "\tGiven To" : givenTo}
  else:
    rem = int(due) + int(amount)
    newRow = {"Name" : name,
              "\tDate" : date,
              "\tDue" : due,
              "\tGiven" : -int(amount),
              "\tRemaining" : rem,
              "\tGiven To" : "New Bill"}
  df.loc[len(df)] = newRow
  df.to_csv("Customers Database.csv", index = False)
  formData = dict(request.form)
  allData, length = fetchCustomerData(name, None, None, None)
  return render_template("getOneCustomer.html", allData = allData, name = name, length = length)

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

@app.route("/updateVendor", methods = ["POST"])
def updateVendor():
  global formData
  name = request.form.get("name")
  if formData == dict(request.form):
    allData, length = fetchData(name, None, None, None)
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
    rem = int(due) + int(amount)
    newRow = {"Name" : name,
              "\tDate" : date,
              "\tDue" : due,
              "\tGiven" : -int(amount),
              "\tRemaining" : rem,
              "Given From" : "New Bill"}
  df.loc[len(df)] = newRow
  df.to_csv("Raw Materials Database.csv", index = False)
  formData = dict(request.form)
  allData, length = fetchData(name, None, None, None)
  return render_template("getOneVendor.html", allData = allData, name = name, length = length)

@app.route("/resetTable", methods = ["GET", "POST"])
def resetTable():
  name = request.form.get("name")
  ftype = request.form.get("type")
  if ftype == "vendor":
    allData, length = fetchData(name, None, None, None)
    return render_template("getOneVendor.html", allData = allData, name = name, length = length)
  elif ftype == "customer":
    allData, length = fetchCustomerData(name, None, None, None)
    return render_template("getOneCustomer.html", allData = allData, name = name, length = length)

if __name__ == "__main__":
    app.run(debug = True, host = "0.0.0.0")
