from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtSql import QSqlTableModel, QSqlQuery
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMdiSubWindow, QMessageBox

import dialogAnggota

class Transaksi(QMdiSubWindow):
    def __init__(self,main=None):
        super().__init__()
        self.main = main
        loadUi('./ui/simpanan.ui', self)
        query = QSqlQuery("select * from jenis where nama_jenis like '%simpanan%'")
        while query.next():
            self.jenis.addItem(query.record().value(1))

        self.message = QMessageBox()
        self.model = QSqlTableModel()

        self.clear()
        self.tampilTransaksi()

        self.simpan.clicked.connect(self.saveSimpanan)
        self.cari_nik.clicked.connect(self.getAnggota)
        self.hapus.clicked.connect(self.hapusSimpanan)
        self.cari.clicked.connect(lambda : self.cariPetugas(self.txtcari.text()))
        self.txtcari.returnPressed.connect(lambda : self.cariSimpanan(self.txtcari.text()))

        self.setWindowTitle('Penarikan')

    def tampilTransaksi(self):
        query = QSqlQuery("SELECT a.nik, a.nama, a.gender, j.id_jenis, j.nama_jenis, s.* FROM anggota a, jenis j, transaksi s WHERE a.nik=s.nik AND j.id_jenis=s.id_jenis AND j.id_jenis!=4")
        self.model.setQuery(query)
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model.select()
        self.model.setHeaderData(0, Qt.Horizontal, "Kode Anggota")
        self.model.setHeaderData(1, Qt.Horizontal, "Nama")
        self.model.setHeaderData(2, Qt.Horizontal, "Jenis Kelamin")
        self.model.setHeaderData(4, Qt.Horizontal, "Jenis Simpanan")
        self.model.setHeaderData(8, Qt.Horizontal, "Jumlah")
        self.model.setHeaderData(9, Qt.Horizontal, "Tanggal Simpan")
        self.tableView.setModel(self.model)

        self.tableView.setColumnHidden(3,True)
        self.tableView.setColumnHidden(5,True)
        self.tableView.setColumnHidden(6,True)
        self.tableView.setColumnHidden(7,True)
        self.tableView.setColumnWidth(0, 150)
        self.tableView.setColumnWidth(1, 170)
        self.tableView.setColumnWidth(4, 170)

    def saveSimpanan(self):
        nik = self.nik.text()
        jenis = self.jenis.currentIndex()
        jumlah = self.jumlah.text()
        tanggal = self.tanggal.text().replace('/','-')
        if nik == "" or jumlah == "" or tanggal == "":
            self.notif.setText('Masukkan data dengan benar !')
        elif len(nik) != 16:
            self.notif.setText('Nik tidak benar !')
        else:
            self.notif.setText('')
            query = QSqlQuery()
            if query.exec_("insert into transaksi values(null,'"+nik+"','"+str(jenis+1)+"','"+jumlah+"','"+tanggal+"')"):
                query.exec_("select nik from simpanan where nik='"+nik+"'")
                if query.next():
                    query.exec_("update simpanan set jumlah=(select jumlah from simpanan where nik='"+nik+"') + "+jumlah+" where nik='"+nik+"'")
                else:
                    query.exec_("insert into simpanan values(null,'"+nik+"','"+jumlah+"')")
                self.message.setText(" ** Data berhasil ditambahkan ke database **")
                self.message.exec_()
                self.tampilTransaksi()
                self.clear()
                self.main.dfsimpan.tampilSimpanan()

    def getAnggota(self):
        anggota = dialogAnggota.DialogAnggota()
        anggota.exec_()
        self.nik.setText(anggota.datanik)

    def clear(self):
        self.nik.setText('')
        self.jenis.setCurrentIndex(0)
        self.jumlah.setText('')
        self.tanggal.setDateTime(QDateTime.currentDateTime())

    def hapusSimpanan(self):
        query = QSqlQuery()
        index = self.tableView.currentIndex().row()
        datamodel = self.tableView.model()
        kode_trans = datamodel.data(datamodel.index(index, 5), 0)
        query.exec_("delete from transaksi where id_trans='" + str(kode_trans) + "'")
        self.tampilTransaksi()

    def cariSimpanan(self,filter):
        query = QSqlQuery("SELECT a.nik, a.nama, a.gender, j.id_jenis, j.nama_jenis, s.* FROM anggota a, jenis j, transaksi s WHERE a.nik=s.nik AND j.id_jenis=s.id_jenis AND j.id_jenis!=4 AND (a.nik LIKE '%" + filter + "%' OR a.nama LIKE '%" + filter + "%' OR j.nama_jenis LIKE '%" + filter + "%' OR s.tgl_trans LIKE '%" + filter + "%')")
        self.model.setQuery(query)
        self.tableView.setModel(self.model)