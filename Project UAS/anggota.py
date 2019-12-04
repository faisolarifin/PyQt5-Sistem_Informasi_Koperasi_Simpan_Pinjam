from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtSql import QSqlTableModel, QSqlQuery
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMdiSubWindow, QMessageBox


class Anggota(QMdiSubWindow):
    def __init__(self, main=None):
        super().__init__()
        self.main = main
        loadUi('./ui/anggota.ui', self)

        self.message = QMessageBox()
        self.model = QSqlTableModel()
        self.tampilAnggota()
        self.clear()

        self.simpan.clicked.connect(self.simpanAnggota)
        self.hapus.clicked.connect(self.hapusAnggota)
        self.cari.clicked.connect(lambda : self.cariAnggota(self.txtcari.text()))
        self.txtcari.returnPressed.connect(lambda : self.cariAnggota(self.txtcari.text()))

        self.setWindowTitle('Anggota')

    def tampilAnggota(self):
        self.model.setTable('anggota')
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model.select()
        self.model.setHeaderData(0, Qt.Horizontal, "NIK")
        self.model.setHeaderData(1, Qt.Horizontal, "Nama")
        self.model.setHeaderData(2, Qt.Horizontal, "Tanggal Lahir")
        self.model.setHeaderData(3, Qt.Horizontal, "Jenis Kelamin")
        self.model.setHeaderData(4, Qt.Horizontal, "No. Telp")
        self.model.setHeaderData(5, Qt.Horizontal, "Alamat")
        self.model.setHeaderData(6, Qt.Horizontal, "Tanggal Gabung")
        self.tableView.setModel(self.model)
        self.tableView.setColumnWidth(0, 150)
        self.tableView.setColumnWidth(1, 170)
        self.tableView.setColumnWidth(5, 180)

    def simpanAnggota(self):
        nik = self.nik.text()
        nama = self.nama.text()
        if self.gender1.isChecked():
            gender = self.gender1.text()
        elif self.gender2.isChecked():
            gender = self.gender2.text()
        lahir = self.lahir.text().replace('/','-')
        telp = self.telp.text()
        alamat = self.alamat.toPlainText()
        if nik == "" or nama == "" or gender == "" or lahir == "" or telp == "" or alamat == "":
            self.notif.setText('Masukkan data dengan benar ! ')
        elif len(nik) != 16:
            self.notif.setText('NIK tidak benar !')
        else:
            self.notif.setText('')
            query = QSqlQuery()
            query.exec_("select nik from anggota where nik='"+nik+"'")
            if not query.next():
                if query.exec_("insert into anggota values('"+nik+"','"+nama +"','"+lahir+"','"+gender+"','"+telp+"','"+alamat+"',date())"):
                    self.tampilAnggota()
                    self.clear()
                    self.message.setText(" \t** Anggota berhasil didaftar, \n Lanjutkan untuk pembayaran Simpanan Pokok **")
                    self.message.exec_()
                    self.main.mdi.addSubWindow(self.main.simpanan)
                    self.main.simpanan.jumlah.setFocus(True)
                    self.main.simpanan.nik.setText(nik)
                    self.main.simpanan.showMaximized()
            else:
                self.notif.setText('Anggota telah terdaftar !')

    def hapusAnggota(self):
        self.model.removeRow(self.tableView.currentIndex().row())
        self.model.select()
        self.tampilAnggota()

    def cariAnggota(self,filter):
        query = QSqlQuery("SELECT * FROM anggota WHERE nik LIKE '%" + filter + "%' OR nama LIKE '%" + filter + "%'OR alamat LIKE '%" + filter + "%'")
        self.model.setQuery(query)
        self.tableView.setModel(self.model)

    def clear(self):
        self.nik.setText('')
        self.nama.setText('')
        self.gender1.setChecked(False)
        self.gender2.setChecked(False)
        self.lahir.setDateTime(QDateTime.currentDateTime())
        self.telp.setText('')
        self.alamat.setPlainText('')