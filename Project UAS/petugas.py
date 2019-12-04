from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlTableModel, QSqlQuery
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMdiSubWindow, QMessageBox


class Petugas(QMdiSubWindow):
    def __init__(self):
        super().__init__()
        loadUi('./ui/petugas.ui', self)

        self.message = QMessageBox()
        self.model = QSqlTableModel()
        self.tampilPetugas()
        self.clear()

        self.simpan.clicked.connect(self.simpanPetugas)
        self.hapus.clicked.connect(self.hapusPetugas)
        self.cari.clicked.connect(lambda : self.cariPetugas(self.txtcari.text()))
        self.txtcari.returnPressed.connect(lambda : self.cariPetugas(self.txtcari.text()))

        self.setWindowTitle('Petugas')

    def tampilPetugas(self):
        self.model.setTable('petugas')
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model.select()
        self.model.setHeaderData(0, Qt.Horizontal, "Kode Petugas")
        self.model.setHeaderData(1, Qt.Horizontal, "Nama")
        self.model.setHeaderData(2, Qt.Horizontal, "Username")
        self.model.setHeaderData(3, Qt.Horizontal, "Password")
        self.model.setHeaderData(4, Qt.Horizontal, "No. Telp")
        self.model.setHeaderData(5, Qt.Horizontal, "Alamat")
        self.tableView.setModel(self.model)
        self.tableView.setColumnWidth(5, 180)

    def simpanPetugas(self):
        nama = self.nama.text()
        telp = self.telp.text()
        user = self.user.text()
        passw = self.passw.text()
        alamat = self.alamat.toPlainText()
        if nama == "" or telp == "" or user == "" or passw == "" or alamat == "" :
            self.notif.setText('Masukkan data dengan benar !')
        else:
            self.notif.setText('')
            query = QSqlQuery()
            if query.exec_("insert into petugas values(null,'"+nama +"','"+user+"','"+passw+"','"+telp+"','"+alamat+"')"):
                self.message.setText(" ** Data berhasil ditambahkan ke database **")
                self.message.exec_()
                self.tampilPetugas()
                self.clear()

    def hapusPetugas(self):
        self.model.removeRow(self.tableView.currentIndex().row())
        self.model.select()
        self.tampilPetugas()

    def cariPetugas(self,filter):
        query = QSqlQuery("SELECT * FROM petugas WHERE nama LIKE '%" + filter + "%' OR alamat LIKE '%" + filter + "%'")
        self.model.setQuery(query)
        self.tableView.setModel(self.model)

    def clear(self):
        self.nama.setText('')
        self.telp.setText('')
        self.user.setText('')
        self.passw.setText('')
        self.alamat.setPlainText('')