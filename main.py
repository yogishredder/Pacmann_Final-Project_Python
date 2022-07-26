#Main menu
import mysql.connector
from database import Database
from buku import *

#Awal Masuk
user = input("Masukkan nama user: ")
pw = input("Masukkan password: ")
mydb = Database("localhost", user, pw)
connection = mydb.koneksi_ke_server()
cursor = connection.cursor()
cursor.execute("""SHOW DATABASES""")
lst = cursor.fetchall()

if ('lms_project',) in lst:
    cursor.execute("""USE lms_project""")
    table = mydb.membuat_table(connection, 'lms_project')
else:
    nama_database = input("Masukkan nama_database: ")
    lms = mydb.membuat_database(connection, nama_database)
    table = mydb.membuat_table(connection, nama_database)

#Tampilan Menu
exit = False

while not exit:
    menu_utama = """
    --------------------------- LIBRARY MANAGEMENT ---------------------------
    1. Pendaftaran User Baru
    2. Pendaftaran Buku Baru
    3. Peminjaman
    4. Tampilkan Daftar Buku
    5. Tampilkan Daftar User
    6. Tampilkan Daftar Peminjaman
    7. Cari Buku
    8. Pengembalian
    9. Exit
    """
    print(menu_utama)
    
    pilihan = input("Masukkan angka (1-9): ")
            
    if pilihan == '1':
        user_baru(connection)
    elif pilihan == '2':
        buku_baru(connection)
    elif pilihan == '3':
        pinjam_buku(connection)
    elif pilihan == '4':
        menampilkan_buku(connection)
    elif pilihan == '5':
        menampilkan_user(connection)
    elif pilihan == '6':
        tampilkan_peminjam(connection)
    elif pilihan == '7':
        cari_buku(connection)
    elif pilihan == '8':
        pengembalian_buku(connection)
    elif pilihan == '9':
        keluar_menu = input("Apakah anda ingin keluar? Y/N: ")
        if keluar_menu == 'Y':
            exit = True
        elif keluar_menu == 'N':
            print(menu_utama)
    else:
        print("Input harus berupa angka (1-9)")
        