import openpyxl
import datetime

comming_time = datetime.datetime.now()
filename = "example.xlsx"

wb = openpyxl.load_workbook(filename)
sheet = wb.get_sheet_by_name('Tabelle1')

cell = 'D' + str(8 + comming_time.timetuple().tm_yday)
sheet[cell] = comming_time

wb.save(filename)

