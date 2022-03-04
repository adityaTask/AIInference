import cx_Oracle

def connect_query(connection_string,sql_query):
    con = cx_Oracle.connect(connection_string)
    cursor = con.cursor()
    output = []
    for row in cursor.execute(sql_query):
        output.append(row)
    return output


