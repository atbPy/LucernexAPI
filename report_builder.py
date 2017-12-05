import os
from openpyxl import Workbook
from openpyxl import load_workbook
from collections import defaultdict

data = defaultdict(dict)

data = {'68701': {'CustomCodeTableID': {'RecID': '5080', 'Name': 'Radius Unit'}, 'CustomCodeFieldName': 'Kilometer(s)'},
        '68702': {'CustomCodeTableID': {'RecID': '5080', 'Name': 'Radius Unit'}, 'CustomCodeFieldName': 'Meter(s)'},
        '68703': {'CustomCodeTableID': {'RecID': '5080', 'Name': 'Radius Unit'}, 'CustomCodeFieldName': 'Mile(s)'}}

field = "CustomCodeField"

file = "C:/Users/abednar/PycharmProjects/LucernexAPI/Templates/RadiusUnit.xlsx"


def build_field_dict_from_template(file, field):
    wb = load_workbook(filename=file)
    ws = wb.get_sheet_by_name(field)
    columns = ws.max_column

    field_dict = {}
    index_number = 4

    row_two = ws[2]
    for column in ws.iter_cols(min_row=2, min_col=5, max_col=columns, max_row=2):
        index_number += 1
        print(column)
        for cell in column:
            print(cell.value)
            field_to_split = cell.value
            field = field_to_split.split(".")
            field_dict[index_number] = field[1]

    return field_dict


def write_to_excel(data, field, file):
    row_number = 3
    wb = load_workbook(filename=file)
    ws = wb.get_sheet_by_name(field)

    fields_dict = build_field_dict_from_template(file, "CustomCodeField")

    for item in data:
        row_number += 1

        # Each row needs Payment in the first column
        ws.cell(column=2, row=row_number, value=field)
        ws.cell(column=4, row=row_number, value=item)

        for fields in fields_dict:
            field_name = fields_dict[fields]
            try:
                if isinstance(data[item][field_name], dict):
                    text_value = data[item][field_name]['Name']
                else:
                    text_value = data[item][field_name]
            except KeyError:
                # Do not populate anything for empty keys
                text_value = ""

            ws.cell(column=fields, row=row_number, value=text_value)

    wb.save("C:/Users/abednar/PycharmProjects/LucernexAPI/Templates/RadiusUnit-test.xlsx")


# build_field_dict_from_template(file, "CustomCodeField")
a = write_to_excel(data, "CustomCodeField", file)
