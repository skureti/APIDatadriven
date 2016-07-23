import xlrd

def getDataFromSpreadsheet(fileName, sheetname) :
    workbook = xlrd.open_workbook(fileName)
    worksheet = workbook.sheet_by_name(sheetname)
    print worksheet
    rowEndIndex = worksheet.nrows - 1
    print "Total Rows in Excel sheet %r." % rowEndIndex
    colEndIndex = worksheet.ncols - 1

    print "Total Columns in Excel sheet %r." % colEndIndex
    rowStartIndex = 1
    colStartIndex = 0
    dataRow = []
    curr_row = rowStartIndex
    while curr_row <= rowEndIndex:
         cur_col = colStartIndex
         while cur_col <= colEndIndex:
             value = worksheet.cell_value(curr_row, cur_col)
             dataRow.append(value)
             cur_col+=1
         curr_row += 1
    return dataRow