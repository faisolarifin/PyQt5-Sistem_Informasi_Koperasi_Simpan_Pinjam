from PyQt5.QtCore import Qt, QDate
from PyQt5.QtSql import QSqlTableModel, QSqlQuery
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMdiSubWindow, QMessageBox

import dialogAnggota

class Pinjaman(QMdiSubWindow):
    def __init__(self,main=None):
        super().__init__()
        self.main = main
        loadUi('./ui/pinjaman.ui', self)

        self.message = QMessageBox()
        self.model = QSqlTableModel()

        self.tampilPinjaman()
        self.clear()
        self.autocode()

        self.simpan.clicked.connect(self.savePinjaman)
        self.bunga.valueChanged.connect(self.setTotal)
        self.jumlah.textChanged.connect(self.setTotal)
        self.lamapinjam.valueChanged.connect(self.setTempo)
        self.cari_nik.clicked.connect(self.getAnggota)

        self.hapus.clicked.connect(self.hapusPinjaman)
        self.cari.clicked.connect(lambda : self.cariPinjaman(self.txtcari.text()))
        self.txtcari.returnPressed.connect(lambda : self.cariPinjaman(self.txtcari.text()))

        self.setWindowTitle('Pinjaman')

    def autocode(self):
        model = QSqlTableModel()
        query = QSqlQuery("select max(id_pinjam) as codepinjam from pinjaman")
        model.setQuery(query)
        code = model.record(0).value('codepinjam')
        if code == '':
            autocode = 1
        else:
            autocode = int(code[3:]) + 1
        self.kd_pinjam.setText('PJM{:04d}'.format(autocode))

    def tampilPinjaman(self):
        query = QSqlQuery("SELECT a.nik, a.nama, p.* FROM anggota a, pinjaman p where a.nik=p.nik")
        self.model.setQuery(query)
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model.select()
        self.model.setHeaderData(0, Qt.Horizontal, "Kode Anggota")
        self.model.setHeaderData(1, Qt.Horizontal, "Nama")
        self.model.setHeaderData(2, Qt.Horizontal, "Kode Pinjam")
        self.model.setHeaderData(4, Qt.Horizontal, "Jumlah")
        self.model.setHeaderData(5, Qt.Horizontal, "Bunga")
        self.model.setHeaderData(6, Qt.Horizontal, "Tanggal Pinjam")
        self.model.setHeaderData(7, Qt.Horizontal, "Lama Pinjam")
        self.model.setHeaderData(8, Qt.Horizontal, "Jatuh Tempo")
        self.model.setHeaderData(9, Qt.Horizontal, "Jumlah Bayar")
        self.model.setHeaderData(10, Qt.Horizontal, "Sisa Bayar")
        self.model.setHeaderData(11, Qt.Horizontal, "Status")
        self.tableView.setModel(self.model)

        self.tableView.setColumnHidden(3, True)
        self.tableView.setColumnWidth(0, 120)
        self.tableView.setColumnWidth(1, 170)
        self.tableView.setColumnWidth(5, 50)

    def savePinjaman(self):
        nik = self.nik.text()
        kode = self.kd_pinjam.text()
        jumlah = self.jumlah.text()
        bunga = self.bunga.value()
        lama_pinjam = self.lamapinjam.value()
        jml_bayar = self.total.text()
        tgl_pinjam = self.tgl_pinjam.text().replace('/','-')
        jth_tempo = self.jatuh_tempo.text().replace('/','-')
        if nik == "" or kode == "" or jumlah == "" or bunga == "" or lama_pinjam == "" or jml_bayar == "":
            self.notif.setText('Harap Lengkapi isian anda !')
        else:
            self.notif.setText('')
            query = QSqlQuery()
            if query.exec_("insert into pinjaman values('" + kode + "','" + nik + "','" + jumlah + "','" + str(bunga) + "','" + tgl_pinjam + "','" + str(lama_pinjam) + "','" + jth_tempo + "','" + jml_bayar + "','" + jml_bayar + "','Belum Lunas')"):
                self.message.setText(" ** Data berhasil ditambahkan ke database **")
                self.message.exec_()
                self.clear()
                self.autocode()
                self.tampilPinjaman()

    def setTotal(self):
        jumlah = self.jumlah.text()
        bunga = self.bunga.value()
        lama = self.lamapinjam.value()
        if jumlah != "" and lama != 0:
            bunga = self.main.hitungBunga(int(jumlah), bunga, lama)
            self.total.setText(str(bunga))

    def setTempo(self):
        tanggal = self.tgl_pinjam.date()
        bulan = self.lamapinjam.value()
        self.jatuh_tempo.setDate(tanggal.addMonths(bulan))
        self.setTotal()

    def getAnggota(self):
        anggota = dialogAnggota.DialogAnggota()
        anggota.exec_()
        self.nik.setText(anggota.datanik)

    def hapusPinjaman(self):
        query = QSqlQuery()
        index = self.tableView.currentIndex().row()
        datamodel = self.tableView.model()
        kode_pinjam = datamodel.data(datamodel.index(index, 2), 0)
        query.exec_("delete from pinjaman where id_pinjam='"+kode_pinjam+"'")
        query.exec_("delete from angsuran where id_pinjam='"+kode_pinjam+"'")
        self.tampilPinjaman()
        self.main.angsuran.tampilAngsuran()
        self.autocode()

    def clear(self):
        self.nik.setText('')
        self.jumlah.setText('')
        self.bunga.setValue(0)
        self.lamapinjam.setValue(0)
        self.total.setText('')
        self.tgl_pinjam.setDate(QDate.currentDate())
        self.jatuh_tempo.setDate(QDate.currentDate())

    def cariPinjaman(self,filter):
        query = QSqlQuery("SELECT a.nik, a.nama, p.* FROM anggota a, pinjaman p where a.nik=p.nik AND (a.nik LIKE '%" + filter + "%' OR a.nama LIKE '%" + filter + "%' OR p.id_pinjam LIKE '%" + filter + "%' OR p.tgl_pinjam LIKE '%" + filter + "%'OR p.jatuh_tempo LIKE '%" + filter + "%' OR p.status LIKE '%" + filter + "%')")
        self.model.setQuery(query)
        self.tableView.setModel(self.model)