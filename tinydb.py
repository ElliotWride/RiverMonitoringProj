from tinydb import TinyDB, Query

# Create a database instance
db = TinyDB('data.json')

# Define the table schema
table = db.table('readings')

# Function to insert data into the database
def insert_data(id, time, ph, ec, validated):
    table.insert({'ID': id, 'TIME': time, 'PH': ph, 'EC': ec, 'VALIDATED': validated})

# Function to retrieve all data from the database
def get_all_data():
    return table.all()

# Function to retrieve data by ID
def get_data_by_id(id):
    return table.get(Query().ID == id)

# Function to update data by ID
def update_data_by_id(id, time=None, ph=None, ec=None, validated=None):
    data = {}
    if time is not None:
        data['TIME'] = time
    if ph is not None:
        data['PH'] = ph
    if ec is not None:
        data['EC'] = ec
    if validated is not None:
        data['VALIDATED'] = validated
    
    table.update(data, Query().ID == id)

# Function to delete data by ID
def delete_data_by_id(id):
    table.remove(Query().ID == id)

# Example usage
if __name__ == "__main__":
    # Inserting sample data
    insert_data(1, 10.5, 7.0, 1.5, True)
    insert_data(2, 11.0, 7.2, 1.6, False)

    # Retrieving all data
    print("All Data:")
    print(get_all_data())

    # Retrieving data by ID
    print("\nData with ID 1:")
    print(get_data_by_id(1))

    # Updating data by ID
    print("\nUpdating data with ID 1:")
    update_data_by_id(1, ph=7.5)
    print(get_data_by_id(1))

    # Deleting data by ID
    print("\nDeleting data with ID 1:")
    delete_data_by_id(1)
    print(get_all_data())
