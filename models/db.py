db = DAL('postgres://postgres:april17@localhost/honors')

db.define_table('awards',
                Field('award_id'),
                Field('award_title'),
                migrate=False
                )

db.define_table('college',
                Field('college_id'),
                Field('college_name'),
                Field('college_address'),
                migrate=False
                )

db.define_table('committee_position',
                Field('position_id'),
                Field('hierarchy_id'),
                Field('position_name'),
                migrate=False
                )

db.define_table('header',
                Field('header_id'),
                Field('college_id'),
                Field('semester'),
                Field('academic_year'),
                migrate=False
                )

db.define_table('dean',
                Field('dean_id'),
                Field('dean_name'),
                Field('professional_title'),
                migrate=False
                )

db.define_table('student',
                Field('student_id'),
                Field('last_name'),
                Field('first_name'),
                Field('middle_name'),
                Field('gender'),
                Field('classification'),
                migrate=False
                )

db.define_table('grade',
                Field('grade_id'),
                Field('student_id'),
                Field('total_units'),
                Field('sum_of_grades'),
                Field('final_gwa'),
                Field('award_id'),
                migrate=False
                )

db.define_table('committee',
                Field('committee_id'),
                Field('position_id'),
                Field('full_name'),
                Field('professional_title'),
                Field('office_position'),
                migrate=False
                )
