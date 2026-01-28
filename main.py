import sqlite3

def main():
    print("Hello from project-il-legible!")
    # connect_db()


def connect_db():
    try:
        # Connect to SQLite Database and create a cursor
        sqliteConnection = sqlite3.connect('sql.db')
        cursor = sqliteConnection.cursor()
        print('DB Init')

        # Execute a query to get the SQLite version
        query = 'SELECT sqlite_version();'
        cursor.execute(query)

        # Fetch and print the result
        result = cursor.fetchall()
        print('SQLite Version is {}'.format(result[0][0]))

        # Close the cursor after use
        cursor.close()

    except sqlite3.Error as error:
        print('Error occurred -', error)

    finally:
        # Ensure the database connection is closed
        if sqliteConnection:
            sqliteConnection.close()
            print('SQLite Connection closed')


if __name__ == "__main__":
    load_dotenv()
    main()
