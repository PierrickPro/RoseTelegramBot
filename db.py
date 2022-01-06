import psycopg2
import configparser


# database connection
def connect():
    config_obj = configparser.ConfigParser()
    config_obj.read('config.ini')
    db_param = config_obj["postgresql"]

    con = psycopg2.connect(
        host=db_param["host"],
        database=db_param["database"],
        user=db_param["user"],
        password=db_param["password"]
    )

    return con


def get_wallets(username):
    con = connect()
    cur = con.cursor()
    cur.execute("SELECT ADDRESS FROM WALLET WHERE OWNER_USERNAME = '%s'" % username)
    rows = cur.fetchall()[0]

    if rows is None:
        return False

    con.close()
    return rows
