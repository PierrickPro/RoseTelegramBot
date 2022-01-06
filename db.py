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


def test():
    con = connect()
    cur = con.cursor()
    cur.execute("SELECT ADDRESS, NAME, OWNER_USERNAME FROM WALLET")
    rows = cur.fetchall()
    con.close()
    return rows
