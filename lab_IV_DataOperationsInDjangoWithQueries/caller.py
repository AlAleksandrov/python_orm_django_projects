import os
import django
from datetime import date

from django.template.defaultfilters import lower

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
# Run and print your queries
from main_app.models import Student


def add_students():
    Student.objects.create(
        student_id="FC5204",
        first_name="John",
        last_name='Doe',
        birth_date=date(1995, 5, 15),
        email='john.doe@university.com'
    )

    student_2 = Student(
        student_id='FE0054',
        first_name='Jane',
        last_name='Smith',
        email='jane.smith@university.com'
    )
    student_2.save()

    student_3 = Student()
    student_3.student_id='FH2014'
    student_3.first_name='Alice'
    student_3.last_name='Johnson'
    student_3.birth_date=date(1998, 2, 10)
    student_3.email='alice.johnson@university.com'
    student_3.save()

    Student.objects.create(
        student_id="FH2015",
        first_name="Bob",
        last_name='Wilson',
        birth_date=date(1996, 11, 25),
        email='bob.wilson@university.com'
    )

# add_students()

def get_students_info():
    all = Student.objects.all()

    return '\n'.join(f"Student №{s.student_id}: {s.first_name} {s.last_name}; Email: {s.email}" for s in all)

# print(get_students_info())

def update_students_emails():
    all = Student.objects.all()
    for student in all:
        student.email = f"{lower(student.first_name)}.{lower(student.last_name)}@uni-students.com"
        # student.save()
    Student.objects.bulk_update(all, ['email'])

# update_students_emails()
# for student in Student.objects.all():
#     print(student.email)

def truncate_students():
    all = Student.objects.all()
    for student in all:
        student.delete()

truncate_students()
print(Student.objects.all())
print(f"Number of students: {Student.objects.count()}")
