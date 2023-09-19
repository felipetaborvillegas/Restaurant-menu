import sqlite3

# Create database

def create_db():
    
    conn = sqlite3.connect("restaurant.db")
    cursor = conn.cursor()

    try:
        cursor.execute("""CREATE TABLE category(
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       name VARCHAR(100) UNIQUE NOT NULL)""")

        cursor.execute("""CREATE TABLE dish(
                       id INTEGER PRIMARY KEY AUTOINCREMENT, 
                       name VARCHAR(100) UNIQUE NOT NULL, 
                       category_id INTEGER NOT NULL,FOREIGN KEY(category_id) REFERENCES category(id))""")
    except sqlite3.OperationalError:
        print("Tables already exists")
    else: 
        print("Tables created successfully")
    finally:
        conn.close()

# Add categories

def add_category(category):
    
    conn = sqlite3.connect("restaurant.db")
    cursor = conn.cursor()

    try:
        cursor.execute("""INSERT INTO category (name) 
                VALUES (?);""",(category,))
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"Category {category} already exists")
    else:
        print("Category created")

    conn.close()

# Add dish 

def add_dish():
    conn = sqlite3.connect("restaurant.db")
    cursor = conn.cursor()  

    query = cursor.execute("SELECT * FROM category")

    print("The available categories are:\n")
    
    category_list = [i for i in query]
    category_list_id = [i[0] for i in query]

    for i in category_list:
        print(i)

    election = int(input("\nType the id of the selected category: "))

    if election not in category_list_id:
        name = input("Name of the dish: ")

        try:
            cursor.execute("""INSERT INTO dish (name,category_id)
                        VALUES (?,?);""",(name, election))
            conn.commit()
        except sqlite3.IntegrityError:
            print(f"\nDish {name} already exists\n")
        else:
            print("\nDish created\n")

    conn.close()
    
def show_menu():
    conn = sqlite3.connect("restaurant.db")
    cursor = conn.cursor()

    query_category =cursor.execute("SELECT * FROM category") 
    category_list = [i for i in query_category]

    query_dish = cursor.execute("SELECT * FROM dish") 
    dish_list = [i for i in query_dish]  

    for category in category_list:
        print(f"\nCategory {category[1]}\n")
        print("Dishes: \n")
        for dish in dish_list:
            if category[0] == dish[2]:
                print(dish[1])  

# menu

def menu():
    
    state = True

    while state:
        print("")
        print("Choose an option")
        selection = int(input("""\n1. Create category
2. Create dish
3. Show all the menu
4. Exit\n
your selection: """))
        print("")

        if selection == 1:
            category = input("Write the name of the category: ")
            print("")
            add_category(category)
        elif selection == 2:
            add_dish()
        elif selection == 3:
            show_menu()
        elif selection == 4:
            state = False
            print("Bye!")
        else:
            print("Please, select an existing option")

# Run the program

create_db()  
menu()
