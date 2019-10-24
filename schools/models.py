from django.db import models
from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.urls import reverse
from django.conf import settings
from django.utils.text import slugify
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from taggit.managers import TaggableManager

START = (('January', 'January'),
         ('February', 'February'),
         ('March', 'March'),
         ('April', 'April'),
         ('May', 'May'),
         ('June', 'June'),
         ('July', 'July'),
         ('August', 'August'),
         ('September', 'September'),
         ('September', 'September'),
         ('September', 'September'),
         ('October', 'October'),
         ('November', 'November'),
         ('December', 'December'))

BLOOD = (('A+', 'A+'),
         ('A-', 'A-'),
         ('B+', 'B+'),
         ('B-', 'B-'),
         ('O+', 'O+'),
         ('O-', 'O-'),
         ('AB+', 'AB+'),
         ('AB-', 'AB-'))

GENDER = (
    ('Male', 'Male'),
    ('Female', 'Female'))

RELIGIONS = (('Christian', 'Christian'),
             ('Muslim', 'Muslim'),
             ('Others', 'Others'))

FIRST = "First"
SECOND = "Second"
THIRD = "Third"

OPTIONS = (('Yes', 'Yes'),
           ('No', 'No'))

TYPES = (('Incoming', 'Incoming'),
         ('Outgoing', 'Outgoing'))

TERM = (
    (FIRST, "First"),
    (SECOND, "Second"),
    (THIRD, "Third"),
)

PROTOCOL = (('Mail', 'Mail'),
            ('Sendmail', 'Sendmail'),
            ('smtp', 'smtp'))

PRIORITY = (('Highest', 'Highest'),
            ('Normal', 'Normal'),
            ('Lowest', 'Lowest'))

EMAIL = (('Text', 'Text'),
         ('Html', 'Html'))

SET = (('utf-8', 'utf-8'),
         ('iso-8859-1', 'iso-8859-1'))

PRO = (
    ('Admin', 'Admin'),
    ('Guardian', 'Guardian'),
    ('Student', 'Student'),
    ('Teacher', 'Teacher'),
    ('Accountant', 'Accountant'),
    ('Librarian', 'Librarian'),
    ('Receptionist', 'Receptionist'),
    ('Staff', 'Staff'),
    ('Servant', 'Servant'),
    ('General Accountant', 'General Accountant'))

EMPTY = 0
STUDENT = 1
TEACHER = 2
GUARDIAN = 3
RECEPTIONIST = 4
LIBRARIAN = 5
ADMIN = 6
ACCOUNTANT = 7
STAFF = 8
SUPERUSER = 9
SERVANT = 10

MONDAY = 1
TUESDAY = 2
WEDNESDAY = 3
THURSDAY = 4
FRIDAY = 5
SATURDAY = 6
SUNDAY = 7
DAYS_OF_THE_WEEK = (
    (MONDAY, 'Monday'),
    (TUESDAY, 'Tuesday'),
    (WEDNESDAY, 'Wednesday'),
    (THURSDAY, 'Thursday'),
    (FRIDAY, 'Friday'),
    (SATURDAY, 'Saturday'),
    (SUNDAY, 'Sunday'),
)


class Settings(models.Model):
    brand_name = models.CharField(max_length=130)
    brand_title = models.CharField(max_length=130)
    language = models.CharField(max_length=130)
    enable_RTL = models.CharField(max_length=130)
    enable_Frontend = models.CharField(max_length=130)
    general_Theme = models.CharField(max_length=130)
    default_time_zone = models.CharField(max_length=130)
    default_date = models.CharField(max_length=130)
    brand_logo = models.FileField(upload_to='logo/', blank=False)
    favicon_icon = models.FileField(upload_to='icon/', blank=False)
    brand_footer = models.CharField(max_length=130)
    google_Analytics = models.CharField(max_length=130)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.slug


def create_slug(instance, new_slug=None):
    slug = slugify(instance.brand_title)
    if new_slug is not None:
        slug = new_slug
    qs = Settings.objects.filter(slug=slug)
    exists = qs.exists()

    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_settings_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_settings_receiver, sender=Settings)


class School(models.Model):
    school_code = models.CharField(max_length=130)
    school_name = models.CharField(max_length=130)
    address = models.CharField(max_length=130)
    phone = models.CharField(max_length=130)
    registration_date = models.DateField(null=True)
    email_address = models.EmailField(max_length=120)
    fax = models.CharField(max_length=130)
    footer = models.CharField(max_length=130)

    currency = models.CharField(max_length=130)
    currency_symbol = models.CharField(max_length=130)

    enable_frontend = models.CharField(max_length=130, blank=False, choices=OPTIONS)
    RESULTS = (('Average of all exams', 'Average of all exams'),
               ('Only based on final exams', 'Only based on final exams'))
    exam_final_result = models.CharField(max_length=130, blank=False, choices=RESULTS)
    latitude = models.CharField(max_length=130)
    longitude = models.CharField(max_length=130)
    api_key = models.CharField(max_length=130)
    online_Admission = models.CharField(max_length=130, blank=False, choices=OPTIONS)

    facebook_url = models.URLField(max_length=130)
    twitter_url = models.URLField(max_length=130)
    linkedIn_url = models.URLField(max_length=130)
    google_plus_url = models.URLField(max_length=130)
    youtube_url = models.URLField(max_length=130)
    instagram_url = models.URLField(max_length=130)
    pinterest_url = models.URLField(max_length=130)

    frontend_Logo = models.FileField(upload_to='logo/', blank=False)
    backend_Logo = models.FileField(upload_to='logo/', blank=False)
    STATUS = (('Active', 'Active'),
              ('Inactive', 'Inactive'))
    status = models.CharField(max_length=130, blank=True, null=True, default="Active", choices=STATUS)
    THEMES = (('Black', 'Black'),
              ('Navy Blue', 'Navy Blue'),
              ('Red', 'Red'),
              ('Maroon', 'Maroon'),
              )
    theme = models.CharField(max_length=130, blank=False, choices=THEMES)

    def __str__(self):
        return self.school_name

    class Meta:
        ordering = ('school_name',)
        verbose_name = 'school'
        verbose_name_plural = 'schools'


