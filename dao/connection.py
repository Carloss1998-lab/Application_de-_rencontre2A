import psycopg2
import conf.properties as properties


def get_connection():
    return psycopg2.connect(host=properties.host, port=properties.port,
                            database=properties.database, user=properties.user, password=properties.password)
