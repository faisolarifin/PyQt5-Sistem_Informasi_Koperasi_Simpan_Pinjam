from PyQt5.uic import loadUi
from PyQt5.QtSql import QSqlTableModel, QSqlQuery
from PyQt5.QtWidgets import QDialog


class DialogAnggota(QDialog):
    def __init__(self):
        super().__init__()
        loadUi('./ui/dialog anggota.ui',self)
        self.datanik = ""
        self.model = QSqlTableModel()

        self.setData()
        self.move(100,120)
        self.setWindowTitle('Anggota')

        self.tombol.clicked.connect(self.getData)
        self.text.textChanged.connect(lambda : self.cariAnggota(self.text.text()))

    def setData(self):
        self.model.setTable('anggota')
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model.select()
        self.table.setModel(self.model)
        self.table.setColumnWidth(0, 120)
        self.table.setColumnWidth(1, 150)

    def getData(self):
        index = self.table.currentIndex().row()
        datamodel = self.table.model()
        self.datanik = datamodel.data(datamodel.index(index, 0), 0)
        self.close()

    def cariAnggota(self, filter):
        query = QSqlQuery("SELECT * FROM anggota WHERE nik LIKE '%" + filter + "%' OR nama LIKE '%" + filter + "%'OR alamat LIKE '%" + filter + "%'")
        self.model.setQuery(query)
        self.table.setModel(self.model)