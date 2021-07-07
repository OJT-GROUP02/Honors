import datetime
import openpyxl

from openpyxl import Workbook, load_workbook
from openpyxl.utils import get_column_letter
from openpyxl.styles import Font, Border, Alignment, fills, numbers
from openpyxl.worksheet.dimensions import ColumnDimension
from openpyxl.descriptors.excel import UniversalMeasure, Relation


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


wb = Workbook()

wb.create_sheet("Rank", 0)
wb.create_sheet("URO", 1)

ws = wb["URO"]
ColumnDimension(ws, auto_size=True)
ws.page_setup.paperHeight = '13in'
ws.page_setup.paperWidth = '8.5in'

# Heading
ws.append(['Republic of the Philippines'])
ws.merge_cells('A1:G1')
ws.append(['Bicol University'])
ws.merge_cells('A2:G2')
ws.append(['College Name'])
ws.merge_cells('A3:G3')
ws['A3'].font = Font(bold=True)

for row in ws.iter_rows():
    for cell in row:
        cell.alignment = Alignment(
            wrap_text=True, horizontal='center', vertical='center')

# rows = range(1, 8)
# columns = range(1, 5)
# for row in rows:
#     for col in columns:
#         ws.cell(row, col).alignment = Alignment(horizontal='center', vertical='center', wrapText=True)

# Date
ws['G5'].value = "Date Today"
ws['G5'].alignment = Alignment(horizontal='right')


# Inside Address
ws['A7'].value = "THE BICOL UNIVERSITY REGISTRAR"
ws['A8'].value = "Bicol University"
ws['A9'].value = "Legazpi City"

for row in ws['A7':'G9']:
    for cell in row:
        cell.alignment = Alignment(horizontal='left')
        
#Attention   
for col in range(1, 8):
    ws.column_dimensions[get_column_letter(col)].bestFit=True

ws['A12'].value = "Attn: UNIVERITY EVALUATION/REVIEW COMMITTEE ON HONOR AND GRADUATES"
ws.merge_cells('A12:G12')
ws['A12'].alignment = Alignment(horizontal='center', vertical='center', wrapText=True)

#Greetings
ws['A15'].value = "Sir/Madam:"
ws['A15'].alignment = Alignment(horizontal='left')

#Letter Body
# ws.row_dimensions[16].bestFit=True

for row in range (16, 18):
   ws.row_dimensions[(row)].bestFit=True
   
ws['A16'].value = "Herewith are the Official List of Candidates for Graduation with Honors under the different degree programs"
ws['A16'].alignment = Alignment(horizontal='left', indent=1)
ws.merge_cells('A16:G16')

ws['A17'].value = " of the _________________________ for the _________________ "
ws['A17'].alignment = Alignment(horizontal='left')
ws.merge_cells('A17:G17')




wb.save('static/Honors.xlsx')