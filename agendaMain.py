from agendaD import *
import sys
import sqlite3
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QTableWidgetItem


class agenda(QMainWindow,Ui_MainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)
        super().setupUi(self)
        self.update = False
        self.index = None
        self.operacao_bd(sql = 'CREATE TABLE IF NOT EXISTS agenda(nome VARCHAR(100) NOT NULL, telefone VARCHAR(11) PRIMARY KEY NOT NULL, email VARCHAR(100))')
        self.saveButton.clicked.connect(self.salvar)
        self.excluirBtn.clicked.connect(self.excluir)
        self.editarBtn.clicked.connect(self.editar)
        self.novoBtn.clicked.connect(self.novo)
        self.tableView.setColumnCount(3)
        self.tableView.setHorizontalHeaderLabels(['Nome','Telefone','Email'])
        self.atualizar_tabela()


    def operacao_bd(self, sql, retorno = False):
        try:
            conexao = sqlite3.connect('agendaBD.db')
            cursor = conexao.cursor()
            
            if not retorno:
                cursor.execute(sql)
                conexao.commit()
                cursor.close()
                conexao.close()
                return True
            else:
                cursor.execute(sql)
                dados = []
                for data in cursor.fetchall():
                    registro = {'nome': data[0], 'telefone': data[1], 'email': data[2]}
                    dados.append(registro)
                    
                cursor.close()
                conexao.close()
                return dados

        except Exception as e:
            QMessageBox.about(self, "Erro", f'Erro: {e} ')


    def atualizar_tabela(self):
        linha = 0
        sql = 'SELECT * FROM agenda ORDER BY nome ASC'
        dados = self.operacao_bd(sql, retorno = True)
        self.tableView.setRowCount(len(dados))

        for dado in dados:
            nome =  QTableWidgetItem(dado['nome'])
            nome.setFlags( QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled )
            telefone = QTableWidgetItem(dado['telefone'])
            telefone.setFlags( QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled )
            email = QTableWidgetItem(dado['email'])
            email.setFlags( QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled )
            self.tableView.setItem(linha, 0 ,nome)
            self.tableView.setItem(linha, 1,telefone )
            self.tableView.setItem(linha, 2, email)
            linha += 1


    def get_dados_tabela(self, index = False):
        indexes = []
        for selectionRange in self.tableView.selectedRanges(): 
            indexes.extend(range(selectionRange.topRow()+1))
        if index:
         indice = self.tableView.item(indexes[-1], 1).text() 
         return indice
        else:
            dados = {'nome':self.tableView.item(indexes[-1], 0).text(), 'telefone':self.tableView.item(indexes[-1], 1).text(), 'email':self.tableView.item(indexes[-1], 2).text()}
            return dados

    def salvar(self):

        if self.update:
            sql = f'UPDATE agenda SET nome ="{self.nomeLine.text()}", telefone = "{self.telLine.text()}", email = "{self.emailLine.text()}" WHERE telefone = "{self.index}"'
            if self.operacao_bd(sql):
                QMessageBox.about(self, "Sucesso", "Contato Aualizado com sucesso !")
                self.atualizar_tabela()
                self.update = False
                self.index = None
                self.novo()
        else:
            sql = 'INSERT INTO agenda (nome,telefone,email) VALUES("' + self.nomeLine.text() + '", "' + self.telLine.text() + '", "' + self.emailLine.text()+'")'
            if self.operacao_bd(sql):
                QMessageBox.about(self, "Sucesso", "Contato adicionado com sucesso !")
                self.atualizar_tabela()
                self.novo()

    def excluir(self):
        try:
            ID = self.get_dados_tabela(index = True)
            if self.operacao_bd(sql = f'DELETE FROM agenda WHERE telefone ="{ID}"'):
                QMessageBox.about(self, "Sucesso", "Deletado com Sucesso !")
                self.atualizar_tabela()
        except:
            QMessageBox.about(self, "Erro", "Nenhum Contato Selecionado")

    def editar(self):
        try:
            dados = self.get_dados_tabela()
            self.nomeLine.setText(dados["nome"])
            self.telLine.setText(dados["telefone"])
            self.emailLine.setText(dados["email"])
            self.update = True
            self.index = dados["telefone"]
        except:
            QMessageBox.about(self, "Erro", "Nenhum Contato Selecionado")


    def novo(self):
        self.nomeLine.setText("")
        self.telLine.setText("")
        self.emailLine.setText("")
        self.update = False



if __name__ == '__main__':
    qt = QApplication(sys.argv)
    new = agenda()
    new.show()
    qt.exec()