class UserManager(BaseUserManager):
    def Create_user(self, username, password=None):
        if not username:
            raise ValueError("Users must have a user name")

        user = self.model(
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.Create_user(
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    full_name = models.CharField(max_length=255, blank=False, null=True)
    email = models.EmailField(max_length=255, unique=True, blank=True, null=True)
    username = models.CharField(max_length=30, unique=True)
    national_ID = models.CharField(max_length=100, blank=False, null=True)
    phone = models.CharField(max_length=100)

    gender = models.CharField(max_length=100, blank=True, choices=GENDER)
    religion = models.CharField(max_length=100, blank=True, choices=RELIGIONS)

    present_address = models.CharField(max_length=100)
    permanent_address = models.CharField(max_length=100)
    blood_group = models.CharField(max_length=100, blank=True, choices=BLOOD)
    birth_date = models.DateField(null=True, blank=True)
    other_info = models.TextField(max_length=200)
    photo = models.ImageField(upload_to='avatars/', blank=False)
    is_active = models.BooleanField(default=True)  # can login
    is_staff = models.BooleanField(default=False)  # staff user non superuser
    joining_date = models.DateTimeField(verbose_name="date joined", null=True, auto_now=False)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)

    is_superuser = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    is_guardian = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

    roles = models.ForeignKey('Role', on_delete=models.CASCADE, blank=False, null=True)

    USERNAME_FIELD = 'username'  # username
    # USERNAME_FIELD and password are required by default
    REQUIRED_FIELDS = []  # ['full_name'] #python manage.py createsuperuser

    objects = UserManager()

    def __str__(self):
        if self.full_name:
            return self.full_name
        return self.username

    def get_picture(self):
        no_picture = settings.STATIC_URL + 'img/img_avatar.png'
        try:
            return self.photo.url
        except:
            return no_picture

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


class Role(models.Model):
    school = models.ForeignKey('School', on_delete=models.CASCADE, blank=False, null=True)
    role_name = models.CharField(max_length=130)
    note = models.CharField(max_length=130)
    is_default = models.CharField(max_length=100, blank=True, choices=OPTIONS)

    def __str__(self):
        return self.role_name


class EmailSetting(models.Model):
    school = models.ForeignKey('School', on_delete=models.CASCADE, blank=False, null=True)
    email_protocol = models.CharField(max_length=100, blank=True, choices=PROTOCOL)
    email_type = models.CharField(max_length=100, blank=True, choices=EMAIL)
    char_set = models.CharField(max_length=100, blank=True, choices=SET)
    priority = models.CharField(max_length=100, blank=True, choices=PRIORITY)
    email_from_name = models.CharField(max_length=300)
    email_from_address = models.CharField(max_length=300)

    def __str__(self):
        return self.email_protocol


class Designation(models.Model):
    school = models.ForeignKey('School', on_delete=models.CASCADE, blank=False, null=True)
    designation = models.CharField(max_length=130)
    note = models.TextField(max_length=300)

    def __str__(self):
        return self.designation


class Feedback(models.Model):
    school = models.ForeignKey('School', on_delete=models.CASCADE, blank=False, null=True)
    feedback = models.TextField(max_length=300)
    is_publish = models.CharField(max_length=130, blank=False, choices=OPTIONS)
    date = models.DateField(null=True)

    def __str__(self):
        return self.feedback


class Superuser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='superuser')
    roles = models.ForeignKey(Role, on_delete=models.CASCADE, blank=False, null=True)
    resume = models.FileField(upload_to='resume/', blank=False)

    def __str__(self):
        return self.user.username


