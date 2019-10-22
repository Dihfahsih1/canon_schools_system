from django import forms
from django.forms import Textarea
from django.db import transaction
from schools.models import *
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput, MonthPickerInput
from django.forms.widgets import CheckboxSelectMultiple


class SettingsForm(forms.ModelForm):
    class Meta:
        model = Settings

        fields = ('brand_name', 'brand_title', 'language', 'enable_RTL', 'enable_Frontend', 'general_Theme',
                  'default_time_zone', 'default_date', 'brand_logo', 'favicon_icon', 'brand_footer',
                  'google_Analytics')


class SchoolForm(forms.ModelForm):
    class Meta:
        model = School

        fields = ('school_name', 'school_code', 'address', 'phone', 'registration_date', 'email_address', 'fax',
                  'footer', 'currency', 'currency_symbol', 'enable_frontend', 'exam_final_result', 'latitude',
                  'longitude', 'facebook_url', 'twitter_url',
                  'online_Admission', 'api_key', 'linkedIn_url', 'google_plus_url', 'youtube_url', 'instagram_url',
                  'pinterest_url', 'status', 'frontend_Logo', 'backend_Logo', 'theme')

        widgets = {
            'registration_date': DatePickerInput(),
        }


class EmailSettingsForm(forms.ModelForm):
    class Meta:
        model = EmailSetting

        fields = ('school', 'email_protocol', 'email_type', 'char_set', 'priority', 'email_from_name',
                  'email_from_address')


class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ('school', 'role_name', 'note', 'is_default')


class DesignationForm(forms.ModelForm):
    class Meta:
        model = Designation
        fields = ('school', 'designation', 'note')


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ('feedback', 'is_publish', 'date')

        widgets = {
            'feedback': Textarea(attrs={'cols': 30, 'rows': 2}),
            'date': DatePickerInput(),
        }


class UserForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['full_name', 'national_ID', 'phone', 'gender', 'blood_group', 'religion', 'birth_date',
                  'present_address', 'permanent_address', 'email', 'username', 'other_info', 'photo']
        # 'roles'

        widgets = {
            'present_address': Textarea(attrs={'cols': 30, 'rows': 2}),
            'permanent_address': Textarea(attrs={'cols': 30, 'rows': 2}),
            'other_info': Textarea(attrs={'cols': 30, 'rows': 2}),
            'birth_date': DatePickerInput(),
        }

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class SuperuserForm(forms.ModelForm):
    class Meta:
        model = Superuser
        fields = ['roles', 'resume']

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.save()
        return user


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['school', 'responsibility', 'salary_grade', 'salary_type', 'resume', 'Is_View_on_Web', 'roles',
                  'facebook_url', 'linkedIn_url', 'twitter_url', 'google_plus_url', 'instagram_url', 'youtube_url',
                  'pinterest_url']

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(TeacherForm, self).save(commit=False)
        if commit:
            user.save()
        return user



