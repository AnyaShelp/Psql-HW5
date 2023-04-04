import psycopg2


def create_db(conn):
    with conn.cursor() as cursor:
        cursor.execute('''
        create table if not exists client(
        id serial primary key,
        name varchar(80) not null,
        surname varchar(80),
        email varchar(80) unique
        );
        ''')

        cursor.execute('''
        create table if not exists phone_number(
        phone_number_id serial primary key,
        client_phone_number varchar(80),
        client_id integer not null references client(id)           
        );
        ''')


def add_client(conn, name, surname, email):
    with conn.cursor() as cursor:
        cursor.execute('''
        insert into client(name, surname, email) 
        values(%s, %s, %s) returning id;
        ''', (name, surname, email))
    cursor.fetchone()
    conn.commit()


def add_phone(conn, client_id, phone_number):
    with conn.cursor() as cursor:
        cursor.execute('''
        insert into phone_number(client_phone_number, client_id) 
        values(%s, %s)
        ''', (phone_number, client_id))
    cursor.fetchone()


def change_client(conn, client_id, name=None, surname=None, email=None):
    with conn.cursor() as cursor:
        if name:
            cursor.execute('''
                        update client
                        set name = %s 
                        where id = %s returning id;
                        ''', (name, client_id,))
        if surname:
            cursor.execute('''
                        update client
                        set surname = %s
                        set id = %s returning id;
                        ''', (surname, client_id,))
        if email:
            cursor.execute('''
                        update client
                        email = %s
                        set id = %s returning id;
                        ''', (email, client_id,))
        cursor.fetchmany()
        conn.commit()


def delete_phone(conn, phone_number_id):
    with conn.cursor() as cursor:
        cursor.execute('''
        delete from phone_number
        where phone_number_id = %s;
        ''', (phone_number_id,))
    cursor.fetchone()
    conn.commit()


def delete_client(conn, client_id):
    with conn.cursor() as cursor:
        cursor.execute('''
        delete from client
        where id = %s;
        ''', (client_id,))
    cursor.fetchone()
    conn.commit()


def find_client(conn, name=None, surname=None, email=None):
    with conn.cursor() as cursor:
        if name:
            cursor.execute('''
                        update client
                        set name = %s 
                        where id = %s returning id;
                        ''', (name,))
        if surname:
            cursor.execute('''
                        update client
                        set surname = %s
                        set id = %s returning id;
                        ''', (surname,))
        if email:
            cursor.execute('''
                        update client
                        email = %s
                        set id = %s returning id;
                        ''', (email,))
        cursor.fetchmany()
        conn.commit()


with psycopg2.connect(database="client_management", user="postgres", password="18483215786") as conn:
    create_db(conn)
    add_client(conn, 'Anna', 'Shelpyakova', 'anya_shelpyakova@inbox.ru')
    add_phone(conn, 1, '+79524236585')
    change_client(conn, 1, surname='Shelpyakova')
    delete_phone(conn, 2)
    delete_client(conn, 2)
    find_client(conn, email='anya_shelpyakova@inbox.ru')

conn.close()
