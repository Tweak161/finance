from PyQt5.QtSql import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import pickle

db = QSqlDatabase.addDatabase("QSQLITE")
filename = '/media/thomas/3A7AB40B7AB3C245/EigeneDateien/Programmieren/Python/InteractiveBrokerAPI/data/data_test.db'
db = QSqlDatabase.addDatabase("QSQLITE")
db.setDatabaseName(filename)
open_success = db.open()
print("Database Connection Success: {}".format(open_success))

query = QSqlQuery()
query_status = query.exec_("DROP TABLE charts")
print("Drop charts = {}".format(query_status))
query_status = query.exec_("""CREATE TABLE charts (
                modified DATETIME NOT NULL,         
                type VARCHAR(40) NOT NULL,
                symbol VARCHAR(40) NOT NULL,
                exchange VARCHAR(40) NOT NULL,
                expiration DATETIME NOT NULL,
                iv BLOB NOT NULL,
                historical BLOB NOT NULL)""")  # historical JSON NOT NULL)

print("Create charts = {}".format(query_status))

x = ["102617",1,2,3]
xb = pickle.dumps(x)
xbb = QByteArray(xb)

query.prepare("INSERT INTO charts (modified, type, symbol, exchange, "
                      "expiration, iv, historical) VALUES (?, ?, ?, ?, ?, ?, ?)")
now = QDateTime.currentDateTime()
modified = now.addYears(-20)
query.addBindValue(QVariant((modified)))
query.addBindValue(QVariant(("FUT")))
query.addBindValue(QVariant("CL"))
query.addBindValue(QVariant("NYMEX"))
query.addBindValue(QVariant(modified))
query.addBindValue(xbb)
query.addBindValue(xbb)
query_status = query.exec_()
print("INSERT INTO charts (BindValue): {}".format(query_status))
query.addBindValue(QVariant((modified)))
query.addBindValue(QVariant(("STK")))
query.addBindValue(QVariant("SPY"))
query.addBindValue(QVariant("ARCA"))
query.addBindValue(QVariant(modified))
query.addBindValue(xbb)
query.addBindValue(xbb)
query_status = query.exec_()
print("INSERT INTO charts (BindValue): {}".format(query_status))

symbol = 'CL'
sec_type = 'FUT'
query_success = query.exec("SELECT * FROM charts WHERE symbol='{}' AND type='{}'".format(symbol, sec_type))
if query_success:
    # Loop through CHARTS
    while query.next():
        modified = query.value(0)
        modified = QDateTime.fromString(modified)
        type_chart = query.value(1)
        symbol_chart = query.value(2)
        exchange_chart = query.value(3)
        expiration_chart = query.value(4)
        iv = query.value(5)
        print("type(iv) = {}".format(type(iv)))
        iv = pickle.loads(iv)
        print("type(iv) = {}".format(type(iv)))
        print("iv = {}".format(iv))