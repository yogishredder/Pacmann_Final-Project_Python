import mysql.connector
import pandas as pd

class Database:
    def __init__(self, host_name, user_name, user_password):
        self.host_name = host_name
        self.user_name = user_name
        self.user_password = user_password
        
    def koneksi_ke_server(self):
        connection = None
        try:
            connection = mysql.connector.connect(
                host=self.host_name,
                user=self.user_name,
                password=self.user_password            
            )
            print("MySQL Database connection successful")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        return connection
      
    def membuat_database(self, connection, nama_database):
        self.nama_database = nama_database
        try:
            query = f"""CREATE DATABASE IF NOT EXISTS {self.nama_database}"""
            cursor = connection.cursor()
            cursor.execute(query)
            print("Database berhasil dibuat")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            
    def membuat_table(self, connection, used_database):
        self.used_database = used_database
        try:
            tabel_user = """CREATE TABLE IF NOT EXISTS user(
                         id_user INT NOT NULL AUTO_INCREMENT, 
                         nama_user VARCHAR(50), 
                         tgl_lahir DATE, 
                         pekerjaan VARCHAR(50), 
                         alamat VARCHAR(50), 
                         constraint user primary key(id_user)
                         )"""
            tabel_buku = """CREATE TABLE IF NOT EXISTS buku(
                         id_buku INT NOT NULL AUTO_INCREMENT, 
                         nama_buku VARCHAR(50), 
                         kategori VARCHAR(50), 
                         stock INT, 
                         constraint user primary key(id_buku)
                         )"""
            tabel_peminjaman = """CREATE TABLE IF NOT EXISTS peminjaman(
                                 id_user INT, 
                                 id_buku INT, 
                                 nama_user VARCHAR(50), 
                                 nama_buku VARCHAR(50), 
                                 tgl_peminjaman DATE, 
                                 tgl_pengembalian DATE, 
                                 FOREIGN KEY(id_user) REFERENCES user(id_user), 
                                 FOREIGN KEY(id_buku) REFERENCES buku(id_buku)
                                 )"""

            cursor = connection.cursor()
            cursor.execute(f"""USE {self.used_database}""")
            cursor.execute(tabel_user)
            cursor.execute(tabel_buku)
            cursor.execute(tabel_peminjaman)
            print("Table berhasil dibuat")
        except mysql.connector.Error as err:
            print(f"Error: {err}")