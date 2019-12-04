from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtSql import QSqlTableModel, QSqlQuery
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMdiSubWindow, QMessageBox

import dialogAnggota

class Penarikan(QMdiSubWindow):
    def __init__(self,main=None):
        super().__init__()
        self.main=main
        loadUi('./ui/penarikan.ui', self)

        self.message = QMessageBox()
        self.model = QSqlTableModel()

        self.clear()
        self.tampilTransaksi()

        self.simpan.clicked.connect(self.simpanPenarikan)
        self.cari_nik.clicked.connect(self.getAnggota)
        self.hapus.clicked.connect(self.hapusPenarikan)
        self.cari.clicked.connect(lambda : self.cariPenarikan(self.txtcari.text()))
        self.txtcari.returnPressed.connect(lambda : self.cariPenarikan(self.txtcari.text()))

        self.setWindowTitle('Penarikan')

    def tampilTransaksi(self):
        query = QSqlQuery("SELECT a.nik, a.nama, a.gender, t.* FROM anggota a, transaksi t WHERE a.nik=t.nik AND t.id_jenis=4")
        self.model.setQuery(query)
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model.select()
        self.model.setHeaderData(0, Qt.Horizontal, "Kode Anggota")
        self.model.setHeaderData(1, Qt.Horizontal, "Nama")
        self.model.setHeaderData(2, Qt.Horizontal, "Jenis Kelamin")
        self.model.setHeaderData(6, Qt.Horizontal, "Jumlah Penarikan")
        self.model.setHeaderData(7, Qt.Horizontal, "Tanggal Penarikan")
        self.tableView.setModel(self.model)

        self.tableView.setColumnHidden(3,True)
        self.tableView.setColumnHidden(4,True)
        self.tableView.setColumnHidden(5,True)
        self.tableView.setColumnWidth(0, 150)
        self.tableView.setColumnWidth(1, 170)

    def simpanPenarikan(self):
        nik = self.nik.text()
        jumlah = self.jumlah.text()
        tanggal = self.tanggal.text().replace('/','-')
        if nik == "" or jumlah == "" or tanggal == "":
            self.notif.setText('Masukkan data dengan benar !')
        elif len(nik) != 16:
            self.notif.setText('Nik tidak benar !')
        else:
            self.notif.setText('')
            query = QSqlQuery()
            query.exec_("select nik from simpanan where nik='" + nik + "'")
            if query.next():
                query.exec_("insert into transaksi values(null,'" + nik + "','4','" + jumlah + "','" + tanggal + "')")
                query.exec_("select jumlah from simpanan where nik='" + nik + "'")
                if query.next():
                    hasil = query.record().value(0)
                    hasil -= int(jumlah)
                    if hasil < 0:
                        self.message.setText(" ** Penarikan melebihi jumlah simpanan **")
                        self.message.exec_()
                    else:
                        query.exec_("update simpanan set jumlah='" + str(hasil) + "' where nik='" + nik + "'")
                        self.message.setText(" ** Data berhasil ditambahkan ke database **")
                        self.message.exec_()
                        self.tampilTransaksi()
                        self.clear()
                        self.main.dfsimpan.tampilSimpanan()
            else:
                self.message.setText(" ** Anggota belum pernah menyimpan **")
                self.message.exec_()

    def getAnggota(self):
        anggota = dialogAnggota.DialogAnggota()
        anggota.exec_()
        self.nik.setText(anggota.datanik)

    def clear(self):
        self.nik.setText('')
        self.jumlah.setText('')
        self.tanggal.setDateTime(QDateTime.currentDateTime())

    def hapusPenarikan(self):
        query = QSqlQuery()
        index = self.tableView.currentIndex().row()
        datamodel = self.tableView.model()
        kode_trans = datamodel.data(datamodel.index(index, 3), 0)
        query.exec_("delete from transaksi where id_trans='" + str(kode_trans) + "'")
        self.tampilTransaksi()

    def cariPenarikan(self,filter):
        query = QSqlQuery("SELECT a.nik, a.nama, a.gender, t.* FROM anggota a, transaksi t WHERE a.nik=t.nik AND t.id_jenis=4 AND (a.nik LIKE '%" + filter + "%' OR a.nama LIKE '%" + filter + "%' OR t.jumlah LIKE '%" + filter + "%'OR t.tgl_trans LIKE '%" + filter + "%')")
        self.model.setQuery(query)
        self.tableView.setModel(self.model)