class Teacher(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, blank=False, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher')
    responsibility = models.CharField(max_length=200)
    roles = models.ForeignKey(Role, on_delete=models.CASCADE, blank=False, null=True)
    resume = models.FileField(upload_to='resume/', blank=False)
    salary_grade = models.ForeignKey('SalaryGrade', on_delete=models.CASCADE, blank=False, null=True)
    TYPE = (('Monthly', 'Monthly'),
            ('Hourly', 'Hourly'))
    salary_type = models.CharField(max_length=100, blank=False, choices=TYPE)
    facebook_url = models.URLField(max_length=130)
    twitter_url = models.URLField(max_length=130)
    linkedIn_url = models.URLField(max_length=130)
    google_plus_url = models.URLField(max_length=130)
    youtube_url = models.URLField(max_length=130)
    instagram_url = models.URLField(max_length=130)
    pinterest_url = models.URLField(max_length=130)
    IS = (('Yes', 'Yes'),
          ('No', 'No'))
    Is_View_on_Web = models.CharField(max_length=100, blank=False, choices=IS)

    def __str__(self):
        return self.user.username


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee')
    school = models.ForeignKey(School, on_delete=models.CASCADE, blank=False, null=True)
    designation = models.ForeignKey('Designation', on_delete=models.CASCADE, blank=False, null=True)
    salary_grade = models.ForeignKey('SalaryGrade', on_delete=models.CASCADE, blank=False, null=True)
    TYPE = (('Monthly', 'Monthly'),
            ('Hourly', 'Hourly'))
    salary_type = models.CharField(max_length=100, blank=False, choices=TYPE)
    roles =models.ForeignKey(Role, on_delete=models.CASCADE, blank=False, null=True)
    resume = models.FileField(upload_to='resume/', blank=False)
    facebook_url = models.URLField(max_length=130)
    twitter_url = models.URLField(max_length=130)
    linkedIn_url = models.URLField(max_length=130)
    google_plus_url = models.URLField(max_length=130)
    youtube_url = models.URLField(max_length=130)
    instagram_url = models.URLField(max_length=130)
    pinterest_url = models.URLField(max_length=130)
    IS = (('Yes', 'Yes'),
          ('No', 'No'))
    Is_View_on_Web = models.CharField(max_length=100, blank=False, choices=IS)
    is_present = models.BooleanField(default=False)
    is_absent = models.BooleanField(default=False)
    is_late = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Guardian(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, blank=False, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='guardians')
    roles = models.ForeignKey(Role, on_delete=models.CASCADE, blank=False, null=True)
    profession = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username


class Student(models.Model):
    school = models.ForeignKey(School, on_delete=models.SET_NULL, blank=False, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student')
    admission_no = models.CharField(max_length=100)
    admission_date = models.DateField(null=True)
    guardian = models.ForeignKey('Guardian', on_delete=models.CASCADE, blank=False, null=True, related_name='guardians')
    RELATION = (('Father', 'Father'),
                ('Mother', 'Mother'),
                ('Sister', 'Sister'),
                ('Bother', 'Bother'),
                ('Uncle', 'Uncle'),
                ('Maternal Uncle', 'Maternal Uncle'),
                ('Aunt', 'Aunt'),
                ('Other Relative', 'Other Relative'))
    relation_With_Guardian = models.CharField(max_length=100, blank=False, choices=RELATION)
    classroom = models.ForeignKey('Classroom', on_delete=models.SET_NULL, blank=False, null=True)
    section = models.ForeignKey('Section', on_delete=models.SET_NULL, blank=False, null=True)
    student_type = models.ForeignKey('StudentType', on_delete=models.SET_NULL, blank=False, null=True)
    GROUP = (
        ('Science', 'Science'),
        ('Arts', 'Arts'),
        ('Commerce', 'Commerce'))
    group = models.CharField(max_length=100, blank=False, choices=GROUP)
    roll_no = models.CharField(max_length=100)
    registration_no = models.CharField(max_length=100)
    roles = models.ForeignKey(Role, on_delete=models.CASCADE, blank=False, null=True)
    discount = models.CharField(max_length=100)
    second_language = models.CharField(max_length=100)
    caste = models.CharField(max_length=100)

    previous_school = models.CharField(max_length=100)
    previous_class = models.CharField(max_length=100)
    transfer_certificate = models.FileField(upload_to='certificates/', null=True, blank=False)

    father_name = models.CharField(max_length=100)
    father_phone = models.CharField(max_length=100)
    father_education = models.CharField(max_length=100)
    father_profession = models.CharField(max_length=100)
    father_designation = models.CharField(max_length=100)
    father_photo = models.FileField(upload_to='avatar/', null=True, blank=False)

    mother_name = models.CharField(max_length=100)
    mother_phone = models.CharField(max_length=100)
    mother_education = models.CharField(max_length=100)
    mother_profession = models.CharField(max_length=100)
    mother_designation = models.CharField(max_length=100)
    mother_photo = models.FileField(upload_to='avatar/', null=True, blank=False)
    health_condition = models.CharField(max_length=100)
    is_present = models.BooleanField(default=False)
    is_absent = models.BooleanField(default=False)
    is_late = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user(sender, instance, created, **kwargs):
    if instance.is_superuser:
        Superuser.objects.get_or_create(user=instance)

    elif instance.is_teacher:
        Teacher.objects.get_or_create(user=instance)

    elif instance.is_student:
        Student.objects.get_or_create(user=instance)

    elif instance.is_guardian:
        Guardian.objects.get_or_create(user=instance)

    else:
        Employee.objects.get_or_create(user=instance)


@receiver(post_save, sender=User)
def save_user(sender, instance, **kwargs):
    if instance.is_superuser:
        instance.superuser.save()

    elif instance.is_teacher:
        instance.teacher.save()

    elif instance.is_student:
        instance.student.save()

    elif instance.is_employee:
        instance.employee.save()

    elif instance.is_guardian:
        instance.guardians.save()

    else:
        None


class StudentType(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, blank=False, null=True)
    student_type = models.CharField(max_length=100, blank=True)
    note = models.TextField(max_length=130)

    def __str__(self):
        return self.student_type

class Activity(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    classroom = models.ForeignKey('Classroom', on_delete=models.CASCADE)
    section = models.ForeignKey('Section', on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=True)
    activity_date = models.DateField(blank=True, null=True)
    activity = models.TextField(max_length=130)

    def __str__(self):
        return self.activity

class Card(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    border_color = models.CharField(max_length=130)
    top_background = models.CharField(max_length=130)
    card_school_name = models.CharField(max_length=130)
    school_name_font_size = models.CharField(max_length=130)
    school_name_color = models.CharField(max_length=130)
    school_address = models.CharField(max_length=130)
    school_address_color = models.CharField(max_length=130)
    admit_card_font_size = models.CharField(max_length=130)
    admit_card_color = models.CharField(max_length=130)
    admit_card_background = models.CharField(max_length=130)
    title_font_size = models.CharField(max_length=130)
    title_color = models.CharField(max_length=130)
    value_font_size = models.CharField(max_length=130)
    value_color = models.CharField(max_length=130)
    exam_font_size = models.CharField(max_length=130)
    exam_color = models.CharField(max_length=130)
    subject_font_size = models.CharField(max_length=130)
    subject_color = models.CharField(max_length=130)
    bottom_signature = models.CharField(max_length=130)
    signature_background = models.CharField(max_length=130)
    signature_color = models.CharField(max_length=130)
    signature_align = models.CharField(max_length=130)
    admit_card_logo = models.FileField(upload_to='card/', null=True, blank=False)

    def __str__(self):
        return self.card_school_name

class Classroom(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    classroom = models.CharField(max_length=130)
    numeric_name = models.CharField(max_length=130)
    class_teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, blank=False, null=True)
    note = models.CharField(max_length=130)

    def __str__(self):
        return self.classroom

    class Meta:
        ordering = ('classroom',)
        verbose_name = 'classroom',
        verbose_name_plural = 'classrooms'


class Section(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    section = models.CharField(max_length=130)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    section_teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, blank=False, null=True)
    note = models.CharField(max_length=130)

    def __str__(self):
        return self.section

    class Meta:
        ordering = ('section',)
        verbose_name = 'section'
        verbose_name_plural = 'sections'


class Year(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, blank=False, null=True)
    start_month = models.DateField(blank=True, null=True)
    end_month = models.DateField(blank=True, null=True)
    is_running = models.BooleanField(default=False, blank=True, null=True)
    note = models.TextField(max_length=300)

    def get_academic_year(self):
        academic_year = ''
        if self.start_month and self.end_month:
            academic_year = str(self.start_month) + " / " + str(self.end_month)
        return academic_year


class Term(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, blank=False, null=True)
    term = models.CharField(max_length=10, choices=TERM, blank=True)
    is_current_term = models.BooleanField(default=False, blank=True, null=True)
    year = models.ForeignKey(Year, on_delete=models.CASCADE, blank=True, null=True)
    next_term_begins = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.term


class Subject(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, blank=False, null=True)
    subject_name = models.CharField(max_length=130)
    subject_code = models.CharField(max_length=130)
    author = models.CharField(max_length=130)
    TYPE = (('Mandatory', 'Mandatory'),
            ('Optional', 'Optional'))
    type = models.CharField(max_length=100, blank=False, choices=TYPE)

    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, blank=False, null=True)
    subject_teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, blank=False, null=True)
    note = models.TextField(max_length=250)

    def __str__(self):
        return self.subject_code + " (" + self.subject_name + ")"

    def get_absolute_url(self):
        return reverse('subject_list', kwargs={'school_id': self.pk})


class Syllabus(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, blank=False, null=True)
    syllabus_title = models.CharField(max_length=130)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, blank=False, null=True)
    subject_name = models.ForeignKey(Subject, on_delete=models.CASCADE, blank=False, null=True)
    year = models.ForeignKey(Year, on_delete=models.CASCADE, blank=False, null=True)
    syllabus = models.FileField(upload_to='syllabus/', null=True, blank=False)
    note = models.TextField(max_length=250)

    def __str__(self):
        return self.syllabus_title


class Material(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, blank=False, null=True)
    material_title = models.CharField(max_length=130)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, blank=False, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, blank=False, null=True)
    material = models.FileField(upload_to='material/', null=True, blank=False)
    description = models.TextField(max_length=250)

    def __str__(self):
        return self.material_title


