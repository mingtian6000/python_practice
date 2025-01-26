## this program is using python to gernate distribution graph post PT
import psycopg2
import matplotlib.pyplot as plt
import pandas as pd
from sqlalchemy import create_engine

def conn_db():
    try:
        connection = psycopg2.connect(
            database="postgres",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432"
        )
        return connection
    except (Exception, psycopg2.Error) as error:
        print("连接 PostgreSQL 数据库时出错:", error)   
        
def query_db(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    #records = cursor.fetchall()
    df = pd.read_sql(query, conn)
    return df

def create_dot_plot(df,title):
    plt.scatter(df['x'], df['y'], alpha=0.6)
    plt.title(title)
    plt.xlabel('uetr')
    plt.ylabel('count')
    plt.grid()   
    plt.show()
    #plt.savefig('dot_plot.png')

def main():   
    conn = conn_db()
    query = 'select * from uetr_dist' #real world query maybe quite complecated..
    df = query_db(conn, query)
    create_dot_plot(df, 'UETR Distribution')
    conn.close()
    
if __name__ == "__main__":
    main()

