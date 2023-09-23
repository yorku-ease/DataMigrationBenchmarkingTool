from parser import Parser

p = Parser("output.log")
data = p.parsetoJson()
p.saveJson("data.json")
p.parsetoCSV("data.csv")
