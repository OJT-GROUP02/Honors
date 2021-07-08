import datetime
import openpyxl
import psycopg2
import itertools

from operator import itemgetter
from openpyxl import Workbook, load_workbook
from openpyxl.utils import get_column_letter
from openpyxl.styles import Border, Side
from openpyxl.styles import Font, Alignment, fills, numbers, PatternFill
from openpyxl.worksheet.dimensions import ColumnDimension
from openpyxl.descriptors.excel import UniversalMeasure, Relation
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.worksheet.pagebreak import Break


def index():
    return dict(message="Hello!")


def uro():
    current_date_uro = str(datetime.datetime.today().strftime('%B %d, %Y'))

    header_uro = db((db.header.college_id == 5) |
                    (db.header.semester == '2nd Semester') |
                    (db.header.academic_year == '2019-2020')).select(
        db.college.college_name, db.college.college_address,
        db.header.semester, db.header.academic_year,
        left=db.college.on(db.header.college_id == db.college.college_id))

    male_students = \
        db((db.student.gender == 'M')).select(
            db.student.last_name, db.student.first_name,
            db.student.middle_name, db.student.gender,
            db.grade.total_units, db.grade.sum_of_grades,
            db.grade.final_gwa, db.awards.award_title,
            left=[db.grade.on(db.student.student_id == db.grade.student_id),
                  db.awards.on(db.grade.award_id == db.awards.award_id)],
            orderby=db.student.last_name)

    female_students = \
        db((db.student.gender == 'F')).select(
            db.student.last_name, db.student.first_name,
            db.student.middle_name, db.student.gender,
            db.grade.total_units, db.grade.sum_of_grades,
            db.grade.final_gwa, db.awards.award_title,
            left=[db.grade.on(db.student.student_id == db.grade.student_id),
                  db.awards.on(db.grade.award_id == db.awards.award_id)],
            orderby=db.student.last_name)

    total_units = 234

    return locals()


def rank():
    current_date_rank = str(datetime.datetime.today().strftime('%B %d, %Y'))

    header_rank = db((db.header.college_id == 5) |
                     (db.header.semester == '2nd Semester') |
                     (db.header.academic_year == '2019-2020')).select(
        db.college.college_name, db.college.college_address,
        db.header.semester, db.header.academic_year,
        left=db.college.on(db.header.college_id == db.college.college_id))

    students_honor = db(db.awards.award_title).select(
        db.student.last_name, db.student.first_name,
        db.student.middle_name, db.student.classification,
        db.grade.total_units, db.grade.sum_of_grades,
        db.grade.final_gwa, db.awards.award_title, orderby=db.grade.final_gwa,
        left=[db.grade.on(db.student.student_id == db.grade.student_id),
              db.awards.on(db.grade.award_id == db.awards.award_id)])

    all_students = db(db.student.classification is None).select(
        db.student.last_name, db.student.first_name,
        db.student.middle_name, db.student.classification,
        db.grade.total_units, db.grade.sum_of_grades,
        db.grade.final_gwa, db.awards.award_title,
        left=[db.grade.on(db.student.student_id == db.grade.student_id),
              db.awards.on(db.grade.award_id == db.awards.award_id)])

    return locals()


# db connection
def connect(query):
    cur = psycopg2.connect(database='honors', user='postgres',
                           password='april17', host='localhost',
                            port="5432").cursor()
    # cur = psycopg2.connect(database='honorsdb', user='postgres',
    #                        password='1612', host='localhost',
    #                         port="5432").cursor()
    cur.execute(query)
    desc = cur.description
    column_names = [col[0] for col in desc]
    result = [dict(itertools.zip_longest(column_names, row)) for row in cur.fetchall()]
    # result = cur.fetchall()

    return result


# QUERIES

