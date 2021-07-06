import datetime


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