class Routine(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, blank=False, null=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, blank=False, null=True)
    section = models.CharField(max_length=130)
    subject_name = models.CharField(max_length=130)
    day = models.IntegerField(choices=DAYS_OF_THE_WEEK, null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, blank=False, null=True)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    room_no = models.CharField(max_length=130)

    def __str__(self):
        return self.start_time


class BulkStudent(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, blank=False, null=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, blank=False, null=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, blank=False, null=True)


class StudentAttendance(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, blank=False, null=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, blank=False, null=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, blank=False, null=True)
    date = models.DateField(null=True)

class SalaryPayment(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, blank=False, null=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, blank=False, null=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, blank=False, null=True)


class TeacherAttendance(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, blank=False, null=True)
    date = models.DateField(null=True)


class EmployeeAttendance(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, blank=False, null=True)
    date = models.DateField(null=True)


class AbsentEmail(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, blank=False, null=True)
    receiver_type = models.CharField(max_length=100, blank=False, choices=PRO)
    absent_user = models.CharField(max_length=100, blank=False, choices=PRO)
    template = models.CharField(max_length=100)
    absent_date = models.DateField(null=True)
    subject = models.CharField(max_length=100)
    email_body = models.TextField(max_length=300)


class AbsentSMS(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, blank=False, null=True)
    receiver_type = models.CharField(max_length=100, blank=False, choices=PRO)
    absent_user = models.CharField(max_length=100, blank=False, choices=PRO)
    template = models.CharField(max_length=100)
    absent_date = models.DateField(null=True)
    SMS = models.TextField(max_length=300)
    gateway = models.CharField(max_length=100)


class Assignment(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, blank=False, null=True)
    assignment_title = models.CharField(max_length=100)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, blank=False, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, blank=False, null=True)
    deadline = models.DateField(null=True)
    assignment = models.FileField(upload_to='assignment/', null=True, blank=False)
    note = models.TextField(max_length=300)


class ExamGrade(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, blank=False, null=True)
    exam_grade = models.CharField(max_length=100)
    grade_point = models.CharField(max_length=100)
    mark_from = models.CharField(max_length=100)
    mark_to = models.CharField(max_length=100)
    note = models.TextField(max_length=300)

    def __str__(self):
        return self.exam_grade


class Exam(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, blank=False, null=True)
    exam_title = models.CharField(max_length=100)
    start_date = models.DateField(null=True)
    note = models.TextField(max_length=300)

    def __str__(self):
        return self.exam_title
class Mark(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, blank=False, null=True)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, blank=False, null=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, blank=False, null=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, blank=False, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, blank=False, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, blank=False, null=True)

    def __str__(self):
        return self.subject

class ExamSchedule(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, blank=False, null=True)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, blank=False, null=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, blank=False, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, blank=False, null=True)
    exam_date = models.DateField(null=True)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    room_no = models.CharField(max_length=300)
    note = models.TextField(max_length=300)


