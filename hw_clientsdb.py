import psycopg2


# функция, создающая структуру БД(таблицы)
def createdb(conn):
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS clients(
    client_id SERIAL PRIMARY KEY,
    first_name VARCHAR(40),
    last_name VARCHAR(60),
    email VARCHAR(200)
    );
    """)
    cur.execute("""
       CREATE TABLE IF NOT EXISTS phones(
       phone_id SERIAL PRIMARY KEY,
       client_id INTEGER NOT NULL REFERENCES clients(client_id) ON DELETE CASCADE,
       phone VARCHAR(12)
       );
       """)
    conn.commit()


# функция, позволяющая добавить нового клиента
def add_client(conn, first_name, last_name, email):
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO clients(first_name, last_name, email)
    VALUES(%s,%s,%s);
    """, (first_name, last_name, email, ))
    conn.commit()


# функция, позволяющая добавить телефон для существующего клиента
def add_phone_cl(conn, client_id, phone):
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO phones (client_id, phone)
    VALUES(%s,%s);
    """, (client_id, phone))
    conn.commit()


# Функция, позволяющая изменить данные о клиенте
def update_client(conn, client_id, first_name=None, last_name=None, email=None):
    cur = conn.cursor()
    cur.execute("""
    SELECT * FROM clients
    WHERE client_id = %s
    """, (client_id, ))
    info_cl = cur.fetchone()
    if first_name is None:
        first_name = info_cl[1]
    if last_name is None:
        last_name = info_cl[2]
    if email is None:
        email = info_cl[3]
    cur.execute("""
    UPDATE clients SET first_name= %s, last_name=%s, email=%s
    WHERE client_id=%s
    """, (first_name, last_name, email, client_id, ))

    conn.commit()


# Функция, позволяющая удалить телефон для существующего клиента
def delete_phone_cl(conn, client_id, phone):
    cur = conn.cursor()
    cur.execute("""
    DELETE FROM phones
    WHERE client_id=%s AND phone=%s
    """, (client_id, phone, ))


# Функция, позволяющая удалить существующего клиента
def delete_clients(conn, client_id):
    cur = conn.cursor()
    cur.execute("""
    DELETE FROM clients
    WHERE client_id=%s
    """, (client_id, ))


# Функция, позволяющая найти клиента по его данным: имени, фамилии, email или телефону
def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    cur = conn.cursor()
    if first_name is None:
        first_name = '%'
    if last_name is None:
        last_name = '%'
    if email is None:
        email = '%'
    if phone is None:
        cur.execute("""
        SELECT c."client_id", c."first_name", c."last_name", c."email", p."phone" FROM clients c 
        LEFT JOIN phones p ON c.client_id = p.client_id
        WHERE c."first_name" LIKE %s AND c."last_name" LIKE %s AND c."email" LIKE %s
        """, (first_name, last_name, email))
    else:
        cur.execute("""
        SELECT c."client_id, c."first_name", c."lst_name", c."email", p."phone" FROM clients c 
        LEFT JOIN phones p ON c.client_id = p.client_id
        WHERE c."first_name" LIKE %s AND c."last_name" LIKE %s AND c."email" LIKE %s AND p."phone" LIKE %s
        """, (first_name, last_name, email, phone))
    print(cur.fetchone())

#
# функция, позволяющая вывести всю информацию о клиентах
def get_find_clients(conn):
    cur = conn.cursor()
    cur.execute("""
    SELECT * FROM clients
    """)
    print(cur.fetchall())


with psycopg2.connect(database='hw_clientsdb_', user='postgres', password='') as conn:
    if __name__ == "__main__":
        # # создание таблиц
        # createdb(conn)
        #
        # # добавление клиентов в таблицу
        # add_client(conn, 'Андрей', 'Богатырев', 'andrei.bog@yandex.ru')
        # add_client(conn, 'Анастасия', 'Добролюбова', 'anastasya75784@gmail.com')
        # add_client(conn, 'Ольга', 'Васильева', 'hgftju5698@mail.ru')
        # add_client(conn, 'Игорь', 'Верхов', 'igor_verhov568a@yanex.ru')
        # add_client(conn, 'Светлана', 'Родионова', 'svetlana_rod8694@mail.ru')
        #
        # # добавление номера телефона для существующего клиента
        # add_phone_cl(conn, '1', '79635645982')
        # add_phone_cl(conn, '2', '79967641258')
        # add_phone_cl(conn, '3', '79965664523')
        #
        # # изменение данных о клиенте
        # update_client(conn, '4', first_name='Олег', )
        #
        # # удаление номера телефона у существующего клиента
        # delete_phone_cl(conn, 2, '79967641258')
        #
        # # удаление существующего клиента
        # delete_clients(conn, '5')

        # поиск клиента по его данным
        find_client(conn, first_name='Андрей')

        find_client(conn, last_name='Верхов')

        # print(get_find_clients(conn))

conn.close()
