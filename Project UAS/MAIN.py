import sys

from PyQt5 import QtSql
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QMainWindow

import dashboard, login, petugas, anggota, jenis, simpanan, penarikan, dfsimpan, pinjaman, angsuran

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        loadUi('./ui/main.ui', self)
        self.Koneksi()

        self.setCentralWidget(self.mdi)
        self.menu_file.triggered.connect(self.windowaction)
        self.menu_master.triggered.connect(self.windowaction)
        self.menu_simpanan.triggered.connect(self.windowaction)
        self.menu_pinjaman.triggered.connect(self.windowaction)

        self.Petugas.setVisible(False)
        self.Anggota.setVisible(False)
        self.Jenis.setVisible(False)
        self.Simpanan.setVisible(False)
        self.Penarikan.setVisible(False)
        self.Daftar_Simpanan.setVisible(False)
        self.Pinjaman.setVisible(False)
        self.Angsuran.setVisible(False)

        self.login = login.Login(self)
        self.dash = dashboard.Dashboard()
        self.petugas = petugas.Petugas()
        self.anggota = anggota.Anggota(self)
        self.jenis = jenis.Jenis()
        self.simpanan = simpanan.Transaksi(self)
        self.penarikan = penarikan.Penarikan(self)
        self.dfsimpan = dfsimpan.DaftarSimpanan(self)
        self.pinjaman = pinjaman.Pinjaman(self)
        self.angsuran = angsuran.Angsuran(self)

        self.mdi.addSubWindow(self.login)
        self.login.showMaximized()
        self.setWindowTitle("Sistem Informasi Koperasi Simpan Pinjam [SIKOSIP]")

    def Koneksi(self):
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('./db/sikosip.db')
        if not db.open():
            self.statusBar().showMessage("Galat !! Database connection failed")
        else:
            self.statusBar().showMessage("Koneksi database berhasil")

    def hitungBunga(self,pinjaman,bunga,lama,bulan=False):
        p = pinjaman
        i = bunga / 100
        t = lama
        angsurantotal = 0
        angsuranpokok = round(p / t, 2)
        if bulan is False:
            for j in range(1, t + 1):
                bungabulan = round((p - ((j - 1) * angsuranpokok)) * i / 12, 2)
                totalangsuran = angsuranpokok + bungabulan
                angsurantotal += totalangsuran
        else:
            bungabulan = round((p - ((bulan - 1) * angsuranpokok)) * i / 12, 2)
            angsurantotal = angsuranpokok + bungabulan

        return angsurantotal

    def windowaction(self, m):
        if m.text() == "Login":
            if self.login.isActiveWindow():
                self.login.showMaximized()
            else:
                self.mdi.addSubWindow(self.login)
                self.login.showMaximized()
        elif m.text() == "Data Petugas":
            if self.petugas.isActiveWindow():
                self.petugas.showMaximized()
            else:
                self.mdi.addSubWindow(self.petugas)
                self.petugas.showMaximized()
        elif m.text() == "Data Anggota":
            if self.anggota.isActiveWindow():
                self.anggota.showMaximized()
            else:
                self.mdi.addSubWindow(self.anggota)
                self.anggota.showMaximized()
        elif m.text() == "Data Jenis":
            if self.jenis.isActiveWindow():
                self.jenis.showMaximized()
            else:
                self.mdi.addSubWindow(self.jenis)
                self.jenis.showMaximized()
        elif m.text() == "Simpanan":
            if self.simpanan.isActiveWindow():
                self.simpanan.showMaximized()
            else:
                self.mdi.addSubWindow(self.simpanan)
                self.simpanan.showMaximized()
        elif m.text() == "Penarikan":
            if self.penarikan.isActiveWindow():
                self.penarikan.showMaximized()
            else:
                self.mdi.addSubWindow(self.penarikan)
                self.penarikan.showMaximized()
        elif m.text() == "Daftar Simpanan":
            if self.dfsimpan.isActiveWindow():
                self.dfsimpan.showMaximized()
            else:
                self.mdi.addSubWindow(self.dfsimpan)
                self.dfsimpan.showMaximized()
        elif m.text() == "Pinjaman":
            if self.pinjaman.isActiveWindow():
                self.pinjaman.showMaximized()
            else:
                self.mdi.addSubWindow(self.pinjaman)
                self.pinjaman.showMaximized()
        elif m.text() == "Angsuran":
            if self.angsuran.isActiveWindow():
                self.angsuran.showMaximized()
            else:
                self.mdi.addSubWindow(self.angsuran)
                self.angsuran.showMaximized()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.showMaximized()
    sys.exit(app.exec_())
