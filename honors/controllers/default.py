def index():
    return dict(message="Hello")


def uro():
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