class GuardianForm(forms.ModelForm):
    class Meta:
        model = Guardian
        fields = ['school', 'roles', 'profession']

    def save(self, commit=True):
        user = super(GuardianForm, self).save(commit=False)
        user.is_guardian = True
        if commit:
            user.save()
        return user


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('school', 'admission_no', 'admission_date', 'guardian', 'relation_With_Guardian', 'classroom',
                  'section', 'group', 'roll_no', 'registration_no', 'roles', 'caste', 'student_type',
                  'discount', 'second_language', 'previous_school', 'previous_class', 'transfer_certificate',
                  'father_name', 'father_phone', 'father_education', 'father_profession', 'father_designation',
                  'father_photo', 'mother_name', 'mother_phone', 'mother_education', 'mother_profession',
                  'mother_designation', 'mother_photo', 'health_condition')

        widgets = {
            'admission_date': DatePickerInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['classroom'].queryset = Classroom.objects.none()
        self.fields['section'].queryset = Section.objects.none()

        if 'school' in self.data:
            try:
                school_id = int(self.data.get('school'))
                self.fields['classroom'].queryset = Classroom.objects.filter(school_id=school_id).order_by('school')
            except (ValueError, TypeError):
                pass

            if 'classroom' in self.data:
                try:
                    classroom_id = int(self.data.get('classroom'))
                    self.fields['section'].queryset = Section.objects.filter(classroom_id=classroom_id).order_by(
                        'classroom')
                except (ValueError, TypeError):
                    pass
            elif self.instance.pk:
                self.fields['section'].queryset = self.instance.classroom.section_set.order_by('section')

        elif self.instance.pk:
            self.fields['classroom'].queryset = self.instance.school.classroom_set.order_by('classroom')

    def save(self, commit=True):
        user = super(StudentForm, self).save(commit=False)
        user.is_student = True
        if commit:
            user.save()
        return user


class StudentTypeForm(forms.ModelForm):
    class Meta:
        model = StudentType
        fields = ('school', 'student_type', 'note')



class ClassroomForm(forms.ModelForm):
    class Meta:
        model = Classroom
        fields = ('school', 'classroom', 'numeric_name', 'class_teacher', 'note')


class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ('school', 'section', 'classroom', 'section_teacher', 'note')


class YearForm(forms.ModelForm):
    class Meta:
        model = Year
        fields = ('school', 'start_month', 'end_month', 'is_running', 'note')

    widgets = {
        'start_month': MonthPickerInput(),
        'end_month': MonthPickerInput(),
    }


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ('school', 'subject_name', 'subject_code', 'author', 'type', 'classroom', 'subject_teacher', 'note')


class SyllabusForm(forms.ModelForm):
    class Meta:
        model = Syllabus
        fields = ('school', 'syllabus_title', 'classroom', 'subject_name', 'syllabus', 'note')


class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ('school', 'material_title', 'classroom', 'subject', 'material', 'description')


class RoutineForm(forms.ModelForm):
    class Meta:
        model = Routine
        fields = ['school', 'classroom', 'section', 'subject_name', 'day', 'teacher', 'start_time', 'end_time',
                  'room_no']

    widgets = {
        'start_time': TimePickerInput(),
        'end_time': TimePickerInput(),
    }

    def __init__(self, *args, **kwargs):
        super(RoutineForm, self).__init__(*args, **kwargs)
        self.fields["section"].queryset = Section.objects.select_related('classroom').order_by('classroom')


class BulkStudentForm(forms.ModelForm):
    class Meta:
        model = BulkStudent
        fields = ('classroom', 'section')


class StudentAttendanceForm(forms.ModelForm):
    class Meta:
        model = StudentAttendance
        fields = ('school', 'classroom', 'section', 'date')

        widgets = {
            'date': DatePickerInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['classroom'].queryset = Classroom.objects.none()
        self.fields['section'].queryset = Section.objects.none()

        if 'school' in self.data:
            try:
                school_id = int(self.data.get('school'))
                self.fields['classroom'].queryset = Classroom.objects.filter(school_id=school_id).order_by(
                    'classroom')
            except (ValueError, TypeError):
                pass

                if 'classroom' in self.data:
                    try:
                        classroom_id = int(self.data.get('classroom'))
                        self.fields['section'].queryset = Section.objects.filter(classroom_id=classroom_id).order_by(
                            'section')
                    except (ValueError, TypeError):
                        pass
                elif self.instance.pk:
                    self.fields['section'].queryset = self.instance.classroom.section_set.order_by('section')

        elif self.instance.pk:
            self.fields['classroom'].queryset = self.instance.school.classroom_set.order_by('classroom')


class TeacherAttendanceForm(forms.ModelForm):
    class Meta:
        model = StudentAttendance
        fields = ('school', 'date',)

        widgets = {
            'date': DatePickerInput(),
        }


class EmployeeAttendanceForm(forms.ModelForm):
    class Meta:
        model = StudentAttendance
        fields = ('date',)

        widgets = {
            'date': DatePickerInput(),
        }


class AbsentEmailForm(forms.ModelForm):
    class Meta:
        model = AbsentEmail
        fields = ('receiver_type', 'absent_user', 'template', 'absent_date', 'subject', 'email_body')

        widgets = {
            'absent_date': DatePickerInput(),
        }


class AbsentSMSForm(forms.ModelForm):
    class Meta:
        model = AbsentSMS
        fields = ('receiver_type', 'absent_user', 'template', 'absent_date', 'gateway')

        widgets = {
            'absent_date': DatePickerInput(),
        }


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ('school', 'assignment_title', 'classroom', 'subject', 'deadline', 'assignment', 'note')


class ExamGradeForm(forms.ModelForm):
    class Meta:
        model = ExamGrade
        fields = ('school', 'exam_grade', 'grade_point', 'mark_from', 'mark_to', 'note')


class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ('school', 'exam_title', 'start_date', 'note')

        widgets = {
            'start_date': DatePickerInput(),
        }


class ExamScheduleForm(forms.ModelForm):
    class Meta:
        model = ExamSchedule
        fields = ('school', 'exam', 'classroom', 'subject', 'exam_date', 'start_time', 'end_time', 'room_no', 'note')

        widgets = {
            'exam_date': DatePickerInput(),
        }


class ExamSuggestionForm(forms.ModelForm):
    class Meta:
        model = ExamSuggestion
        fields = ('school', 'suggestion_title', 'exam', 'classroom', 'subject', 'suggestion', 'note')


class MarkForm(forms.ModelForm):
    class Meta:
        model = Mark
        fields = ('school', 'exam', 'classroom', 'section', 'subject', 'student')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['exam'].queryset = Exam.objects.none()
        self.fields['classroom'].queryset = Classroom.objects.none()
        self.fields['section'].queryset = Section.objects.none()
        self.fields['subject'].queryset = Subject.objects.none()

        if 'school' in self.data:
            try:
                school_id = int(self.data.get('school'))
                self.fields['exam'].queryset = Exam.objects.filter(school_id=school_id).order_by('school')
                self.fields['classroom'].queryset = Classroom.objects.filter(school_id=school_id).order_by('school')
            except (ValueError, TypeError):
                pass

            if 'classroom' in self.data:
                try:
                    classroom_id = int(self.data.get('classroom'))
                    self.fields['section'].queryset = Section.objects.filter(classroom_id=classroom_id).order_by(
                        'classroom')
                    self.fields['subject'].queryset = Subject.objects.filter(classroom_id=classroom_id).order_by(
                        'classroom')
                except (ValueError, TypeError):
                    pass
            elif self.instance.pk:
                self.fields['section'].queryset = self.instance.classroom.section_set.order_by('section')
                self.fields['subject'].queryset = self.instance.classroom.subject_set.order_by('subject')

        elif self.instance.pk:
            self.fields['classroom'].queryset = self.instance.school.classroom_set.order_by('classroom')


class ExamAttendanceForm(forms.ModelForm):
    class Meta:
        model = ExamAttendance
        fields = ('exam', 'classroom', 'section', 'subject')


class CertificateForm(forms.ModelForm):
    class Meta:
        model = CertificateType
        fields = ('school', 'certificate_name', 'school_name', 'certificate_text', 'footer_left_text',
                  'footer_middle_text', 'footer_right_text', 'background')


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('school', 'book_title', 'book_ID', 'ISBN_no', 'edition',
                  'author', 'language', 'price', 'quantity', 'almira_no', 'book_cover')


class EBookForm(forms.ModelForm):
    class Meta:
        model = EBook
        fields = (
            'school', 'classroom', 'subject', 'EBook_title', 'edition', 'author', 'language', 'cover_image', 'e_book')


class LibraryMemberForm(forms.ModelForm):
    class Meta:
        model = LibraryMember
        fields = ('school', 'photo', 'library_ID', 'name', 'classroom', 'section', 'roll_no')


class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ('school', 'select_book', 'library_member', 'ISBN_no', 'edition', 'author', 'language', 'price',
                  'quantity', 'almira_no', 'book_cover', 'return_date')

        widgets = {
            'return_date': DatePickerInput(),
        }


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ('school', 'vehicle_number', 'vehicle_model', 'driver', 'vehicle_licence', 'vehicle_contact', 'note')


class RouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = ('school', 'route_title', 'route_start', 'route_end', 'vehicle_for_route', 'stop_name', 'stop_km',
                  'stop_fare', 'note')


class TransportMemberForm(forms.ModelForm):
    class Meta:
        model = TransportMember
        fields = ('school', 'photo', 'name', 'classroom', 'section', 'roll_no', 'transport_route_name', 'stop_Name',
                  'stop_KM', 'stop_Fare')


class HostelForm(forms.ModelForm):
    class Meta:
        model = Hostel
        fields = ('school', 'hostel_name', 'hostel_type', 'address', 'note')


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ('school', 'room_no', 'room_type', 'seat_total', 'hostel', 'cost_per_seat', 'note')


class HostelMemberForm(forms.ModelForm):
    class Meta:
        model = HostelMember
        fields = ('school', 'photo', 'name', 'classroom', 'section', 'roll_no', 'hostel_name', 'room_no',
                  'room_type')


class EmailForm(forms.ModelForm):
    class Meta:
        model = Email
        fields = ('school_name', 'receiver_type', 'receiver', 'subject', 'email_body', 'attachment')


class SMSForm(forms.ModelForm):
    class Meta:
        model = SMS
        fields = ('school', 'receiver_type', 'receiver', 'SMS', 'gateway')


class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ('school', 'notice_title', 'date', 'notice_for', 'notice', 'Is_View_on_Web')

        widgets = {
            'date': DatePickerInput(),
        }


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ('school', 'news_title', 'date', 'image', 'news', 'Is_View_on_Web')

        widgets = {
            'date': DatePickerInput(),
        }


class HolidayForm(forms.ModelForm):
    class Meta:
        model = Holiday
        fields = ('school', 'holiday_title', 'from_date', 'to_date', 'note', 'Is_View_on_Web')

        widgets = {
            'from_date': DatePickerInput(),
            'to_date': DatePickerInput(),
        }


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('school', 'event_title', 'event_for', 'event_place', 'from_date', 'to_date', 'image', 'note',
                  'Is_View_on_Web')

        widgets = {
            'from_date': DatePickerInput(),
            'to_date': DatePickerInput(),
        }


class VisitorForm(forms.ModelForm):
    class Meta:
        model = Visitor
        fields = ('school', 'name', 'phone', 'to_meet_user_type', 'to_meet_user', 'visitor_purpose',
                  'check_in', 'check_out', 'note')


class PurposeForm(forms.ModelForm):
    class Meta:
        model = Purpose
        fields = ('school', 'visitor_purpose')


class LogForm(forms.ModelForm):
    class Meta:
        model = Log
        fields = ('school', 'name', 'phone', 'call_duration', 'call_date', 'follow_up', 'call_type', 'note')


class LeaveForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = ('school', 'applicant_type', 'leave_Type', 'total_Type')


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ('school', 'applicant_type', 'applicant', 'leave_Type', 'application_Date', 'leave_From', 'leave_To',
                  'leave_Reason', 'leave_attachment')


class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ('school', 'border_color', 'top_background', 'card_school_name', 'school_name_font_size',
                  'school_name_color', 'school_address', 'school_address_color', 'admit_card_font_size',
                  'admit_card_color', 'admit_card_background', 'title_font_size', 'title_color', 'value_font_size',
                  'value_color', 'exam_font_size', 'exam_color', 'subject_font_size', 'subject_color',
                  'bottom_signature', 'signature_background', 'signature_color', 'signature_align', 'admit_card_logo')


class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ('school', 'classroom', 'section', 'student', 'activity_date', 'activity')


class DiscountForm(forms.ModelForm):
    class Meta:
        model = Discount
        fields = ('school', 'title', 'amount', 'note')


class DispatchForm(forms.ModelForm):
    class Meta:
        model = Dispatch
        fields = (
            'school', 'to_Title', 'reference', 'address', 'from_Title', 'dispatch_date', 'note', 'postal_Attachment')


class ReceiveForm(forms.ModelForm):
    class Meta:
        model = Receive
        fields = (
            'school', 'to_Title', 'reference', 'address', 'from_Title', 'receive_date', 'note', 'postal_Attachment')


class FeeTypeForm(forms.ModelForm):
    class Meta:
        model = FeeType
        fields = ('school', 'fee_type', 'fee_title', 'note', 'Class', 'Class_Amount')


class BulkInvoiceForm(forms.ModelForm):
    class Meta:
        model = BulkInvoice
        fields = ('classroom', 'fee_type', 'student_name', 'is_discount_applicable',
                  'month', 'paid_status', 'note')


class DueFeeEmailForm(forms.ModelForm):
    class Meta:
        model = DueFeeEmail
        fields = ('school', 'receiver_role', 'classroom', 'due_fee_student', 'template',
                  'subject', 'email_body', 'attachment')


class DueFeeSMSForm(forms.ModelForm):
    class Meta:
        model = DueFeeSMS
        fields = ('school', 'receiver_type', 'classroom', 'due_fee_student', 'template',
                  'SMS', 'gateway')


class IncomeHeadForm(forms.ModelForm):
    class Meta:
        model = IncomeHead
        fields = ('school', 'income_head', 'note')



class ExpenditureHeadForm(forms.ModelForm):
    class Meta:
        model = ExpenditureHead
        fields = ('school', 'expenditure_head', 'note')


class ExpenditureForm(forms.ModelForm):
    class Meta:
        model = Expenditure
        fields = ('school', 'expenditure_head', 'expenditure_method', 'amount', 'date', 'note')

        widgets = {
            'date': DatePickerInput(),
        }


class GalleryForm(forms.ModelForm):
    class Meta:
        model = Gallery
        fields = ('school', 'gallery_title', 'note', 'Is_View_on_Web')


class PaypalForm(forms.ModelForm):
    class Meta:
        model = Paypal
        fields = ('paypal_email', 'is_demo', 'paypal_extra_charge', 'is_active', 'photo')


class PayUMoneyForm(forms.ModelForm):
    class Meta:
        model = PayUMoney
        fields = ('payUMoney_key', 'payUMoney_key_salt', 'is_demo', 'payUMoney_extra_charge', 'is_active', 'photo')


class PayTMForm(forms.ModelForm):
    class Meta:
        model = PayTM
        fields = ('payTM_merchant_key', 'payTM_merchant_MID', 'payTM_website', 'payTM_industry_type', 'is_demo',
                  'payTM_extra_charge', 'is_active', 'photo')


class PaystackForm(forms.ModelForm):
    class Meta:
        model = Paystack
        fields = ('sk_key', 'pk_key', 'is_demo', 'extra_charge', 'is_active', 'photo')


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('school', 'gallery_title', 'gallery_image', 'image_caption')


class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ('school', 'page_location', 'page_title', 'page_description', 'page_image')


class SliderForm(forms.ModelForm):
    class Meta:
        model = Slider
        fields = ('school', 'slider_image', 'image_title')


class TypeForm(forms.ModelForm):
    class Meta:
        model = Type
        fields = ('school', 'complain_type')


class ComplainForm(forms.ModelForm):
    class Meta:
        model = Complain
        fields = ('school', 'complain_user_type', 'complain_user', 'complain_type', 'complain_date', 'complain',
                  'action_date')


class AboutForm(forms.ModelForm):
    class Meta:
        model = About
        fields = ('school', 'about', 'about_image')


class SMSTemplateForm(forms.ModelForm):
    class Meta:
        model = smstemplate
        fields = ('school', 'receiver_type', 'template_title', 'template', 'dynamic_tags')


class EmailTemplateForm(forms.ModelForm):
    class Meta:
        model = emailtemplate
        fields = ('school', 'receiver_type', 'template_title', 'dynamic_tags', 'template')


class AttendanceForm(forms.Form):
    school = forms.ModelChoiceField(
        queryset=School.objects.all(),
        required=False
    )

    classroom = forms.ModelChoiceField(
        queryset=Classroom.objects.none(),
        required=False
    )

    section = forms.ModelChoiceField(
        queryset=Section.objects.none(),
        required=False
    )

    class Meta:
        fields = ('classroom', 'section')

    def __init__(self, school=None, classroom=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['classroom'].queryset = Classroom.objects.filter(school=school)
        if classroom:
            self.fields['section'].queryset = Section.objects.filter(
                classroom=classroom)

#creating the invoice table model with the fields
class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ('school', 'classroom', 'student', 'fee_type', 'fee_amount', 'month',
                  'is_discount_applicable', 'paid_status', 'Payment_Method',
                   'Cheque_Number','Bank_Name','note')
        widgets = {
            'note': Textarea(attrs={'cols': 30, 'rows': 2}),
            'month': MonthPickerInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['classroom'].queryset = Classroom.objects.none()
        self.fields['fee_type'].queryset = FeeType.objects.none()
        self.fields['student'].queryset = Student.objects.none()
        self.fields['fee_amount'].queryset = FeeType.objects.none()

        if 'school' in self.data:
            try:
                school_id = int(self.data.get('school'))
                fee_type_id = int(self.data.get('fee_type'))
                self.fields['fee_type'].queryset = FeeType.objects.filter(school_id=school_id).order_by('school')
                self.fields['classroom'].queryset = Classroom.objects.filter(school_id=school_id).order_by('school')
                self.fields['fee_amount'].queryset = FeeType.objects.filter(id=fee_type_id).order_by('Class_Amount')
            except (ValueError, TypeError):
                pass

            if 'classroom' in self.data:
                try:
                    classroom_id = int(self.data.get('classroom'))
                    self.fields['student'].queryset = Student.objects.filter(classroom_id=classroom_id).order_by(
                        'classroom')
                except (ValueError, TypeError):
                    pass
            elif self.instance.pk:
                self.fields['student'].queryset = self.instance.classroom.student_set.order_by('student')

            if 'fee_type' in self.data:
                try:
                    fee_type_id = int(self.data.get('fee_type'))
                    self.fields['fee_amount'].queryset = FeeType.objects.filter(id=fee_type_id).order_by('Class_Amount')
                except (ValueError, TypeError):
                    pass
            elif self.instance.pk:
                self.fields['fee_amount'].queryset = self.instance.fee_title.Class_Amount_set.order_by('Class_Amount')

        elif self.instance.pk:
            self.fields['classroom'].queryset = self.instance.school.classroom_set.order_by('classroom')
class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ('school', 'income_head', 'payment_method', 'amount', 'date', 'note', 'Bank_Name', 'Cheque_Number')

        widgets = {
            'date': DatePickerInput(),
        }
class SalaryGradeForm(forms.ModelForm):
    class Meta:
        model = SalaryGrade
        fields = ('school','payee', 'grade_name', 'basic_salary', 'house_rent', 'transport_allowance', 'medical_allowance',
                  'over_time_hourly_pay', 'provident_fund', 'hourly_rate', 'total_allowance', 'total_deduction',
                  'gross_salary', 'net_salary','over_time_total_hour','over_time_amount','Bonus','Penalty','Month','Payment_Method','Expenditure_Head','Cheque_Number', 'Bank_Name', 'note')

        widgets = {
            'note': Textarea(attrs={'cols': 30, 'rows': 2}),
        }
class ManageUserForm(forms.ModelForm):
    class Meta:
        model = ManageUser
        fields = ('school', 'user_type', 'user',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_type'].queryset = Role.objects.none()
        self.fields['user'].queryset = User.objects.none()

        if 'school' in self.data:
            try:
                school_id = int(self.data.get('school'))
                self.fields['user_type'].queryset = Role.objects.filter(school_id=school_id).order_by('role_name')
            except (ValueError, TypeError):
                pass

                if 'user_type' in self.data:
                    try:
                        user_type_id = int(self.data.get('user_type'))
                        self.fields['user'].queryset = User.objects.filter(roles_id=user_type_id).order_by(
                            'full_name')
                    except (ValueError, TypeError):
                        pass
                elif self.instance.pk:
                    self.fields['user'].queryset = self.instance.role.user_set.order_by('full_name')

        elif self.instance.pk:
            self.fields['user_type'].queryset = self.instance.school.role_set.order_by('role_name')


class SalaryPaymentForm(forms.ModelForm):
    class Meta:
        model = SalaryPayment
        fields = ('school','role','employee')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['role'].queryset = Role.objects.none()
        self.fields['employee'].queryset = Employee.objects.none()

        if 'school' in self.data:
            try:
                school_id = int(self.data.get('school'))
                self.fields['role'].queryset = Role.objects.filter(school_id=school_id).order_by(
                    'role_name')
            except (ValueError, TypeError):
                pass

                if 'role' in self.data:
                    try:
                        rolesId = int(self.data.get('role'))
                        self.fields['employee'].queryset = Employee.objects.filter(roles_id=rolesId).order_by(
                            'user')

                    except (ValueError, TypeError):
                        pass



class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['school', 'designation', 'salary_grade', 'salary_type', 'resume', 'Is_View_on_Web', 'roles',
                  'facebook_url', 'linkedIn_url', 'twitter_url', 'google_plus_url', 'instagram_url', 'youtube_url',
                  'pinterest_url']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['designation'].queryset = Designation.objects.none()
        self.fields['salary_grade'].queryset = SalaryGrade.objects.none()
        if 'school' in self.data:
            try:
                school_id = int(self.data.get('school'))
                self.fields['designation'].queryset = Designation.objects.filter(school_id=school_id).order_by('designation')
                self.fields['salary_grade'].queryset = SalaryGrade.objects.filter(school_id=school_id).order_by('grade_name')
            except (ValueError, TypeError):
                pass

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(EmployeeForm, self).save(commit=False)
        user.is_employee = True
        if commit:
            user.save()
        return user