class ExamSuggestion(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, blank=False, null=True)
    suggestion_title = models.CharField(max_length=300)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, blank=False, null=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, blank=False, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, blank=False, null=True)
    suggestion = models.FileField(upload_to='suggestion/', null=True, blank=False)
    note = models.TextField(max_length=300)

    def __str__(self):
        return self.suggestion_title


class ExamAttendance(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, blank=False, null=True)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, blank=False, null=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, blank=False, null=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, blank=False, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, blank=False, null=True)


class Promotion(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, blank=False, null=True)
    running_session = models.CharField(max_length=100)
    promote_to_session = models.CharField(max_length=100)
    current_class = models.ForeignKey(Classroom, on_delete=models.CASCADE, blank=False, null=True)
    promote_to_class = models.CharField(max_length=100)


class CertificateType(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, blank=False, null=True)
    certificate_name = models.CharField(max_length=100)
    school_name = models.CharField(max_length=100)
    certificate_text = models.TextField(max_length=400)
    footer_left_text = models.CharField(max_length=100)
    footer_middle_text = models.CharField(max_length=100)
    footer_right_text = models.CharField(max_length=100)
    background = models.FileField(upload_to='background/', null=True, blank=False)

    def __str__(self):
        return self.certificate_name


class GenerateCertificate(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, blank=False, null=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, blank=False, null=True)
    certificate_type = models.ForeignKey(CertificateType, on_delete=models.CASCADE, blank=False, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, blank=False, null=True)


class Book(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, blank=False, null=True)
    book_title = models.CharField(max_length=100)
    book_ID = models.CharField(max_length=100)
    ISBN_no = models.CharField(max_length=100)
    edition = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    language = models.CharField(max_length=100)
    price = models.CharField(max_length=100)
    quantity = models.CharField(max_length=100)
    almira_no = models.CharField(max_length=100)
    book_cover = models.FileField(upload_to='cover', blank=False)

    def __str__(self):
        return self.book_title


class EBook(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, blank=False, null=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, blank=False, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, blank=False, null=True)
    EBook_title = models.CharField(max_length=100)
    edition = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    language = models.CharField(max_length=100)
    cover_image = models.ImageField(upload_to='cover', blank=False)
    e_book = models.FileField(upload_to='ebook', blank=False)

    def __str__(self):
        return self.EBook_title


class LibraryMember(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, blank=False, null=True)
    photo = models.ImageField(upload_to='avatar/', null=True, blank=False)
    library_ID = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    classroom = models.CharField(max_length=100)
    section = models.CharField(max_length=100)
    roll_no = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Issue(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, blank=False, null=True)
    select_book = models.ForeignKey(Book, on_delete=models.CASCADE, blank=False, null=True)
    library_member = models.ForeignKey(LibraryMember, on_delete=models.CASCADE, blank=False, null=True)
    ISBN_no = models.CharField(max_length=100)
    edition = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    language = models.CharField(max_length=100)
    price = models.CharField(max_length=100)
    quantity = models.CharField(max_length=100)
    almira_no = models.CharField(max_length=100)
    book_cover = models.ImageField(upload_to='cover/', null=True, blank=False)
    issue_date = models.DateField(null=True)
    due_date = models.DateField(null=True)
    return_date = models.DateField(null=True)

    def __str__(self):
        return self.select_book


class Vehicle(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, blank=False, null=True)
    vehicle_number = models.CharField(max_length=100)
    vehicle_model = models.CharField(max_length=100)
    driver = models.CharField(max_length=100)
    vehicle_licence = models.CharField(max_length=100)
    vehicle_contact = models.CharField(max_length=100)
    note = models.CharField(max_length=100)

    def __str__(self):
        return self.vehicle_number

class Type(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, blank=False, null=True)
    complain_type = models.CharField(max_length=100)

    def __str__(self):
        return self.complain_type


class Complain(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, blank=False, null=True)
    complain_user_type = models.ForeignKey(Role, on_delete=models.CASCADE, blank=False, null=True)
    complain_user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=True)
    complain_type = models.ForeignKey(Type, on_delete=models.CASCADE, blank=False, null=True)
    complain_date = models.DateField(null=True)
    action_date = models.DateField(null=True)
    complain = models.TextField(max_length=400)

    def __str__(self):
        return self.complain_user

class Route(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, blank=False, null=True)
    route_title = models.CharField(max_length=100)
    route_start = models.CharField(max_length=100)
    route_end = models.CharField(max_length=100)
    vehicle_for_route = models.ForeignKey(Vehicle, on_delete=models.CASCADE, blank=False, null=True)
    stop_name = models.CharField(max_length=100)
    stop_km = models.CharField(max_length=100)
    stop_fare = models.CharField(max_length=100)
    note = models.CharField(max_length=100)

    def __str__(self):
        return self.route_title


class TransportMember(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, blank=False, null=True)
    photo = models.ImageField(upload_to='avatar/', null=True, blank=False)
    name = models.ForeignKey(Student, on_delete=models.CASCADE, blank=False, null=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, blank=False, null=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, blank=False, null=True)
    roll_no = models.CharField(max_length=100)
    transport_route_name = models.ForeignKey(Route, on_delete=models.CASCADE, blank=False, null=True)
    stop_Name = models.CharField(max_length=100)
    stop_KM = models.CharField(max_length=100)
    stop_Fare = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Hostel(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, blank=False, null=True)
    hostel_name = models.CharField(max_length=100)
    TYPE = (
        ('Single - Boys', 'Single - Boys'),
        ('Single - Girls', 'Single - Girls'),
        ('Mixed', 'Mixed'))
    hostel_type = models.CharField(max_length=100, blank=False, choices=TYPE)
    address = models.CharField(max_length=100)
    note = models.TextField(max_length=300)

    def __str__(self):
        return self.hostel_name


