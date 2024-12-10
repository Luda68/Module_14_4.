import sqlite3


def initiate_db():
    connection = sqlite3.connect('products.db')
    cursor = connection.cursor()
    cursor.execute('''
                CREATE TABLE IF NOT EXISTS Products (
                'id INTEGER PRiMARY KEY,'
                'title TEXT NOT NULL,'
                'description TEXT,'
                'price INTEGER NOT NULL');
    ''')

    
    for i in range(4):
        cursor.execute('INSERT INTO Products (title, description, price) VALUES (?, ?, ?, ?)',
                  (f'title{i}', f'description{i}', f'price{i*10}'))

    connection.commit()
    connection.close()

def get_all_products():
    connection = sqlite3.connect('products.db')
    cursor = connection.cursor()
    cursor.execute('SELECT id, title, description, price FROM Products')
    db = cursor.fetchall()

    connection.commit()
    connection.close()

def check_db(id, title, description, price):
    connection = sqlite3.connect('products.db')
    cursor = connection.cursor()

    check_db = cursor.execute('SELECT * FROM Products WHERE title=?', (title,))

    if check_db.fetchone() is None:
        cursor.execute(f'''
    INSERT INTO Products (id, title, description, price) VALUES('{id}', '{title}', '{description}', '{price}')
''')

    connection.commit()
    connection.close()

check_db(1,'Product 1', 'описание 1', 100)
check_db(2,'Product 2', 'описание 2', 200)
check_db(3,'Product 3', 'описание 3', 300)
check_db(4, 'Product 4', 'описание 4', 400)