# fetch header data
# header_query = "SELECT header.header_id, college.college_name, " \
#                "college.college_address, header.semester, " \
#                "header.academic_year FROM header LEFT JOIN college on " \
#                "college.college_id = header.college_id WHERE " \
#                "college.college_name = 'College of Social Sciences and Philosophy' \
#                AND header.semester = '2nd Semester' AND " \
#                "academic_year = '2019-2020'"

header_query = "SELECT header.header_id, college.college_name, " \
               "college.college_address, header.semester, " \
               "header.academic_year FROM header LEFT JOIN college on " \
               "college.college_id = header.college_id WHERE " \
               "college.college_name = 'College of Business, Economics, " \
               "and Management' \
               AND header.semester = '2nd Semester' AND " \
               "academic_year = '2019-2020'"

header = connect(header_query)
college_name = header[0]["college_name"]
college_name_upper = header[0]["college_name"].upper()
college_address = header[0]["college_address"]
college_semester = header[0]["semester"]
academic_year = header[0]["academic_year"]

# fetch student data
m_student_query = "SELECT CONCAT(student.first_name, ' ', " \
                  "student.middle_name, ' ', student.last_name) AS " \
                  "full_name, grade.total_units, grade.sum_of_grades, " \
                  "grade.final_gwa, awards.award_title FROM student " \
                  "LEFT JOIN grade ON student.student_id = grade.student_id " \
                  "LEFT JOIN awards ON awards.award_id = grade.award_id " \
                  "WHERE student.gender = 'M' ORDER BY student.last_name"

f_student_query = "SELECT CONCAT(student.first_name, ' ', " \
                  "student.middle_name, ' ', student.last_name) AS " \
                  "full_name, grade.total_units, grade.sum_of_grades, " \
                  "grade.final_gwa, awards.award_title FROM student " \
                  "LEFT JOIN grade ON student.student_id = grade.student_id " \
                  "LEFT JOIN awards ON awards.award_id = grade.award_id " \
                  "WHERE student.gender = 'F' ORDER BY student.last_name"

m_students = connect(m_student_query)
m_total_rows = len(m_students)
f_students = connect(f_student_query)
f_total_rows = len(f_students)
minimum_row = 19    # for table
maximum_col = 6     # for table
total_units = 234

# WORKBOOK

wb = Workbook()

wb.create_sheet("Rank", 0)
wb.create_sheet("URO", 1)

ws = wb["URO"]
ColumnDimension(ws, auto_size=True)
ws.page_setup.paperHeight = '13in'
ws.page_setup.paperWidth = '8.5in'
ws.page_margins.left = 0.50
ws.page_margins.rigt = 0.50
# ws.print_options.verticalCentered = True
# ws.print_options.horizontalCentered = True

# column sizes
ws.column_dimensions["A"].width = 5
ws.column_dimensions["B"].width = 32
ws.column_dimensions["C"].width = 9
ws.column_dimensions["D"].width = 9
ws.column_dimensions["E"].width = 12
ws.column_dimensions["F"].width = 25

# Heading
ws.append(['Republic of the Philippines'])
ws.merge_cells('A1:F1')
ws.append(['Bicol University'])
ws.merge_cells('A2:F2')
ws.append([college_name_upper])
ws.merge_cells('A3:F3')
ws['A3'].font = Font(bold=True)
ws.append([college_address])
ws.merge_cells('A4:F4')

rows = ws.iter_cols(min_row=1, min_col=1, max_row=4, max_col=6)
for row in rows:
    for cell in row:
        cell.alignment = Alignment(wrap_text=True, horizontal='center', vertical='center')

# rows = range(1, 8)
# columns = range(1, 5)
# for row in rows:
#     for col in columns:
#         ws.cell(row, col).alignment = Alignment(horizontal='center', vertical='center', wrapText=True)

# Date
date = str(datetime.datetime.today().strftime('%B %d, %Y'))
date_today = ws['F5']
date_today.value = date
date_today.alignment = Alignment(horizontal='right')


