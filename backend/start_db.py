import psycopg2


def db_create_vkr_db():
    conn = psycopg2.connect(dbname="postgres", user="postgres", password="admin", host="db")
    cursor = conn.cursor()

    conn.autocommit = True
    sql = '''DROP DATABASE IF EXISTS vkr_db;'''
    cursor.execute(sql)
    sql = '''CREATE DATABASE vkr_db
            WITH 
            OWNER = postgres
            ENCODING = 'UTF8'
            TABLESPACE = pg_default
            CONNECTION LIMIT = -1;'''
    try:
        cursor.execute(sql)
    except psycopg2.Error as e:
        print("Error creating database:", e)
    conn.commit()
    cursor.close()
    conn.close()
    conn = psycopg2.connect(dbname="vkr_db", user="postgres", password="admin",
                            host="db")
    cursor = conn.cursor()
    conn.autocommit = True
    sql1 = '''
DROP TABLE IF EXISTS student CASCADE;
DROP TABLE IF EXISTS study_meeting CASCADE;
DROP TABLE IF EXISTS table_for_all CASCADE;
DROP TABLE IF EXISTS lesson CASCADE;
DROP TABLE IF EXISTS team CASCADE;
DROP TABLE IF EXISTS teacher CASCADE;
DROP TABLE IF EXISTS stud CASCADE;
DROP TABLE IF EXISTS rmup CASCADE;
CREATE TABLE rmup(
      id                 BIGSERIAL,
      name               VARCHAR   NOT NULL,
      link              VARCHAR   NOT NULL,
      date_of_add        TIMESTAMP NOT NULL,
      PRIMARY KEY(id)
    );
CREATE TABLE stud(
      id                 BIGSERIAL,
      name               VARCHAR   NOT NULL,
      email              VARCHAR,
      speciality VARCHAR NOT NULL,
      date_of_add        TIMESTAMP NOT NULL,

      PRIMARY KEY(id)
    );
CREATE TABLE teacher(
      id                 BIGSERIAL,
      name               VARCHAR   NOT NULL,
      lect_or_pract              VARCHAR NOT NULL,
      date_of_add        TIMESTAMP NOT NULL,
      PRIMARY KEY(id)
    );
CREATE TABLE team(
      id                 BIGSERIAL,
      name               VARCHAR   NOT NULL,
	  rmup_id bigint NOT NULL REFERENCES rmup ON DELETE CASCADE,
	  FOREIGN KEY(rmup_id) REFERENCES rmup(id),
      date_of_add        TIMESTAMP NOT NULL,
      PRIMARY KEY(id)
    );
CREATE TABLE lesson(
      id                 BIGSERIAL,
      name               VARCHAR   NOT NULL,
      mark_for_work REAL NOT NULL,
      arrival VARCHAR NOT NULL,
      test REAL NOT NULL,
      result_points REAL,
      result_mark VARCHAR,
      stud_id bigint NOT NULL REFERENCES stud ON DELETE CASCADE,
	  FOREIGN KEY(stud_id) REFERENCES stud(id),
      team_id bigint NOT NULL REFERENCES team ON DELETE CASCADE,
	  FOREIGN KEY(team_id) REFERENCES team(id),
      teacher_id bigint NOT NULL REFERENCES teacher ON DELETE CASCADE,
	  FOREIGN KEY(teacher_id) REFERENCES teacher(id),
      date_of_add        TIMESTAMP NOT NULL,
      PRIMARY KEY(id, team_id)
    )PARTITION BY RANGE (team_id);
    -- Create 200 partitions
DO $$
BEGIN
  FOR i IN 1..200 LOOP
    EXECUTE format('CREATE TABLE lesson_%s PARTITION OF lesson FOR VALUES FROM (%s) TO (%s)',
                   i, (i-1)*10, i*10);
  END LOOP;
END $$;
    '''
    cursor.execute(sql1)
    conn.commit()
    print("Database created successfully........")

    # Closing the connection

    cursor.close()
    conn.close()

def db_create_vkr_db_users():
    conn = psycopg2.connect(dbname="postgres", user="postgres", password="admin", host="db")
    cursor = conn.cursor()

    conn.autocommit = True
    sql = '''DROP DATABASE IF EXISTS vkr_db_users;'''
    cursor.execute(sql)
    sql = '''CREATE DATABASE vkr_db_users
            WITH 
            OWNER = postgres
            ENCODING = 'UTF8'
            TABLESPACE = pg_default
            CONNECTION LIMIT = -1;'''
    try:
        cursor.execute(sql)
    except psycopg2.Error as e:
        print("Error creating database:", e)
    conn.commit()
    cursor.close()
    conn.close()
    conn = psycopg2.connect(dbname="vkr_db_users", user="postgres", password="admin",
                            host="db")
    cursor = conn.cursor()
    conn.autocommit = True
    sql1 = '''
DROP TABLE IF EXISTS users CASCADE;
CREATE TABLE users(
    id SERIAL PRIMARY KEY,
    FIO VARCHAR NOT NULL,
    username VARCHAR(255) NOT NULL,
    password VARCHAR NOT NULL,
    email VARCHAR(255) NOT NULL,
    isAdmin bool NOT NULL,
    isTeacher bool NOT NULL,
    isCurator bool NOT NULL,
    date_of_add TIMESTAMP  NOT NULL
);
    '''
    cursor.execute(sql1)
    conn.commit()
    print("Database created successfully........")

    # Closing the connection

    cursor.close()
    conn.close()


db_create_vkr_db()
db_create_vkr_db_users()
