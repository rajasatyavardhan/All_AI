import sqlite3

# Connect to the searches.db database
conn = sqlite3.connect('searches.db', check_same_thread=False)
c = conn.cursor()

# Function to retrieve all search entries from the database
def get_all_searches():
    c.execute("SELECT * FROM search_logs")
    return c.fetchall()

if __name__ == "__main__":
    searches = get_all_searches()
    if searches:
        print("Logged Searches:")
        for search in searches:
            print(f"Query: {search[0]}, Timestamp: {search[1]}")
    else:
        print("No searches found.")
