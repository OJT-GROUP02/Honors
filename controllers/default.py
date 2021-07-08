import datetime
import openpyxl
import psycopg2
import itertools

from operator import itemgetter
from openpyxl import Workbook, load_workbook
from openpyxl.utils import get_column_letter
from openpyxl.styles import Border, Side
from openpyxl.styles import Font, Alignment, fills, numbers
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
    # cur = psycopg2.connect(database='honors', user='postgres',
    #                        password='april17', host='localhost',
    #                         port="5432").cursor()
    cur = psycopg2.connect(database='honorsdb', user='postgres',
                           password='1612', host='localhost',
                            port="5432").cursor()
    cur.execute(query)
    desc = cur.description
    column_names = [col[0] for col in desc]
    result = [dict(itertools.zip_longest(column_names, row)) for row in cur.fetchall()]
    # result = cur.fetchall()

    return result


# QUERIES

# fetch header data
header_query = "SELECT header.header_id, college.college_name, " \
               "college.college_address, header.semester, " \
               "header.academic_year FROM header LEFT JOIN college on " \
               "college.college_id = header.college_id WHERE " \
               "college.college_name = 'College of Social Sciences and Philosophy' \
               AND header.semester = '2nd Semester' AND " \
               "academic_year = '2019-2020'"

header = connect(header_query)
college_name = header[0]["college_name"]
college_name_upper = header[0]["college_name"].upper()
college_address = header[0]["college_address"]
college_semester = header[0]["semester"]
academic_year = header[0]["academic_year"]

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
   
ws['A16'].value = "Herewith are the Official List of Candidates for Graduation with Honors under the different degree programs"
ws['A16'].alignment = Alignment(horizontal='left', indent=1)
ws.merge_cells('A16:F16')

ws['A17'].value = f" of the {college_name}  for the {college_semester}, {academic_year} "
ws['A17'].alignment = Alignment(horizontal='left')
ws.merge_cells('A17:F17')

#table

thin = Side(border_style="thin", color="000000")# border style, color 
border = Border(left=thin, right=thin, top=thin, bottom=thin)# the position of the border 

rows = ws.iter_cols(min_row=19, min_col=1, max_row=86, max_col=6)

# border
for row in rows:
    for cell in row:
        cell.border = border

#center table contents
rows = ws.iter_cols(min_row=19, min_col=1, max_row=86, max_col=6)
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
rows = ws.iter_cols(min_row=21, min_col=1, max_row=86, max_col=6)
for row in rows:
    for cell in row:
        cell.font = font_size

ws['A88'].value = "Note: Subject for verification/recommendation/approval by the University Evaluation/Review Committee"
ws['A88'].alignment = Alignment(horizontal='left', indent=1)
ws.merge_cells('A88:F88')
ws['A89'].value = "on Honor Graduates"
ws['A89'].alignment = Alignment(horizontal='left', indent=1)
ws.merge_cells('A89:F89')

wb.save('static/Honors.xlsx')