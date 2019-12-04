from PyQt5.QtSql import QSqlQuery
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMdiSubWindow, QMessageBox, QLineEdit


class Login(QMdiSubWindow):
    def __init__(self,main=None):
        self.main = main
        super().__init__()
        loadUi('./ui/login.ui', self)
        self.setWindowTitle('Login')
        self.login.clicked.connect(self.cekLogin)
        self.username.returnPressed.connect(self.cekLogin)
        self.password.returnPressed.connect(self.cekLogin)
        self.checkBox.clicked.connect(self.showHide)

    def cekLogin(self):
        message = QMessageBox()
        query = QSqlQuery()
        username = self.username.text()
        password = self.password.text()
        if username != '' and password != '':
            query.exec_("SELECT * FROM petugas WHERE username='"+username+"' AND password='"+password+"'")
            if query.next():
                self.notif.setText('')
                self.main.Petugas.setVisible(True)
                self.main.Anggota.setVisible(True)
                self.main.Jenis.setVisible(True)
                self.main.Simpanan.setVisible(True)
                self.main.Penarikan.setVisible(True)
                self.main.Daftar_Simpanan.setVisible(True)
                self.main.Pinjaman.setVisible(True)
                self.main.Angsuran.setVisible(True)
                self.main.Login.setVisible(False)
                message.setText(' ** Anda Berhasil Login ** ')
                message.exec_()
                self.close()
                self.main.mdi.addSubWindow(self.main.dash)
                self.main.dash.showMaximized()
            else:
                self.notif.setText('Username atau Password Anda Salah !!')
        else:
            self.notif.setText('Masukkan username dan password anda !!')

    def showHide(self):
        if self.checkBox.isChecked():
            self.password.setEchoMode(QLineEdit.Normal)
        else:
            self.password.setEchoMode(QLineEdit.Password)