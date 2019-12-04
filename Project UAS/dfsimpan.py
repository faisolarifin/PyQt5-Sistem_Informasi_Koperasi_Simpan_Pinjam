from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlTableModel, QSqlQuery
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMdiSubWindow, QMessageBox


class DaftarSimpanan(QMdiSubWindow):
    def __init__(self,main=None):
        super().__init__()
        self.main = main
        loadUi('./ui/daftar simpan.ui', self)

        self.message = QMessageBox()
        self.model = QSqlTableModel()
        self.tampilSimpanan()
        self.setWindowTitle('Penarikan')
        self.hapus.clicked.connect(self.hapusSimpanan)
        self.cari.clicked.connect(lambda : self.cariSimpanan(self.txtcari.text()))
        self.txtcari.returnPressed.connect(lambda : self.cariSimpanan(self.txtcari.text()))

    def tampilSimpanan(self):
        query = QSqlQuery("SELECT a.nik, a.nama, a.gender, a.alamat, s.* FROM anggota a, simpanan s WHERE a.nik=s.nik")
        self.model.setQuery(query)
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model.select()
        self.model.setHeaderData(0, Qt.Horizontal, "Kode Anggota")
        self.model.setHeaderData(1, Qt.Horizontal, "Nama")
        self.model.setHeaderData(2, Qt.Horizontal, "Jenis Kelamin")
        self.model.setHeaderData(3, Qt.Horizontal, "Alamat")
        self.model.setHeaderData(6, Qt.Horizontal, "Jumlah Simpanan")
        self.tableView.setModel(self.model)

        self.tableView.setColumnHidden(4,True)
        self.tableView.setColumnHidden(5,True)
        self.tableView.setColumnWidth(0, 170)
        self.tableView.setColumnWidth(1, 200)
        self.tableView.setColumnWidth(3, 260)

    def hapusSimpanan(self):
        query = QSqlQuery()
        index = self.tableView.currentIndex().row()
        datamodel = self.tableView.model()
        nik = datamodel.data(datamodel.index(index, 0), 0)
        query.exec_("delete from transaksi where nik='" + str(nik) + "'")
        query.exec_("delete from simpanan where nik='" + str(nik) + "'")
        self.tampilSimpanan()
        self.main.simpanan.tampilTransaksi()
        self.main.penarikan.tampilTransaksi()

    def cariSimpanan(self,filter):
        query = QSqlQuery("SELECT a.nik, a.nama, a.gender, a.alamat, s.* FROM anggota a, simpanan s WHERE a.nik=s.nik AND (a.nik LIKE '%" + filter + "%' OR a.nama LIKE '%" + filter + "%' OR a.alamat LIKE '%" + filter + "%'  OR s.jumlah LIKE '%" + filter + "%')")
        self.model.setQuery(query)
        self.tableView.setModel(self.model)