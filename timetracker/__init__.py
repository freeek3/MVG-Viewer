import datetime
import sys

import openpyxl

TIME = datetime.datetime.now()
FILENAME = 'example.xlsx'
SHEET = 'worktime'
START = 'C'
END = 'D'
START_PAUSE = 'F'
END_PAUSE = 'G'
SOLL = 'K'
OFFSET = 8

name = "timetracker"


def writetofile(f, sheet, col, offset, val):
    '''

    :param f: filename
    :param sheet: Excel sheet
    :param col: Colunm of Cell
    :param offset: offset of Cell
    :param val: Value to write to Cell
    :return: -
    '''
    wb = openpyxl.load_workbook(f)
    sheet = wb.get_sheet_by_name(sheet)
    cell = col + str(offset + val.timetuple().tm_yday)
    sheet[cell] = val
    wb.save(f)


def main():
    if len(sys.argv) == 2:
        if sys.argv[1] == 'startpause':
            writetofile(FILENAME, SHEET, START_PAUSE, OFFSET, TIME)
        elif sys.argv[1] == 'endpause':
            writetofile(FILENAME, SHEET, END_PAUSE, OFFSET, TIME)
        elif sys.argv[1] == 'start':
            writetofile(FILENAME, SHEET, START, OFFSET, TIME)
        elif sys.argv[1] == 'end':
            writetofile(FILENAME, SHEET, END, OFFSET, TIME)
    else:
        print("Wrong Parameter")
        print("start, end, startpause or endpause")


if __name__ == '__main__':
    main()