# Inside Address
ws['A7'].value = "THE BICOL UNIVERSITY REGISTRAR"
ws['A8'].value = "Bicol University"
ws['A9'].value = "Legazpi City"

for row in ws['A7':'F9']:
    for cell in row:
        cell.alignment = Alignment(horizontal='left')

#Attention
for col in range(1, 7):
    ws.column_dimensions[get_column_letter(col)].bestFit=True

ws['A12'].value = "Attn: UNIVERITY EVALUATION/REVIEW COMMITTEE ON HONOR AND GRADUATES"
ws.merge_cells('A12:F12')
ws['A12'].alignment = Alignment(horizontal='center', vertical='center', wrapText=True)

#Greetings
ws['A15'].value = "Sir/Madam:"
ws['A15'].alignment = Alignment(horizontal='left')

#Letter Body

for row in range (16, 18):
   ws.row_dimensions[(row)].bestFit=True

ws['A16'].value = "Herewith are the Official List of Candidates for Graduation with Honors under the different"
ws['A16'].alignment = Alignment(horizontal='left', indent=2)
ws.merge_cells('A16:F16')

ws['A17'].value = f"degree programs of the {college_name}  for the {college_semester}, {academic_year}."
ws['A17'].alignment = Alignment(horizontal='left')
ws.merge_cells('A17:F17')

#table

thin = Side(border_style="thin", color="000000")# border style, color
border = Border(left=thin, right=thin, top=thin, bottom=thin)# the position of the border

rows = ws.iter_cols(min_row=19, min_col=1,
                    max_row=minimum_row + m_total_rows + f_total_rows + 3,
                    max_col=6)

# border
for row in rows:
    for cell in row:
        cell.border = border

#center table contents
rows = ws.iter_cols(min_row=19, min_col=1,
                    max_row=minimum_row + m_total_rows + f_total_rows + 3,
                    max_col=6)
for row in rows:
    for cell in row:
        cell.alignment = Alignment(horizontal='center', vertical='center', wrapText=True)

# table header
ws['A19'].value = "NO."
ws.merge_cells(start_row=19, start_column=1, end_row=20, end_column=1)
ws['B19'].value = "NAME"
ws.merge_cells(start_row=19, start_column=2, end_row=20, end_column=2)
ws['C19'].value = "RATING"
ws.merge_cells('C19:E19')
ws['C20'].value = "Sum of Grades"
ws['D20'].value = "Total Units"
ws['E20'].value = "Final GWA"
ws['F19'].value = "AWARD"
ws.merge_cells(start_row=19, start_column=6, end_row=20, end_column=6)

bold_font = Font(bold=True)
for cell in ws["19:19"]:
    cell.font = bold_font
for cell in ws["20:20"]:
    cell.font = bold_font

font_size = Font(name='Calibri', size=9)
rows = ws.iter_cols(min_row=21, min_col=1,
                    max_row=minimum_row + m_total_rows + f_total_rows + 3,
                    max_col=6)
for row in rows:
    for cell in row:
        cell.font = font_size

# male students
ws['A21'].value = "MALE"
ws['A21'].font = Font(name='Calibri', size=9, bold=True)
ws.merge_cells('A21:F21')

key_list = ["full_name", "sum_of_grades", "total_units", "final_gwa",
            "award_title"]

min_row_m = minimum_row + 3
max_row_m = min_row_m + m_total_rows
count = 1

