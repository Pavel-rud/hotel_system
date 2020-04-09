from docxtpl import DocxTemplate
import xlsxwriter
import xlrd, xlwt
import csv
import pandas as pd


def admin_and_guest(surname_guest, name_guest, name_guest_father, hotel,
                    room, surname_admin, name_admin, name_guest_admin, date, action, location):
    doc = DocxTemplate("example_document_for_admin_and_guest.docx")
    context = {'surname_guest': surname_guest,
               'name_guest': name_guest,
               'name_guest_father': name_guest_father,
               'hotel': hotel,
               'room': room,
               'surname_admin': surname_admin,
               'name_admin': name_admin,
               'name_guest_admin': name_guest_admin,
               'date': date,
               'action': action}
    doc.render(context)
    doc.save(f"{location}.docx")


def info_about_guests(guests, location):
    data = []
    for i in guests:
        data.append({"фамилия": i[0],
                     "имя": i[1],
                     "отчество": i[2],
                     "дата рождения": i[3],
                     "пол": i[4],
                     "номер телефона": i[5],
                     "паспортные данные": i[6]})
    pd.DataFrame(data).to_csv(f'{location}.csv', index=False)


def write_time(time, chance):
    f = open('time_block.txt', 'w')
    f.write(time + '\n')
    f.write(chance)


def read_time():
    f = open('time_block.txt')
    first = True
    lines = []
    for line in f:
        lines.append(line)
    return lines[0][:-1], lines[1]


def read_info_about_administrators(location):
    rb = xlrd.open_workbook(location)
    page = rb.sheet_by_index(0)
    admistrators = [page.row_values(rownum) for rownum in range(1, page.nrows)]
    return admistrators


# info_about_guests([["ad", "dada", "ad", "dada", "ad", "dada", "ad", "dada"], ["dfdad", "dadaadda", "adaadd", "daddada", "addads", "dada", "ad", "dada"]], "g")
# write_time("09:55", "2")
# print(read_time())
# read_info_about_administrators()
# admin_and_guest("Rudnik", "Pavel", "Alekseevich", "grand", "7", "rey", "maks", "sergeevich", "10.20.10", "выселение")