class Room(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, blank=False, null=True)
    room_no = models.CharField(max_length=100)
    TYPE = (
        ('AC', 'AC'),
        ('Non AC', 'Non AC'))
    room_type = models.CharField(max_length=100, blank=False, choices=TYPE)
    seat_total = models.CharField(max_length=100)
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, blank=False, null=True)
    cost_per_seat = models.CharField(max_length=100)
    note = models.TextField(max_length=300)


class HostelMember(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, blank=False, null=True)
    photo = models.FileField(upload_to='avatar/', null=True, blank=False)
    name = models.ForeignKey(Student, on_delete=models.CASCADE, blank=False, null=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, blank=False, null=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, blank=False, null=True)
    roll_no = models.CharField(max_length=100)
    hostel_name = models.ForeignKey(Hostel, on_delete=models.CASCADE, blank=False, null=True)
    room_no = models.CharField(max_length=100)
    TYPE = (
        ('AC', 'AC'),
        ('Non AC', 'Non AC'))
    room_type = models.CharField(max_length=100, blank=False, choices=TYPE)


class Email(models.Model):
    school_name = models.ForeignKey(School, on_delete=models.CASCADE, blank=False, null=True)
    receiver_type = models.CharField(max_length=100, blank=False, choices=PRO)
    receiver = models.CharField(max_length=100, blank=False, choices=PRO)
    subject = models.CharField(max_length=100)
    email_body = models.TextField(max_length=300)
    attachment = models.FileField(upload_to='attachment/', null=True, blank=False)


class SMS(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, blank=False, null=True)
    receiver_type = models.CharField(max_length=100, blank=False, choices=PRO)
    receiver = models.CharField(max_length=100, blank=False, choices=PRO)
    SMS = models.TextField(max_length=300)
    gateway = models.CharField(max_length=100)


class Notice(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, blank=False, null=True)
    notice_title = models.CharField(max_length=100)
    date = models.DateField(null=True)
    notice_for = models.CharField(max_length=100, blank=False, choices=PRO)
    notice = models.TextField(max_length=300)
    IS = (('Yes', 'Yes'),
          ('No', 'No'))
    Is_View_on_Web = models.CharField(max_length=100, blank=False, choices=IS)


class News(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, blank=False, null=True)
    news_title = models.CharField(max_length=100)
    date = models.DateField(null=True)
    image = models.FileField(upload_to='images/', null=True, blank=False)
    news = models.TextField(max_length=300)
    IS = (('Yes', 'Yes'),
          ('No', 'No'))
    Is_View_on_Web = models.CharField(max_length=100, blank=False, choices=IS)


class Holiday(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, blank=False, null=True)
    holiday_title = models.CharField(max_length=100)
    from_date = models.DateField(null=True)
    to_date = models.DateField(null=True)
    note = models.TextField(max_length=300)
    IS = (('Yes', 'Yes'),
          ('No', 'No'))
    Is_View_on_Web = models.CharField(max_length=100, blank=False, choices=IS)


class Event(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, blank=False, null=True)
    event_title = models.CharField(max_length=100)
    event_for = models.CharField(max_length=100, blank=False, choices=PRO)
    event_place = models.CharField(max_length=100)
    from_date = models.DateField(null=True)
    to_date = models.DateField(null=True)
    image = models.FileField(upload_to='images/', null=True, blank=False)
    note = models.TextField(max_length=300)
    IS = (('Yes', 'Yes'),
          ('No', 'No'))
    Is_View_on_Web = models.CharField(max_length=100, blank=False, choices=IS)

class ExpenditureHead(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, blank=False, null=True)
    expenditure_head = models.CharField(max_length=100)
    note = models.TextField(max_length=300)
    def __str__(self):
        return self.expenditure_head

