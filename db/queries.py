import datetime

from db.database import connections


def create_table_query(table_column_data, file_path, table_name=None):
    if not table_name:
        table_name = f'table_{int(datetime.datetime.utcnow().timestamp())}'

    create_table_query_str = f'''CREATE TABLE {table_name} (
        id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
        {','.join(f"{name} {column_type}" for name, column_type in table_column_data)}
    );'''

    insert_data_str = f'''INSERT INTO {table_name} (
        {','.join(f"{name}" for name, _ in table_column_data)})
        VALUES ({', '.join("%s" for _ in table_column_data)})
    '''

    conn = connections.getconn()
    with conn.cursor() as cursor:
        cursor.execute(create_table_query_str)
        with open(file_path) as file:
            next(file)
            for row in file:
                cursor.execute(
                    insert_data_str,
                    row.strip().split(";")
                )
    conn.commit()

    connections.putconn(conn)
    return table_name

