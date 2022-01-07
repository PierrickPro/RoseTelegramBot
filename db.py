import configparser
from sqlalchemy import create_engine


def connect():
    # connect
    config_obj = configparser.ConfigParser()
    config_obj.read('config.ini')
    db_param = config_obj["postgresql"]
    conn = create_engine(db_param["uri"])
    return conn


def insert_wallet(address, name, username):
    conn = connect()
    sql = "INSERT INTO wallet (address, name, owner_username) VALUES(%s,%s,%s);"
    conn.execute(sql, (address, name, username))

    # close
    conn.dispose()


def delete_wallet(username, name):
    conn = connect()
    sql = "DELETE FROM wallet WHERE name = %s AND owner_username = %s"
    conn.execute(sql, (name, username))

    # close
    conn.dispose()


def get_wallets(username):
    conn = connect()
    sql = "SELECT address, name FROM WALLET WHERE owner_username = %s;"
    resultset = conn.execute(sql, username)
    rows = resultset.mappings().all()

    if rows is None:
        return False

    # close
    conn.dispose()

    return rows


def get_wallet(username, name):
    conn = connect()
    sql = "SELECT ADDRESS, NAME FROM WALLET WHERE OWNER_USERNAME = %s AND NAME = %s"
    resultset = conn.execute(sql, (username, name))
    rows = resultset.mappings().all()

    if rows is None:
        return False

    # close
    conn.dispose()

    return rows