temp_row = min_row_m
for m_student in m_students:
    list_index = 0
    ws['A' + str(temp_row)].value = count

    if m_student[key_list[2]] is not None:
        if m_student[key_list[2]] < total_units:
            ws['A' + str(temp_row)].fill = \
                PatternFill(fill_type='solid', fgColor="f0e68c")

    for col_table in range(2, 7):
        char = get_column_letter(col_table)
        ws[char + str(temp_row)] = m_student[key_list[list_index]]

        if m_student[key_list[3]] is not None:
            if list_index == 3:
                ws[char + str(temp_row)].font = \
                    Font(name='Calibri', size=9, bold=True)

        # yellow fill (row)
        if m_student[key_list[2]] is not None:
            if m_student[key_list[2]] < total_units:
                ws[char + str(temp_row)].fill = \
                    PatternFill(fill_type='solid', fgColor="f0e68c")

        # red fill (cell)
        if m_student[key_list[list_index]] is not None:

            if list_index == 3 and m_student[key_list[list_index]] <= 1.75:
                ws[char + str(temp_row)].font = \
                    Font(color="9d0008", name='Calibri', size=9, bold=True)
                ws[char + str(temp_row)].fill = \
                    PatternFill(fill_type='solid', fgColor="fbc3cb")
        list_index += 1

    temp_row += 1
    count += 1

# female students
min_row_f = minimum_row + min_row_m + 2
max_row_f = min_row_f + f_total_rows
count = 1

ws['A' + str(min_row_f - 1)].value = "FEMALE"
ws['A' + str(min_row_f - 1)].font = Font(name='Calibri', size=9, bold=True)
range_f_min = 'A' + str(min_row_f - 1)
range_f_max = 'F' + str(min_row_f - 1)
ws.merge_cells(f'{str(range_f_min)}:{str(range_f_max)}')

temp_row = min_row_f
for f_student in f_students:
    list_index = 0
    ws['A' + str(temp_row)].value = count

    if f_student[key_list[2]] is not None:
        if f_student[key_list[2]] < total_units:
            ws['A' + str(temp_row)].fill = \
                PatternFill(fill_type='solid', fgColor="f0e68c")

    for col_table in range(2, 7):
        char = get_column_letter(col_table)
        ws[char + str(temp_row)] = f_student[key_list[list_index]]

        if f_student[key_list[3]] is not None:
            if list_index == 3:
                ws[char + str(temp_row)].font = \
                    Font(name='Calibri', size=9, bold=True)

        # yellow fill (row)
        if f_student[key_list[2]] is not None:
            if f_student[key_list[2]] < total_units:
                ws[char + str(temp_row)].fill = \
                    PatternFill(fill_type='solid', fgColor="f0e68c")

        # red fill (cell)
        if f_student[key_list[list_index]] is not None:
            if list_index == 3 and f_student[key_list[list_index]] <= 1.75:
                ws[char + str(temp_row)].font = \
                    Font(color="9d0008", name='Calibri', size=9, bold=True)
                ws[char + str(temp_row)].fill = \
                    PatternFill(fill_type='solid', fgColor="fbc3cb")

        list_index += 1

    temp_row += 1
    count += 1

total_rows_after_table = minimum_row + min_row_m + f_total_rows + 3

ws['A' + str(total_rows_after_table)].value = "Note: Subject for verification/recommendation/approval by the University Evaluation/Review"
ws['A' + str(total_rows_after_table)].alignment = Alignment(horizontal='left', indent=2)
range_min = 'A' + str(total_rows_after_table)
range_max = 'F' + str(total_rows_after_table)
ws.merge_cells(f'{str(range_min)}:{str(range_max)}')
ws['A' + str(total_rows_after_table + 1)].value = "Committee on Honor " \
                                                  "Graduates"
ws['A' + str(total_rows_after_table + 1)].alignment = Alignment(
    horizontal='left', indent=6)
range_min = 'A' + str(total_rows_after_table + 1)
range_max = 'F' + str(total_rows_after_table + 1)
ws.merge_cells(f'{str(range_min)}:{str(range_max)}')
ws.merge_cells(f'{str(range_min)}:{str(range_max)}')

# wb.save('static/Honors.xlsx')
# ivee
wb.save('D:\\Users\\iveej\\Desktop\\web2py\\applications\\honors\\static'
        '\\Honors.xlsx')
