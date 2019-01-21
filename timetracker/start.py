import openpyxl
import datetime

comming_time = datetime.datetime.now()
filename = "example.xlsx"

wb = openpyxl.load_workbook(filename)
sheet = wb.get_sheet_by_name('Tabelle1')

cell = 'C' + str(8 + comming_time.timetuple().tm_yday)
sheet[cell] = comming_time.time()

# Insert SOLL
cell = 'K' + str(8 + comming_time.timetuple().tm_yday)
sheet[cell] = 4

wb.save(filename)