class SalaryGrade(models.Model):
    payee = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE, blank=False, null=True)
    grade_name = models.CharField(max_length=100)
    basic_salary = models.CharField(max_length=100)
    house_rent = models.CharField(max_length=100)
    transport_allowance = models.CharField(max_length=100)
    medical_allowance = models.CharField(max_length=100)
    over_time_hourly_pay = models.CharField(max_length=100)
    provident_fund = models.CharField(max_length=100)
    hourly_rate = models.CharField(max_length=100)
    total_allowance = models.CharField(max_length=100, blank=True, null=True)
    total_deduction = models.CharField(max_length=100, blank=True, null=True)
    gross_salary = models.CharField(max_length=100, blank=True, null=True)
    net_salary = models.CharField(max_length=100, blank=True, null=True)
    note = models.TextField(null=True, blank=False)
    over_time_total_hour = models.CharField(max_length=100, blank=True, null=True)
    over_time_amount = models.CharField(max_length=100, blank=True, null=True)
    Bonus = models.CharField(max_length=100, blank=True, null=True)
    Penalty = models.CharField(max_length=100, blank=True, null=True)
    Month = models.CharField(max_length=100, blank=True, null=True)
    pay = (('Cheque','Cheque'),
           ('MobileMoney','MobileMoney'),
          ('Cash','Cash'))
    Payment_Method = models.CharField(max_length=100,choices=pay, blank=True, null=True)
    Bank_Name = models.CharField(max_length=100, blank=True, null=True)
    Cheque_Number = models.CharField(max_length=100, blank=True, null=True)
    Expenditure_Head = models.ForeignKey(ExpenditureHead, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.grade_name


class Discount(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, blank=False, null=True)
    title = models.CharField(max_length=100)
    amount = models.CharField(max_length=100)
    note = models.TextField(max_length=300)


class FeeType(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, blank=False, null=True)
    IS = (('GeneralFee', 'GeneralFee'),
          ('Hostel', 'Hostel'),
          ('Transport', 'Transport'))
    fee_type = models.CharField(max_length=100, blank=False, choices=IS)
    fee_title = models.CharField(max_length=100)
    note = models.TextField(max_length=300)
    Class =models.ForeignKey(Classroom, on_delete=models.CASCADE, blank=True, null=True)
    Class_Amount=models.CharField(max_length=100, default='Shs 0.0', blank=True, null=True)

    def __str__(self):
        return self.fee_title

class Invoice(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, blank=False, null=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, blank=False, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, blank=False, null=True)
    fee_type = models.ForeignKey(FeeType, on_delete=models.CASCADE, blank=False, null=True, related_name='fee')
    fee_amount = models.ForeignKey(FeeType, on_delete=models.CASCADE, blank=False, null=True, related_name='fee_am')
    month = models.DateField(max_length=100)
    IS = (('Yes', 'Yes'),
          ('No', 'No'))
    is_discount_applicable = models.CharField(max_length=100, blank=False, choices=IS)
    STATUS = (('Paid', 'Paid'),
              ('Unpaid', 'Unpaid'))
    method =(('Cash', 'Cash'),
              ('Cheque','Cheque'))
    paid_status = models.CharField(max_length=100, blank=False, choices=STATUS)
    Payment_Method = models.CharField(max_length=100, choices=method, blank=True, null=True)
    Bank_Name = models.CharField(max_length=100, default='Shs 0.0', blank=True, null=True)
    Cheque_Number = models.CharField(max_length=100, default='Shs 0.0', blank=True, null=True)
    note = models.TextField(max_length=300)

class BulkInvoice(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, blank=False, null=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, blank=False, null=True)
    fee_type = models.CharField(max_length=100)
    student_name = models.CharField(max_length=100)
    IS = (('Yes', 'Yes'),
          ('No', 'No'))
    is_discount_applicable = models.CharField(max_length=100, blank=False, choices=IS)
    month = models.DateField(max_length=100)
    STATUS = (('Paid', 'Paid'),
              ('Pending', 'Pending'))
    paid_status = models.CharField(max_length=100, blank=False, choices=STATUS)
    note = models.TextField(max_length=300)


class DueFeeEmail(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, blank=False, null=True)
    PRO = (('Guardian', 'Guardian'),
           ('Student', 'Student'))
    receiver_role = models.CharField(max_length=100, blank=False, choices=PRO)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, blank=False, null=True)

    due_fee_student = models.CharField(max_length=100)
    template = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    email_body = models.TextField(max_length=300)
    attachment = models.FileField(upload_to='attachment/', null=True, blank=False)


class DueFeeSMS(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, blank=False, null=True)
    PRO = (('Guardian', 'Guardian'),
           ('Student', 'Student'))
    receiver_type = models.CharField(max_length=100, blank=False, choices=PRO)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, blank=False, null=True)
    due_fee_student = models.CharField(max_length=100)
    template = models.CharField(max_length=100)
    SMS = models.TextField(max_length=300)
    gateway = models.CharField(max_length=100)


class IncomeHead(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, blank=False, null=True)
    income_head = models.CharField(max_length=100)
    note = models.TextField(max_length=300)
    def __str__(self):
        return self.income_head

class Income(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, blank=False, null=True)
    income_head = models.ForeignKey(IncomeHead, on_delete=models.CASCADE, blank=False, null=True)
    method =(('Cash', 'Cash'),
              ('Cheque','Cheque'))
    payment_method = models.CharField(max_length=100, blank=False, choices=method)
    Bank_Name = models.CharField(max_length=100, default='bank name', blank=True, null=True)
    Cheque_Number = models.CharField(max_length=100, default='cheque number', blank=True, null=True)
    amount = models.CharField(max_length=100)
    date = models.DateField(null=True)
    note = models.TextField(max_length=300)


class Expenditure(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, blank=False, null=True)
    expenditure_head = models.ForeignKey(ExpenditureHead, on_delete=models.CASCADE, blank=False, null=True)
    expenditure_method = models.CharField(max_length=100)
    amount = models.CharField(max_length=100)
    date = models.DateField(null=True)
    note = models.TextField(max_length=300)


class Gallery(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, blank=False, null=True)
    gallery_title = models.CharField(max_length=100)
    note = models.TextField(max_length=300)
    IS = (('Yes', 'Yes'),
          ('No', 'No'))
    Is_View_on_Web = models.CharField(max_length=100, blank=False, choices=IS)

    def __str__(self):
        return self.gallery_title


class Image(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, blank=False, null=True)
    gallery_title = models.ForeignKey(Gallery, on_delete=models.CASCADE, blank=False, null=True)
    gallery_image = models.FileField(upload_to='images/', null=True, blank=False)
    image_caption = models.CharField(max_length=100)

    def __str__(self):
        return self.image_caption


class Page(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, blank=False, null=True)
    IS = (('Header', 'Header'),
          ('Footer', 'Footer'))
    page_location = models.CharField(max_length=100, blank=False, choices=IS)
    page_title = models.CharField(max_length=100)
    page_description = models.TextField(max_length=300)
    page_image = models.FileField(upload_to='images/', null=True, blank=False)

    def __str__(self):
        return self.page_title


class Slider(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, blank=False, null=True)
    slider_image = models.FileField(upload_to='sliders/', null=True, blank=False)
    image_title = models.CharField(max_length=100)

    def __str__(self):
        return self.image_title

class About(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, blank=False, null=True)
    about_image = models.FileField(upload_to='about/', null=True, blank=False)
    about = models.TextField(max_length=500)

    def __str__(self):
        return self.about

class Paypal(models.Model):
    paypal_email = models.CharField(max_length=100)
    is_demo = models.CharField(max_length=130, blank=False, choices=OPTIONS)
    paypal_extra_charge = models.CharField(max_length=100)
    is_active = models.CharField(max_length=130, blank=False, choices=OPTIONS)
    photo = models.ImageField(upload_to='avatars/', blank=False)

    def __str__(self):
        return self.paypal_email


