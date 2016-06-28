import cgi
import os
import xlrd


class excelHelper():
    
    def readExcel(self,xfile,start,end):
        rows=[]
        book = xlrd.open_workbook(xfile)
        sheet = book.sheet_by_index(0)
        for rownum in range(sheet.nrows):
            if rownum > start and rownum <= end:
                rows.append(sheet.row_values(rownum))
        return rows