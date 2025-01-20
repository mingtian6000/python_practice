import psycopg2


def connect_to_postgres():

    try:
        connection = psycopg2.connect(
            database="postgres",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432"
        )

        cursor = connection.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print("PostgreSQL 数据库版本: ", version)
        cursor.close()
        connection.close()
    except (Exception, psycopg2.Error) as error:
        print("连接 PostgreSQL 数据库时出错:", error)


if __name__ == "__main__":
    connect_to_postgres()