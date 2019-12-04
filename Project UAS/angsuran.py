from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtSql import QSqlTableModel, QSqlQuery
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMdiSubWindow, QMessageBox

import dialogAnggota

class Angsuran(QMdiSubWindow):
    def __init__(self,main=None):
        super().__init__()
        self.main = main
        loadUi('./ui/angsuran.ui', self)

        self.message = QMessageBox()
        self.model = QSqlTableModel()

        self.clear()
        self.tampilAngsuran()

        self.simpan.clicked.connect(self.simpanAngsuran)
        self.cari_nik.clicked.connect(self.getAnggota)
        self.hapus.clicked.connect(self.hapusAngsuran)
        self.cari.clicked.connect(lambda : self.cariPetugas(self.txtcari.text()))
        self.txtcari.returnPressed.connect(lambda : self.cariAngsuran(self.txtcari.text()))

        self.setWindowTitle('Angsuran')

    def tampilAngsuran(self):
        query = QSqlQuery("SELECT a.nik, a.nama, p.id_pinjam, p.jumlah_bayar, ang.* FROM anggota a, pinjaman p, angsuran ang where a.nik=ang.nik and p.id_pinjam=ang.id_pinjam")
        self.model.setQuery(query)
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model.select()
        self.model.setHeaderData(0, Qt.Horizontal, "Kode Anggota")
        self.model.setHeaderData(1, Qt.Horizontal, "Nama")
        self.model.setHeaderData(2, Qt.Horizontal, "Kode Pinjam")
        self.model.setHeaderData(3, Qt.Horizontal, "Total Bayar")
        self.model.setHeaderData(7, Qt.Horizontal, "Jumlah Angsuran")
        self.model.setHeaderData(8, Qt.Horizontal, "Angsuran Ke")
        self.model.setHeaderData(9, Qt.Horizontal, "Tanggal Angsuran")
        self.tableView.setModel(self.model)

        self.tableView.setColumnHidden(4,True)
        self.tableView.setColumnHidden(5,True)
        self.tableView.setColumnHidden(6,True)
        self.tableView.setColumnWidth(0, 150)
        self.tableView.setColumnWidth(1, 170)

    def simpanAngsuran(self):
        nik = self.nik.text()
        kd_pinjam = self.kd_pinjam.text()
        jumlah = self.jumlah.text()
        angsur = self.angsuran.text()
        tanggal = self.tanggal.text().replace('/','-')
        query = QSqlQuery()
        query.exec_("select nik, id_pinjam from pinjaman where nik='"+nik+"' and id_pinjam='"+kd_pinjam+"'")
        if query.next():
            query.exec_("insert into angsuran values(null,'" + nik + "','" + kd_pinjam + "','" + jumlah + "','" + angsur + "', '" + tanggal + "')")
            query.exec_("update pinjaman set sisa=(select sisa from pinjaman where nik='"+nik+"' and id_pinjam='"+kd_pinjam+"') - "+jumlah+" where nik='"+nik+"' and id_pinjam='"+kd_pinjam+"'")
            self.message.setText("** Data berhasil ditambahkan ke database **")
            self.message.exec_()
            self.clear()
            self.tampilAngsuran()
            self.main.pinjaman.tampilPinjaman()
        else:
            self.message.setText("** Anggota tidak ditemukan **")
            self.message.exec_()

    def getAnggota(self):
        anggota = dialogAnggota.DialogAnggota()
        anggota.exec_()
        self.nik.setText(anggota.datanik)

        if anggota.datanik != '':
            query = QSqlQuery()
            query.exec_("select id_pinjam from pinjaman where nik='"+anggota.datanik+"' and status like '%belum lunas%'")
            if query.next():
                kd_pinjam = query.value(0)
                self.kd_pinjam.setText(kd_pinjam)
                query.exec_("SELECT pinjaman.id_pinjam, pinjaman.jumlah, pinjaman.bunga, pinjaman.lama_pinjam, angsuran.id_pinjam, max(angsuran.angsur_ke) as angsur FROM pinjaman LEFT JOIN angsuran ON pinjaman.id_pinjam = angsuran.id_pinjam where pinjaman.id_pinjam='"+kd_pinjam+"' or angsuran.id_pinjam='"+kd_pinjam+"'")
                if query.next():
                    bulan_ke = query.value(5)
                    if bulan_ke == '':
                        bulan_ke = 1
                    else:
                        bulan_ke += 1
                    self.jumlah.setText(str(self.main.hitungBunga(query.value(1), query.value(2), query.value(3), bulan_ke)))
                    self.angsuran.setText(str(bulan_ke))
            else:
                self.message.setText("** Pinjaman anggota tersebut tidak ditemukan ! **")
                self.message.exec_()
                self.clear()

    def hapusAngsuran(self):
        query = QSqlQuery()
        index = self.tableView.currentIndex().row()
        datamodel = self.tableView.model()
        kode_angsur = datamodel.data(datamodel.index(index, 4), 0)
        query.exec_("delete from angsuran where id_angsuran='"+str(kode_angsur)+"'")
        self.tampilAngsuran()

    def clear(self):
        self.nik.setText('')
        self.kd_pinjam.setText('')
        self.jumlah.setText('')
        self.angsuran.setText('')
        self.tanggal.setDateTime(QDateTime.currentDateTime())

    def cariAngsuran(self,filter):
        query = QSqlQuery("SELECT a.nik, a.nama, p.id_pinjam, p.jumlah_bayar, ang.* FROM anggota a, pinjaman p, angsuran ang where a.nik=ang.nik and p.id_pinjam=ang.id_pinjam AND  (a.nik LIKE '%" + filter + "%' OR a.nama LIKE '%" + filter + "%' OR p.id_pinjam LIKE '%" + filter + "%' OR ang.tgl_angsur LIKE '%" + filter + "%')")
        self.model.setQuery(query)
        self.tableView.setModel(self.model)