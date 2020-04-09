B=["ID отдела","Название","Артикул","Дата поступки","Срок хранения","Цена оптом","Цена розница","Кол-во",""]
self.tableWidget = QTableWidget(self.tab2)
self.tableWidget.setRowCount(count1)
self.tableWidget.setColumnCount(9)
self.tableWidget.setColumnWidth(8,30)
self.tableWidget.setColumnWidth(0,120)
self.tableWidget.resize(920,400)
self.tableWidget.setHorizontalHeaderLabels(B)
cursor.execute("SELECT * FROM tovar")
rows = cursor.fetchall()
countTID=0
for row in rows:
    self.tableWidget.setItem(countTID,0, QTableWidgetItem(str(row.id_otdela)))
    self.tableWidget.setItem(countTID,1, QTableWidgetItem(str(row.nazvanie)))
    self.tableWidget.setItem(countTID,2, QTableWidgetItem(str(row.artikul)))
    self.tableWidget.setItem(countTID,3, QTableWidgetItem(str(row.data_postupki)))
    self.tableWidget.setItem(countTID,4, QTableWidgetItem(str(row.srok_kh)))
    self.tableWidget.setItem(countTID,5, QTableWidgetItem(str(row.cena_optom)))
    self.tableWidget.setItem(countTID,6, QTableWidgetItem(str(row.cena_roznica)))
    self.tableWidget.setItem(countTID,7, QTableWidgetItem(str(row.kolichestvo)))
    self.tableWidget.setCellWidget(countTID,8,QCheckBox())
    countTID+=1
    self.tableWidget.show()