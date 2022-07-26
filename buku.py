from database import Database
import pandas as pd
from datetime import datetime, timedelta

def user_baru(connection):
    try:
        nama_user = input('Masukkan nama user: ')
        tgl_lahir = input('Masukkan nama tgl_lahir (YYYY-MM-DD): ')
        pekerjaan = input('Masukkan pekerjaan: ')
        alamat = input('Masukkan alamat: ')
        data_user_baru = f"""INSERT INTO user(
                                            nama_user, 
                                            tgl_lahir, 
                                            pekerjaan, 
                                            alamat) 
                                            values(
                                            '{nama_user}', 
                                            '{tgl_lahir}', 
                                            '{pekerjaan}', 
                                            '{alamat}'
                                            )"""    
        cursor = connection.cursor()
        cursor.execute(data_user_baru)
        connection.commit()
        print("User baru berhasil ditambahkan")
    except mysql.connector.Error as err:
        print(f"Error: {err}")      

def buku_baru(connection):
    try:
        nama_buku = input('Masukkan nama buku: ')
        kategori = input('Masukkan kategori: ')
        stock = input('Masukkan jumlah stock: ')
        data_buku_baru = f"""INSERT INTO buku(
                                              nama_buku, 
                                              kategori, 
                                              stock) 
                                              values (
                                              '{nama_buku}', 
                                              '{kategori}', 
                                              '{stock}'
                                              )"""
        cursor = connection.cursor()
        cursor.execute(data_buku_baru)
        connection.commit()
        print("Buku baru berhasil ditambahkan")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

def update_buku(connection, id_buku, jumlah):
    try:
        stok_buku = f"""SELECT stock FROM buku WHERE id_buku = {id_buku}"""
        cursor = connection.cursor()
        cursor.execute(stok_buku)
        result = cursor.fetchone()
        jumlah_stok = result[0] + jumlah
        sisa_stock = f"""UPDATE buku SET stock = {jumlah_stok} WHERE id_buku = {id_buku}"""
        cursor.execute(sisa_stock)
        connection.commit()
        print("Stock buku berhasil diupdate")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

def pinjam_buku(connection):
    try:
        id_user = input("Masukkan id user: ")
        id_buku = input("Masukkan id buku: ")
        nama_user = input("Masukkan nama user: ")
        nama_buku = input("Masukkan nama buku: ")
        format_date = "%Y-%m-%d"
        tgl_pinjam = input("Masukkan tgl peminjaman(YYYY-MM-DD): ")
        tgl_pengembalian = (datetime.strptime(tgl_pinjam, format_date) + 
                            timedelta(days=3)).strftime(format_date)
        peminjaman_buku = f"""INSERT INTO peminjaman values(
                                                            '{id_user}',
                                                            '{id_buku}',
                                                            '{nama_user}',
                                                            '{nama_buku}',
                                                            '{tgl_pinjam}',
                                                            '{tgl_pengembalian}'
                                                            )"""
        cursor = connection.cursor()
        cursor.execute(peminjaman_buku)
        connection.commit()
        print("Buku dipinjamkan ke:", nama_user)
        update_buku(connection, id_buku, -1)
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        
def menampilkan_buku(connection):
    result = None   
    try:   
        tampil_buku = """SELECT * FROM buku"""
        cursor = connection.cursor()
        cursor.execute(tampil_buku)
        result = cursor.fetchall()
        jumlah_kolom = len(cursor.description)
        nama_kolom = [i[0] for i in cursor.description]
        df = pd.DataFrame(result)
        if df.empty == True:
            print('DataFrame is empty')
            print(nama_kolom)
        else:
            df.columns = nama_kolom
            print(df)
    except mysql.connector.Error as err:
        print(f"Error: {err}")

def menampilkan_user(connection):
    result = None   
    try:  
        cursor = connection.cursor()
        tampil_user = """SELECT * FROM user"""
        cursor.execute(tampil_user)
        result = cursor.fetchall()
        jumlah_kolom = len(cursor.description)
        nama_kolom = [i[0] for i in cursor.description]
        df = pd.DataFrame(result)
        if df.empty == True:
            print('DataFrame is empty')
            print(nama_kolom)
        else:
            df.columns = nama_kolom
            print(df)
    except mysql.connector.Error as err:
        print(f"Error: {err}")  

def tampilkan_peminjam(connection):
    result = None   
    try:
        cursor = connection.cursor()
        tampil_peminjam = """SELECT * FROM peminjaman"""
        cursor.execute(tampil_peminjam)
        result = cursor.fetchall()
        jumlah_kolom = len(cursor.description)
        nama_kolom = [i[0] for i in cursor.description]
        df = pd.DataFrame(result)
        if df.empty == True:
            print('DataFrame is empty')
            print(nama_kolom)
        else:
            df.columns = nama_kolom
            print(df)
    except mysql.connector.Error as err:
        print(f"Error: {err}")

def cari_buku(connection):
    result = None
    try:    
        nama_buku = input("Masukkan nama buku yang dicari: ")
        caribuku = f"""SELECT * from buku WHERE nama_buku = '{nama_buku}'"""
        cursor = connection.cursor()
        cursor.execute(caribuku)
        result = cursor.fetchall()
        jumlah_kolom = len(cursor.description)
        nama_kolom = [i[0] for i in cursor.description]
        df = pd.DataFrame(result)
        df.columns = nama_kolom
        print(df)  
    except mysql.connector.Error as err:
        print(f"Error: {err}")

def pengembalian_buku(connection):
    try:
        id_user = input("Masukkan id user:")
        id_buku = input("Masukkan id buku:")
        kembali_buku = f"""DELETE FROM peminjaman WHERE id_user={id_user} AND id_buku={id_buku}"""       
        cursor = connection.cursor()
        cursor.execute(kembali_buku)
        connection.commit()
        query_user = f"""SELECT nama_user FROM user WHERE id_user = {id_user}"""
        cursor = connection.cursor()
        cursor.execute(query_user)
        result = cursor.fetchone()
        nama_user = result[0]
        print("Buku telah dikembalikan oleh:", nama_user)
        update_buku(connection, id_buku, 1)
    except mysql.connector.Error as err:
        print(f"Error: {err}")
