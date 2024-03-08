import duckdb

def addition(a, b):
    return a+b

def tstduck():
    con = duckdb.connect("")
    print("connection was successfull")
    return con