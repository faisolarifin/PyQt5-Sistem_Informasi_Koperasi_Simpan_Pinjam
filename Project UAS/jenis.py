from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtSql import QSqlTableModel, QSqlQuery
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMdiSubWindow, QMessageBox


class Jenis(QMdiSubWindow):
    def __init__(self):
        super().__init__()
        loadUi('./ui/jenis.ui', self)

        self.message = QMessageBox()
        self.model = QSqlTableModel()
        self.clear()
        self.tampilkanJenis()

        self.simpan.clicked.connect(self.simpanJenis)
        self.hapus.clicked.connect(self.hapusJenis)

        self.setWindowTitle('Jenis')

    def tampilkanJenis(self):
        self.model.setTable('jenis')
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model.select()
        self.model.setHeaderData(0, Qt.Horizontal, "Kode Jenis")
        self.model.setHeaderData(1, Qt.Horizontal, "Nama Jenis")
        self.model.setHeaderData(2, Qt.Horizontal, "Keterangan")
        self.tableView.setModel(self.model)
        self.tableView.setColumnWidth(1, 150)
        self.tableView.setColumnWidth(2, 430)

    def simpanJenis(self):
        jenis = self.jenis.text()
        desc = self.desc.toPlainText()
        if jenis == "" or desc == "":
            self.notif.setText('Masukkan data dengan banar !')
        else:
            self.notif.setText('')
            query = QSqlQuery()
            if query.exec_("insert into jenis values(null,'"+jenis +"','"+desc+"')"):
                self.message.setText(" ** Data berhasil ditambahkan ke database **")
                self.message.exec_()
                self.tampilkanJenis()
                self.clear()

    def hapusJenis(self):
        self.model.removeRow(self.tableView.currentIndex().row())
        self.model.select()
        self.tampilkanJenis()

    def clear(self):
        self.jenis.setText('')
        self.desc.setPlainText('')