class PayUMoney(models.Model):
    payUMoney_key = models.CharField(max_length=100)
    payUMoney_key_salt = models.CharField(max_length=100)
    is_demo = models.CharField(max_length=130, blank=False, choices=OPTIONS, default='Yes')
    payUMoney_extra_charge = models.CharField(max_length=100)
    is_active = models.CharField(max_length=130, blank=False, choices=OPTIONS)
    photo = models.ImageField(upload_to='avatars/', blank=False)

    def __str__(self):
        return self.payUMoney_key


class PayTM(models.Model):
    payTM_merchant_key = models.CharField(max_length=100)
    payTM_merchant_MID = models.CharField(max_length=100)
    payTM_website = models.CharField(max_length=100)
    payTM_industry_type = models.CharField(max_length=100, default='Retail')
    is_demo = models.CharField(max_length=130, blank=False, choices=OPTIONS, default='Yes')
    payTM_extra_charge = models.CharField(max_length=100)
    is_active = models.CharField(max_length=130, blank=False, choices=OPTIONS)
    photo = models.ImageField(upload_to='avatars/', blank=False)

    def __str__(self):
        return self.payTM_website


class Paystack(models.Model):
    sk_key = models.CharField(max_length=100)
    pk_key = models.CharField(max_length=100)
    is_demo = models.CharField(max_length=130, blank=False, choices=OPTIONS)
    extra_charge = models.CharField(max_length=100)
    is_active = models.CharField(max_length=130, blank=False, choices=OPTIONS)
    photo = models.ImageField(upload_to='avatars/', blank=False)

    def __str__(self):
        return self.sk_key


class ManageUser(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, blank=False, null=True)
    user_type = models.ForeignKey(Role, blank=False, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=True)


class smstemplate(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, blank=False, null=True)
    receiver_type = models.ForeignKey(Role, on_delete=models.CASCADE, blank=False)
    template_title = models.CharField(max_length=100)
    template = models.TextField(max_length=300)
    dynamic_tags = TaggableManager()


class emailtemplate(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    receiver_type = models.ForeignKey(Role, on_delete=models.CASCADE, blank=False)
    template_title = models.CharField(max_length=100)
    template = models.TextField(max_length=300)
    dynamic_tags = TaggableManager()


class Purpose(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    visitor_purpose = models.CharField(max_length=100)

    def __str__(self):
        return self.visitor_purpose


class Visitor(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, blank=False, null=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    to_meet_user_type = models.ForeignKey(Role, on_delete=models.CASCADE, blank=False, null=True)
    to_meet_user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=True)
    visitor_purpose = models.ForeignKey(Purpose, on_delete=models.CASCADE, blank=False, null=True)
    note = models.TextField(max_length=100)
    check_in = models.TimeField(null=True)
    check_out = models.TimeField(null=True)

    def __str__(self):
        return self.name


class Log(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, blank=False, null=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    call_duration = models.CharField(max_length=100)
    call_date = models.DateField(max_length=100)
    follow_up = models.CharField(max_length=100)
    call_type = models.CharField(max_length=100, blank=False, choices=TYPES)
    note = models.TextField(max_length=100)

    def __str__(self):
        return self.name


class Dispatch(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, blank=False, null=True)
    to_Title = models.CharField(max_length=100)
    reference = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    from_Title = models.CharField(max_length=100)
    dispatch_date = models.DateField(max_length=100)
    note = models.TextField(max_length=100)
    postal_Attachment = models.FileField(upload_to='attachments/', max_length=100, default='photo')

class Receive(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, blank=False, null=True)
    to_Title = models.CharField(max_length=100)
    reference = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    from_Title = models.CharField(max_length=100)
    receive_date = models.DateField(max_length=100)
    note = models.TextField(max_length=100)
    postal_Attachment = models.FileField(upload_to='attachments/', max_length=100)


class Leave(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    applicant_type = models.ForeignKey(Role, on_delete=models.CASCADE, blank=False)
    leave_Type = models.CharField(max_length=100)
    total_Type = models.CharField(max_length=100)


class Application(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    applicant_type = models.ForeignKey(Role, on_delete=models.CASCADE, blank=False)
    applicant = models.CharField(max_length=100)
    leave_Type = models.CharField(max_length=100)
    application_Date = models.DateField(max_length=100)
    leave_From = models.CharField(max_length=100)
    leave_To = models.CharField(max_length=100)
    leave_Reason = models.TextField(max_length=100)
    leave_attachment = models.FileField(upload_to='leave/', max_length=100)

class MonthlySalaryPaid(models.Model):
    employee_id=models.CharField(max_length=100, blank=True, null=True)
    employee = models.CharField(max_length=100)
    school = models.CharField(max_length=100)
    grade_name = models.CharField(max_length=100)
    basic_salary = models.CharField(max_length=100)
    house_rent = models.CharField(max_length=100)
    transport_allowance = models.CharField(max_length=100)
    medical_allowance = models.CharField(max_length=100)
    over_time_hourly_pay = models.CharField(max_length=100)
    provident_fund = models.CharField(max_length=100)
    hourly_rate = models.CharField(max_length=100)
    total_allowance = models.CharField(max_length=100)
    total_deduction = models.CharField(max_length=100)
    gross_salary = models.CharField(max_length=100)
    net_salary = models.CharField(max_length=100)
    over_time_total_hour = models.CharField(max_length=100)
    over_time_amount = models.CharField(max_length=100)
    Bonus = models.CharField(max_length=100)
    Penalty = models.CharField(max_length=100)
    Month = models.CharField(max_length=100)
    Payment_Method = models.CharField(max_length=100)
    Expenditure_Head = models.CharField(max_length=100)
    Bank_Name = models.CharField(max_length=100, blank=True, null=True)
    Cheque_Number = models.CharField(max_length=100, blank=True, null=True)
    note = models.CharField(max_length=100, blank=True, null=True)
