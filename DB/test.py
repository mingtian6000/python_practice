from sqlalchemy import create_engine, Column, Integer, String




def main():
    engine = create_engine('postgresql://postgres:postgres@localhost:5432/postgres')
    engine.connect()
    # if connect fine, print log "connect OK"
    try:
        engine.connect()
        print("connect OK")
    except Exception as err:
        print(f"Failed to connect: {err}")
    
    



if __name__ == "__main__":
    main()