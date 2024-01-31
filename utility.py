import pandas as pd

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

def fetchCustomerData(name, fromDate, toDate, givenTo):
  df = pd.read_csv("Customers Database.csv")
  df = df[df["Name"] == name]
  if (fromDate != None and toDate != None) and (fromDate != "" and toDate != ""):
    df['\tDate'] = pd.to_datetime(df['\tDate'])
    df = df[(df['\tDate'] >= fromDate) & (df['\tDate'] <= toDate)]
  if givenTo != "###" and givenTo != None:
    df = df[df["\tGiven To"] == givenTo]
  date, due, given, remaining, givenFrom = [], [], [], [], []
  for row in df.iloc():
    date.append(row[1])
    due.append(row[2])
    given.append(row[3])
    remaining.append(row[4])
    givenFrom.append(row[5])
  allData = [date, due, given, remaining, givenFrom]
  return allData, len(date)
