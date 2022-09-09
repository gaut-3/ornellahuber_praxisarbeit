def load_account(username, password, conn):
    sql = """SELECT * FROM accounts WHERE username = %s AND password = %s  """

    cur = conn.cursor()
    cur.execute(sql, (username, password))
    account = cur.fetchone()

    cur.close()

    account_as_object = _map_account(account)

    return account_as_object

def check_does_new_account_exist(username, conn):

    sql = """SELECT * FROM accounts WHERE username = %s """

    cur = conn.cursor()
    cur.execute(sql, (username,))
    account = cur.fetchone()

    conn.commit()

    cur.close()
    if account is None:
        return False
    else:
        return True

def insert_new_account(username, password, conn):

    sql = """INSERT INTO accounts(username, password) VALUES(%s, %s)"""

    cur = conn.cursor()
    cur.execute(sql, (username, password))

    conn.commit()

    cur.close()

def _map_account(account):

    account_as_object = {
        'id': account[0],
        'username': account[1]
    }

    return account_as_object
