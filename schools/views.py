import random
import string

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.views.generic import CreateView, UpdateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView
from bootstrap_datepicker_plus import DatePickerInput
from django.http import HttpResponseRedirect, HttpResponseForbidden, Http404

from .forms import *
from .models import *

IMAGE_FILE_TYPES = ['png', 'jpg', 'pjeg']


def login_user(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(email=email, password=password, backend='django.contrib.auth.backends.ModelBackend')
        if user is not None:
            if user.is_active:
                login(request, user)
                return render(request, 'home/home.html')
            else:
                return render(request, 'home/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'home/login.html', {'error_message': 'Invalid login'})
    return render(request, 'home/login.html')


def logout_user(request):
    logout(request)
    return render(request, 'home/login.html')


def index(request):
    student_count = Student.objects.all().count()
    guardian_count = Guardian.objects.all().count()
    employee_count = Employee.objects.all().count()
    teacher_count = Teacher.objects.all().count()
    income_count = Income.objects.all().count()
    expenditure_count = Expenditure.objects.all().count()
    context = {
        'student_count': student_count,
        'guardian_count': guardian_count,
        'employee_count': employee_count,
        'teacher_count': teacher_count,
    }
    return render(request, 'home/home.html', context)


# def view_profile(request):
#     return render(request, 'profiles/profile.html')

class UserProfileView(DetailView):
    model = User
    template_name = 'profiles/profile.html'
    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'


class ProfileUpdateView(UpdateView):
    model = User
    template_name = 'profiles/update_profile.html'
    fields = ('full_name', 'phone', 'present_address', 'permanent_address', 'gender', 'blood_group', 'religion',
              'birth_date', 'email', 'photo', 'other_info')

    def get_form(self):
        form = super().get_form()
        form.fields['birth_date'].widget = DatePickerInput()
        return form

    # send the user back to their own page after a successful update
    def get_success_url(self):
        return reverse('profile',
                       kwargs={'username': self.request.user.username})

    def get_object(self):
        # Only get the User record for the user making the request
        return User.objects.get(username=self.request.user.username)


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect(reverse('profile'))
        else:
            return redirect(reverse('change_password'))
    else:
        form = PasswordChangeForm(user=request.user)

        args = {'form': form}
        return render(request, 'home/change_password.html', args)

    # #######################################===>BEGINNING OF SCHOOL MODULE<===########################################


class SchoolCreateView(CreateView):
    model = School
    template_name = 'schools/create_school.html'
    fields = ('school_name', 'school_code', 'address', 'phone', 'registration_date', 'email_address', 'fax',
              'footer', 'currency', 'currency_symbol', 'api_key',
              'online_Admission', 'enable_frontend', 'exam_final_result', 'latitude', 'longitude', 'facebook_url',
              'twitter_url', 'linkedIn_url', 'google_plus_url', 'youtube_url', 'instagram_url', 'pinterest_url',
              'status', 'frontend_Logo', 'backend_Logo', 'theme')

    def get_form(self):
        form = super().get_form()
        form.fields['registration_date'].widget = DatePickerInput()
        return form

    def form_valid(self, form):
        school = form.save(commit=False)
        school.save()
        return redirect('school_list')


class SchoolUpdateView(UpdateView):
    model = School
    template_name = 'schools/update_school.html'
    pk_url_kwarg = 'school_pk'
    fields = ('school_name', 'school_code', 'address', 'phone', 'registration_date', 'email_address', 'fax',
              'footer', 'currency', 'currency_symbol', 'api_key',
              'online_Admission', 'enable_frontend', 'exam_final_result', 'latitude', 'longitude', 'facebook_url',
              'twitter_url', 'linkedIn_url', 'google_plus_url', 'youtube_url', 'instagram_url', 'pinterest_url',
              'status', 'frontend_Logo', 'backend_Logo', 'theme')

    def get_form(self):
        form = super().get_form()
        form.fields['registration_date'].widget = DatePickerInput()
        return form

    def form_valid(self, form):
        school = form.save(commit=False)
        school.save()
        return redirect('school_list')


class SchoolListView(ListView):
    model = School
    template_name = 'schools/school_list.html'
    context_object_name = 'schools'


def save_school_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            schools = School.objects.all()
            data['html_school_list'] = render_to_string('schools/includes/partial_school_list.html', {
                'schools': schools
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def school_view(request, school_pk):
    school = get_object_or_404(School, pk=school_pk)
    if request.method == 'POST':
        form = SchoolForm(request.POST, instance=school)
    else:
        form = SchoolForm(instance=school)
    return save_school_form(request, form, 'schools/includes/partial_school_view.html')


def school_delete(request, school_pk):
    school = get_object_or_404(School, pk=school_pk)
    data = dict()
    if request.method == 'POST':
        school.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        schools = School.objects.all()
        data['html_school_list'] = render_to_string('schools/includes/partial_school_list.html', {
            'schools': schools
        })
    else:
        context = {'school': school}
        data['html_form'] = render_to_string('schools/includes/partial_school_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


class SchoolSettingView(UpdateView):
    model = School
    template_name = 'schools/school_setting.html'
    pk_url_kwarg = 'school_pk'
    fields = ('school_name', 'school_code', 'address', 'phone', 'registration_date', 'email_address', 'fax',
              'footer', 'currency', 'currency_symbol', 'session_start_month', 'session_end_month', 'api_key',
              'online_Admission', 'enable_frontend', 'exam_final_result', 'latitude', 'longitude', 'facebook_url',
              'twitter_url', 'linkedIn_url', 'google_plus_url', 'youtube_url', 'instagram_url', 'pinterest_url',
              'status', 'frontend_Logo', 'backend_Logo', 'theme')

    def form_valid(self, form):
        school = form.save(commit=False)
        school.save()
        return redirect('school_list')


class SettingsView(UpdateView):
    model = Settings
    template_name = 'settings/settings.html'
    pk_url_kwarg = 'settings_pk'
    fields = ('brand_name', 'brand_title', 'language', 'enable_RTL', 'enable_Frontend', 'general_Theme',
              'default_time_zone', 'default_date', 'brand_logo', 'favicon_icon', 'brand_footer',
              'google_Analytics')

    def form_valid(self, form):
        school = form.save(commit=False)
        school.save()
        return redirect('school_list')

    # #######################################===>END OF SCHOOL MODULE<===########################################

    # #######################################===>BEGINNING OF CLASS MODULE<===###################################


class ClassroomListView(ListView):
    model = Classroom
    template_name = 'classrooms/classroom_list.html'
    context_object_name = 'classrooms'


class ClassroomCreateView(CreateView):
    model = Classroom
    template_name = 'classrooms/classroom_create.html'
    fields = ('school', 'classroom', 'numeric_name', 'class_teacher', 'note')

    def form_valid(self, form):
        classroom = form.save(commit=False)
        classroom.save()
        return redirect('classroom_list')


class ClassroomUpdateView(UpdateView):
    model = Classroom
    template_name = 'classrooms/update_classroom.html'
    pk_url_kwarg = 'classroom_pk'
    fields = ('school', 'classroom', 'numeric_name', 'class_teacher', 'note')

    def form_valid(self, form):
        classroom = form.save(commit=False)
        classroom.save()
        return redirect('classroom_list')


def save_classroom_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            classrooms = Classroom.objects.all()
            data['html_classroom_list'] = render_to_string('classrooms/includes/partial_classroom_list.html', {
                'classrooms': classrooms
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def classroom_delete(request, classroom_pk):
    classroom = get_object_or_404(Classroom, pk=classroom_pk)
    data = dict()
    if request.method == 'POST':
        classroom.delete()
        data['form_is_valid'] = True
        classrooms = Classroom.objects.all()
        data['html_classroom_list'] = render_to_string('classrooms/includes/partial_classroom_list.html', {
            'classrooms': classrooms
        })
    else:
        context = {'classroom': classroom}
        data['html_form'] = render_to_string('classrooms/includes/partial_classroom_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)

    # #######################################===>END OF CLASS MODULE<===########################################

    # #######################################===>BEGINNING OF SECTION MODULE<===###################################


class SectionListView(ListView):
    model = Section
    template_name = 'sections/section_list.html'
    context_object_name = 'sections'


def save_section_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            sections = Section.objects.all()
            data['html_section_list'] = render_to_string('sections/includes/partial_section_list.html', {
                'sections': sections
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


class SectionCreateView(CreateView):
    model = Section
    template_name = 'sections/section_create.html'
    fields = ('school', 'section', 'classroom', 'section_teacher', 'note')

    def form_valid(self, form):
        school = form.save(commit=False)
        school.save()
        return redirect('section_list')


class SectionUpdateView(UpdateView):
    model = Section
    template_name = 'sections/section_update.html'
    pk_url_kwarg = 'section_pk'
    fields = ('school', 'section', 'classroom', 'section_teacher', 'note')

    def form_valid(self, form):
        school = form.save(commit=False)
        school.save()
        return redirect('section_list')


def section_delete(request, section_pk):
    section = get_object_or_404(Section, pk=section_pk)
    data = dict()
    if request.method == 'POST':
        section.delete()
        data['form_is_valid'] = True
        sections = Section.objects.all()
        data['html_section_list'] = render_to_string('sections/includes/partial_section_list.html', {
            'sections': sections
        })
    else:
        context = {'section': section}
        data['html_form'] = render_to_string('sections/includes/partial_section_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)

    # #######################################===>END OF SECTION MODULE<===########################################

    # #######################################===>BEGINNING OF Email Setting MODULE<===################################


class EmailSettingsListView(ListView):
    model = EmailSetting
    template_name = 'emailsettings/emailsetting_list.html'
    context_object_name = 'emailsettings'


class EmailSettingsCreateView(CreateView):
    model = EmailSetting
    template_name = 'emailsettings/emailsetting_create.html'
    fields = ('school', 'email_protocol', 'email_type', 'char_set', 'priority', 'email_from_name',
              'email_from_address')

    def form_valid(self, form):
        emailsetting = form.save(commit=False)
        emailsetting.save()
        return redirect('emailsetting_list')


class EmailSettingsUpdateView(UpdateView):
    model = EmailSetting
    template_name = 'emailsettings/update_emailsetting.html'
    pk_url_kwarg = 'emailsetting_pk'
    fields = ('school', 'email_protocol', 'email_type', 'char_set', 'priority', 'email_from_name',
              'email_from_address')

    def form_valid(self, form):
        emailsetting = form.save(commit=False)
        emailsetting.save()
        return redirect('emailsetting_list')


def save_emailsetting_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            emailsettings = EmailSetting.objects.all()
            data['html_emailsetting_list'] = render_to_string('emailsettings/includes/partial_emailsetting_list.html', {
                'emailsettings': emailsettings
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def emailsetting_view(request, emailsetting_pk):
    emailsetting = get_object_or_404(EmailSetting, pk=emailsetting_pk)
    if request.method == 'POST':
        form = EmailSettingsForm(request.POST, instance=emailsetting)
    else:
        form = EmailSettingsForm(instance=emailsetting)
    return save_emailsetting_form(request, form, 'emailsettings/includes/partial_emailsetting_view.html')


def emailsetting_delete(request, emailsetting_pk):
    emailsetting = get_object_or_404(EmailSetting, pk=emailsetting_pk)
    data = dict()
    if request.method == 'POST':
        emailsetting.delete()
        data['form_is_valid'] = True
        emailsettings = emailsetting.objects.all()
        data['html_emailsetting_list'] = render_to_string('emailsettings/includes/partial_emailsetting_list.html', {
            'emailsettings': emailsettings
        })
    else:
        context = {'emailsetting': emailsetting}
        data['html_form'] = render_to_string('emailsettings/includes/partial_emailsetting_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)

    # #######################################===>END OF Email Setting MODULE<===######################################

    # #######################################===>BEGINNING OF ROLE MODULE<===###################################


class RoleListView(ListView):
    model = Role
    template_name = 'roles/role_list.html'
    context_object_name = 'roles'


class RoleCreateView(CreateView):
    model = Role
    template_name = 'roles/role_create.html'
    fields = ('school', 'role_name', 'note', 'is_default')

    def form_valid(self, form):
        role = form.save(commit=False)
        role.save()
        return redirect('role_list')


class RoleUpdateView(UpdateView):
    model = Role
    template_name = 'roles/update_role.html'
    pk_url_kwarg = 'role_pk'
    fields = ('school', 'role_name', 'note', 'is_default')

    def form_valid(self, form):
        role = form.save(commit=False)
        role.save()
        return redirect('role_list')


def save_role_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            roles = Role.objects.all()
            data['html_role_list'] = render_to_string('roles/includes/partial_role_list.html', {
                'roles': roles
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def role_delete(request, role_pk):
    role = get_object_or_404(Role, pk=role_pk)
    data = dict()
    if request.method == 'POST':
        role.delete()
        data['form_is_valid'] = True
        roles = Role.objects.all()
        data['html_role_list'] = render_to_string('roles/includes/partial_role_list.html', {
            'roles': roles
        })
    else:
        context = {'role': role}
        data['html_form'] = render_to_string('roles/includes/partial_role_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF ROLE MODULE<===########################################

# #######################################===>BEGINNING OF SUPERUSER MODULE<===###################################


class SuperuserListView(ListView):
    model = Superuser
    template_name = 'superusers/superuser_list.html'
    context_object_name = 'superusers'


def save_superuser_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            superusers = Superuser.objects.all()
            data['html_superuser_list'] = render_to_string('superusers/includes/partial_superuser_list.html', {
                'superusers': superusers
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def superuser_create(request):
    temp_password = ''.join([random.choice(string.ascii_letters + string.digits + '-_') for ch in range(8)])

    if request.method == 'POST':
        form = UserForm(request.POST or None, request.FILES or None)
        superuser_form = SuperuserForm(request.POST or None, request.FILES or None)

        if form.is_valid() and superuser_form.is_valid():
            user = form.save(commit=False)
            user.is_superuser = True
            user.save()

            user.superuser.roles = superuser_form.cleaned_data.get('roles')
            user.superuser.resume = superuser_form.cleaned_data.get('resume')
            user.superuser.save()

            return redirect('superuser_list')

    else:
        form = UserForm()
        superuser_form = SuperuserForm()

    context = {
        'form': form,
        'temp_password': temp_password,
        'superuser_form': superuser_form
    }
    return render(request, 'superusers/superuser_create.html', context)


def superuser_view(request, superuser_pk):
    superuser = get_object_or_404(Superuser, pk=superuser_pk)
    if request.method == 'POST':
        form = SuperuserForm(request.POST, instance=superuser)
    else:
        form = SuperuserForm(instance=superuser)
    return save_superuser_form(request, form, 'superusers/includes/partial_superuser_view.html')


def superuser_update(request, superuser_pk):
    superuser = get_object_or_404(Superuser, pk=superuser_pk)
    user = get_object_or_404(User, pk=superuser_pk)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        superuser_form = SuperuserForm(request.POST, instance=superuser)
    else:
        form = UserForm(instance=user)
        superuser_form = SuperuserForm(instance=superuser)
    context = {
        'form': form,
        'superuser_form': superuser_form
    }
    return render(request, 'superusers/superuser_update.html', context)


def superuser_delete(request, superuser_pk):
    superuser = get_object_or_404(Superuser, pk=superuser_pk)
    data = dict()
    if request.method == 'POST':
        superuser.delete()
        data['form_is_valid'] = True
        superusers = Superuser.objects.all()
        data['html_superuser_list'] = render_to_string('superusers/includes/partial_superuser_list.html', {
            'superusers': superusers
        })
    else:
        context = {'superuser': superuser}
        data['html_form'] = render_to_string('superusers/includes/partial_superuser_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)

    # #######################################===>END OF SUPERUSER MODULE<===######################################


# #######################################===>BEGINNING OF MANAGE USER MODULE<===######################################


def manage_user(request):
    context = {}

    school = request.GET.get('school')
    role = request.GET.get('user_type')
    context['form'] = ManageUserForm(school, role)
    # Filter
    q = request.GET.get('user')
    if q:
        q = q.replace('.', '')
        users = User.objects.filter(id__in=q).order_by('full_name')
        context['users'] = users
        return render(request, 'users/test.html', context)
    return render(request, 'users/manage_users.html', context)


# #######################################===>END OF MANAGE USER MODULE<===######################################


# #######################################===>BEGINNING OF BACKUP MODULE<===##################################


def backup(request):
    return render(request, 'backup/backup.html')


# #######################################===>END OF BACKUP MODULE<===######################################


# #######################################===>BEGINNING OF USER CREDENTIAL MODULE<===##################################


def manage_credential(request):
    context = {}

    school = request.GET.get('school')
    role = request.GET.get('user_type')
    context['form'] = ManageUserForm(school, role)
    # Filter
    users = request.GET.get('user')
    if users:
        users = users.replace('.', '')
        users = User.objects.filter(full_name=str(users))
        context['users'] = users

    return render(request, 'users/credentials.html', context)


# #######################################===>END OF USER CREDENTIAL MODULE<===######################################


# #######################################===>BEGINNING OF ACTIVITY LOG MODULE<===##################################


def activity(request):
    context = {}

    school = request.GET.get('school')
    role = request.GET.get('user_type')
    context['form'] = ManageUserForm(school, role)
    # Filter
    users = request.GET.get('user')
    if users:
        users = users.replace('.', '')
        users = User.objects.filter(full_name=str(users))
        context['users'] = users

    return render(request, 'users/activity.html', context)


# #######################################===>END OF ACTIVITY LOG MODULE<===######################################


# ####################################===>BEGINNING OF FEEDBACK MODULE<===########################################


class FeedbackListView(ListView):
    model = Feedback
    template_name = 'feedbacks/feedback_list.html'
    context_object_name = 'feedbacks'


# class FeedbackCreateView(CreateView):
#     model = Feedback
#     template_name = 'feedbacks/feedback_create.html'
#     fields = ('feedback', 'is_publish', 'date')
#
#     def form_valid(self, form):
#         feedback = form.save(commit=False)
#         feedback.save()
#         return redirect('feedback_list')


class FeedbackUpdateView(UpdateView):
    model = Feedback
    template_name = 'feedbacks/update_feedback.html'
    pk_url_kwarg = 'feedback_pk'
    fields = ('feedback', 'is_publish', 'date')

    def form_valid(self, form):
        feedback = form.save(commit=False)
        feedback.save()
        return redirect('feedback_list')


def save_feedback_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            feedbacks = Feedback.objects.all()
            data['html_feedback_list'] = render_to_string('feedbacks/includes/partial_feedback_list.html', {
                'feedbacks': feedbacks
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def feedback_delete(request, feedback_pk):
    feedback = get_object_or_404(Feedback, pk=feedback_pk)
    data = dict()
    if request.method == 'POST':
        feedback.delete()
        data['form_is_valid'] = True
        feedbacks = Feedback.objects.all()
        data['html_feedback_list'] = render_to_string('feedbacks/includes/partial_feedback_list.html', {
            'feedbacks': feedbacks
        })
    else:
        context = {'feedback': feedback}
        data['html_form'] = render_to_string('feedbacks/includes/partial_feedback_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# ####################################### ===>END OF FEEDBACK MODULE<===########################################


# #######################################===>BEGINNING OF STUDENT MODULE<===######################################


class StudentListView(ListView):
    model = Student
    template_name = 'students/student_list.html'
    context_object_name = 'students'


class OnlineStudentListView(ListView):
    model = Student
    template_name = 'students/online_list.html'
    context_object_name = 'students'


def save_student_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            students = Student.objects.all()
            data['html_student_list'] = render_to_string('students/includes/partial_student_list.html', {
                'students': students
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def student_create(request):
    form = UserForm(request.POST or None, request.FILES or None)
    student_form = StudentForm(request.POST or None, request.FILES or None)

    if form.is_valid() and student_form.is_valid():
        user = form.save(commit=False)
        user.is_student = True
        user.save()

        user.student.school = student_form.cleaned_data.get('school')
        user.student.admission_no = student_form.cleaned_data.get('admission_no')
        user.student.admission_date = student_form.cleaned_data.get('admission_date')
        user.student.guardian = student_form.cleaned_data.get('guardian')
        user.student.relation_With_Guardian = student_form.cleaned_data.get('relation_With_Guardian')
        user.student.classroom = student_form.cleaned_data.get('classroom')
        user.student.section = student_form.cleaned_data.get('section')
        user.student.group = student_form.cleaned_data.get('group')
        user.student.roll_no = student_form.cleaned_data.get('roll_no')
        user.student.registration_no = student_form.cleaned_data.get('registration_no')
        user.student.roles = student_form.cleaned_data.get('roles')
        user.student.discount = student_form.cleaned_data.get('discount')
        user.student.second_language = student_form.cleaned_data.get('second_language')
        user.student.previous_school = student_form.cleaned_data.get('previous_school')
        user.student.previous_class = student_form.cleaned_data.get('previous_class')
        user.student.transfer_certificate = student_form.cleaned_data.get('transfer_certificate')
        user.student.father_name = student_form.cleaned_data.get('father_name')
        user.student.father_phone = student_form.cleaned_data.get('father_phone')
        user.student.father_education = student_form.cleaned_data.get('father_education')
        user.student.father_profession = student_form.cleaned_data.get('father_profession')
        user.student.father_designation = student_form.cleaned_data.get('father_designation')
        user.student.father_photo = student_form.cleaned_data.get('father_photo')
        user.student.mother_name = student_form.cleaned_data.get('mother_name')
        user.student.mother_phone = student_form.cleaned_data.get('mother_phone')
        user.student.mother_education = student_form.cleaned_data.get('mother_education')
        user.student.mother_profession = student_form.cleaned_data.get('mother_profession')
        user.student.mother_designation = student_form.cleaned_data.get('mother_designation')
        user.student.mother_photo = student_form.cleaned_data.get('mother_photo')
        user.student.health_condition = student_form.cleaned_data.get('health_condition')
        user.student.save()

        student_url = reverse('student_list')
        return redirect(student_url)
    context = {
        'form': form,
        'student_form': student_form,
    }
    return render(request, 'students/student_create.html', context)


def student_view(request, student_pk):
    student = get_object_or_404(Student, pk=student_pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
    else:
        form = StudentForm(instance=student)
    return save_student_form(request, form, 'students/includes/partial_student_view.html')


def student_update(request, student_pk):
    user = get_object_or_404(User, pk=student_pk)
    student = get_object_or_404(Student, pk=student_pk)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        student_form = StudentForm(request.POST, instance=student)
    else:
        form = StudentForm(instance=user)
        student_form = StudentForm(instance=student)
    context = {
        'form': form,
        'student_form': student_form
    }
    return render(request, 'students/student_update.html', context)


def student_delete(request, student_pk):
    student = get_object_or_404(Student, pk=student_pk)
    data = dict()
    if request.method == 'POST':
        student.delete()
        data['form_is_valid'] = True
        students = student.objects.all()
        data['html_student_list'] = render_to_string('students/includes/partial_student_list.html', {
            'students': students
        })
    else:
        context = {'student': student}
        data['html_form'] = render_to_string('students/includes/partial_student_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF STUDENT MODULE<===##########################################

# #######################################===>BEGINNING OF GUARDIAN MODULE<===####################################


class GuardianListView(ListView):
    model = Guardian
    template_name = 'guardians/guardian_list.html'
    context_object_name = 'guardians'


# def guardian_student_list(request):
#     books = school.book_set.all()
#     return render(request, 'books/book_list.html', {
#         'school': school,
#         'books': books,
#     })


def save_guardian_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            guardians = Guardian.objects.all()
            data['html_guardian_list'] = render_to_string('guardians/includes/partial_guardian_list.html', {
                'guardians': guardians
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def guardian_create(request):
    form = UserForm(request.POST or None, request.FILES or None)
    guardian_form = GuardianForm(request.POST or None, request.FILES or None)

    if form.is_valid() and guardian_form.is_valid():
        user = form.save(commit=False)
        user.is_guardian = True
        user.save()

        user.guardians.school = guardian_form.cleaned_data.get('school')
        user.guardians.roles = guardian_form.cleaned_data.get('roles')
        user.guardians.profession = guardian_form.cleaned_data.get('profession')
        user.guardians.save()

        guardian_url = reverse('guardian_list')
        return redirect(guardian_url)

    context = {
        'form': form,
        'guardian_form': guardian_form,
    }
    return render(request, 'guardians/guardian_create.html', context)


def guardian_view(request, guardian_pk):
    guardian = get_object_or_404(Guardian, pk=guardian_pk)
    if request.method == 'POST':
        form = GuardianForm(request.POST, instance=guardian)
    else:
        form = GuardianForm(instance=guardian)
    return save_guardian_form(request, form, 'guardians/includes/partial_guardian_view.html')


def guardian_update(request, guardian_pk):
    user = get_object_or_404(User, pk=guardian_pk)
    guardian = get_object_or_404(Guardian, pk=guardian_pk)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=guardian)
        guardian_form = GuardianForm(request.POST, instance=guardian)
    else:
        form = UserForm(instance=guardian)
        guardian_form = GuardianForm(instance=guardian)
    context = {
        'form': form,
        'guardian_form': guardian_form
    }
    return render(request, 'guardians/guardian_update.html', context)


def guardian_delete(request, guardian_pk):
    guardian = get_object_or_404(Guardian, pk=guardian_pk)
    data = dict()
    if request.method == 'POST':
        guardian.delete()
        data['form_is_valid'] = True
        guardians = Guardian.objects.all()
        data['html_guardian_list'] = render_to_string('guardians/includes/partial_guardian_list.html', {
            'guardians': guardians
        })
    else:
        context = {'guardian': guardian}
        data['html_form'] = render_to_string('guardians/includes/partial_guardian_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)

    # ####################################===>END OF GUARDIAN MODULE<===##############################################

    # ####################################===>BEGINNING OF DESIGNATION MODULE<===#####################################


class DesignationListView(ListView):
    model = Designation
    template_name = 'designations/designation_list.html'
    context_object_name = 'designations'


class DesignationCreateView(CreateView):
    model = Designation
    template_name = 'designations/designation_create.html'
    fields = ('school', 'designation', 'note')

    def form_valid(self, form):
        designation = form.save(commit=False)
        designation.save()
        return redirect('designation_list')


class DesignationUpdateView(UpdateView):
    model = Designation
    template_name = 'designations/update_designation.html'
    pk_url_kwarg = 'designation_pk'
    fields = ('school', 'designation', 'note')

    def form_valid(self, form):
        designation = form.save(commit=False)
        designation.save()
        return redirect('designation_list')


def save_designation_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            designations = Designation.objects.all()
            data['html_designation_list'] = render_to_string('designations/includes/partial_designation_list.html', {
                'designations': designations
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def designation_delete(request, designation_pk):
    designation = get_object_or_404(Designation, pk=designation_pk)
    data = dict()
    if request.method == 'POST':
        designation.delete()
        data['form_is_valid'] = True
        designations = Designation.objects.all()
        data['html_designation_list'] = render_to_string('designations/includes/partial_designation_list.html', {
            'designations': designations
        })
    else:
        context = {'designation': designation}
        data['html_form'] = render_to_string('designations/includes/partial_designation_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# ####################################### ===>END OF DESIGNATION MODULE<===########################################

# ####################################===>BEGINNING OF EMAIL TEMPLATE MODULE<===#####################################


class EmailtemplateListView(ListView):
    model = emailtemplate
    template_name = 'emailtemplates/emailtemplate_list.html'
    context_object_name = 'emailtemplates'


class EmailtemplateCreateView(CreateView):
    model = emailtemplate
    template_name = 'emailtemplates/emailtemplate_create.html'
    fields = ('school', 'receiver_type', 'template_title', 'template', 'dynamic_tags')

    def form_valid(self, form):
        emailtemplate = form.save(commit=False)
        emailtemplate.save()
        return redirect('emailtemplate_list')


class EmailtemplateUpdateView(UpdateView):
    model = emailtemplate
    template_name = 'emailtemplates/update_emailtemplate.html'
    pk_url_kwarg = 'emailtemplate_pk'
    fields = ('school', 'receiver_type', 'template_title', 'template', 'dynamic_tags')

    def form_valid(self, form):
        emailtemplate = form.save(commit=False)
        emailtemplate.save()
        return redirect('emailtemplate_list')


def save_emailtemplate_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            emailtemplates = emailtemplate.objects.all()
            data['html_emailtemplate_list'] = render_to_string(
                'emailtemplates/includes/partial_emailtemplate_list.html',
                {
                    'emailtemplates': emailtemplates
                })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def emailtemplate_delete(request, emailtemplate_pk):
    template = get_object_or_404(emailtemplate, pk=emailtemplate_pk)
    data = dict()
    if request.method == 'POST':
        template.delete()
        data['form_is_valid'] = True
        emailtemplates = emailtemplate.objects.all()
        data['html_emailtemplate_list'] = render_to_string('emailtemplates/includes/partial_emailtemplate_list.html', {
            'emailtemplates': emailtemplates
        })
    else:
        context = {'emailtemplate': emailtemplate}
        data['html_form'] = render_to_string('emailtemplates/includes/partial_emailtemplate_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# ####################################### ===>END OF EMAIL TEMPLATE MODULE<===########################################

# ####################################===>BEGINNING OF SMS TEMPLATE MODULE<===#####################################

class SmstemplateListView(ListView):
    model = smstemplate
    template_name = 'smstemplates/smstemplate_list.html'
    context_object_name = 'smstemplates'


class SmstemplateCreateView(CreateView):
    model = smstemplate
    template_name = 'smstemplates/smstemplate_create.html'
    fields = ('school', 'receiver_type', 'template_title', 'template', 'dynamic_tags')

    def form_valid(self, form):
        smstemplate = form.save(commit=False)
        smstemplate.save()
        return redirect('smstemplate_list')


class SmstemplateUpdateView(UpdateView):
    model = smstemplate
    template_name = 'smstemplates/update_smstemplate.html'
    pk_url_kwarg = 'smstemplate_pk'
    fields = ('school', 'receiver_type', 'template_title', 'template', 'dynamic_tags')

    def form_valid(self, form):
        smstemplate = form.save(commit=False)
        smstemplate.save()
        return redirect('smstemplate_list')


def save_smstemplate_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            smstemplates = smstemplate.objects.all()
            data['html_smstemplate_list'] = render_to_string(
                'smstemplates/includes/partial_smstemplate_list.html', {
                    'smstemplates': smstemplates
                })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def smstemplate_delete(request, smstemplate_pk):
    template = get_object_or_404(smstemplate, pk=smstemplate_pk)
    data = dict()
    if request.method == 'POST':
        template.delete()
        data['form_is_valid'] = True
        smstemplates = smstemplate.objects.all()
        data['html_smstemplate_list'] = render_to_string('smstemplates/includes/partial_smstemplate_list.html',
                                                         {
                                                             'smstemplates': smstemplates
                                                         })
    else:
        context = {'smstemplate': smstemplate}
        data['html_form'] = render_to_string('smstemplates/includes/partial_smstemplate_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# ####################################### ===>END OF SMS TEMPLATE MODULE<===########################################


# #######################################===>BEGINNING OF LOG MODULE<===#####################################


class LogListView(ListView):
    model = Log
    template_name = 'log/log_list.html'
    context_object_name = 'log'


class LogCreateView(CreateView):
    model = Log
    template_name = 'log/log_create.html'
    fields = ('school', 'name', 'phone', 'call_duration', 'call_date', 'follow_up', 'call_type', 'note')

    def form_valid(self, form):
        log = form.save(commit=False)
        log.save()
        return redirect('log_list')


class LogUpdateView(UpdateView):
    model = Log
    template_name = 'log/update_log.html'
    pk_url_kwarg = 'log_pk'
    fields = ('school', 'name', 'phone', 'call_duration', 'call_date', 'follow_up', 'call_type', 'note')

    def form_valid(self, form):
        log = form.save(commit=False)
        log.save()
        return redirect('log_list')


def log_view(request, log_pk):
    log = get_object_or_404(Log, pk=log_pk)
    if request.method == 'POST':
        form = LogForm(request.POST, instance=log)
    else:
        form = LogForm(instance=log)
    return save_log_form(request, form, 'log/includes/partial_log_view.html')


def save_log_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            logs = Log.objects.all()
            data['html_log_list'] = render_to_string('log/includes/partial_log_list.html', {
                'logs': logs
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def log_delete(request, log_pk):
    log = get_object_or_404(Log, pk=log_pk)
    data = dict()
    if request.method == 'POST':
        log.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        logs = Log.objects.all()
        data['html_log_list'] = render_to_string('log/includes/partial_log_list.html', {
            'logs': logs
        })
    else:
        context = {'log': log}
        data['html_form'] = render_to_string('log/includes/partial_log_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF LOG MODULE<===#####################################

# #######################################===>BEGINNING OF EMPLOYEE MODULE<===######################################


class EmployeeListView(ListView):
    model = Employee
    template_name = 'employees/employee_list.html'
    context_object_name = 'employees'


def save_employee_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            employees = Employee.objects.all()
            data['html_employee_list'] = render_to_string('employees/includes/partial_employee_list.html', {
                'employees': employees
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def employee_create(request):
    form = UserForm(request.POST or None, request.FILES or None)
    employee_form = EmployeeForm(request.POST or None, request.FILES or None)

    if form.is_valid() and employee_form.is_valid():
        user = form.save(commit=False)
        user.is_employee = True
        user.save()

        user.employee.school = employee_form.cleaned_data.get('school')
        user.employee.designation = employee_form.cleaned_data.get('designation')
        user.employee.salary_grade = employee_form.cleaned_data.get('salary_grade')
        user.employee.salary_type = employee_form.cleaned_data.get('salary_type')
        user.employee.roles = employee_form.cleaned_data.get('roles')
        user.employee.resume = employee_form.cleaned_data.get('resume')
        user.employee.Is_View_on_Web = employee_form.cleaned_data.get('Is_View_on_Web')
        user.employee.facebook_url = employee_form.cleaned_data.get('facebook_url')
        user.employee.linkedIn_url = employee_form.cleaned_data.get('linkedIn_url')
        user.employee.twitter_url = employee_form.cleaned_data.get('twitter_url')
        user.employee.google_plus_url = employee_form.cleaned_data.get('google_plus_url')
        user.employee.instagram_url = employee_form.cleaned_data.get('instagram_url')
        user.employee.youtube_url = employee_form.cleaned_data.get('youtube_url')
        user.employee.pinterest_url = employee_form.cleaned_data.get('pinterest_url')
        user.employee.save()

        employee_url = reverse('employee_list')
        return redirect(employee_url)

    context = {
        'form': form,
        'employee_form': employee_form,
    }
    return render(request, 'employees/employee_create.html', context)


def employee_view(request, employee_pk):
    employee = get_object_or_404(Employee, pk=employee_pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
    else:
        form = EmployeeForm(instance=employee)
    return save_employee_form(request, form, 'employees/includes/partial_employee_view.html')


def employee_update(request, employee_pk):
    user = get_object_or_404(User, pk=employee_pk)
    employee = get_object_or_404(Employee, pk=employee_pk)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        employee_form = EmployeeForm(request.POST, instance=employee)
    else:
        form = EmployeeForm(instance=user)
        employee_form = EmployeeForm(instance=employee)
    context = {
        'form': form,
        'employee_form': employee_form
    }
    return render(request, 'employees/employee_update.html', context)


def employee_delete(request, employee_pk):
    employee = get_object_or_404(Employee, pk=employee_pk)
    data = dict()
    if request.method == 'POST':
        employee.delete()
        data['form_is_valid'] = True
        employees = Employee.objects.all()
        data['html_employee_list'] = render_to_string('employees/includes/partial_employee_list.html', {
            'employees': employees
        })
    else:
        context = {'employee': employee}
        data['html_form'] = render_to_string('employees/includes/partial_employee_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)

    # #######################################===>END OF EMPLOYEE MODULE<===########################################

    # ###################################===>BEGINNING OF ACADEMIC YEAR MODULE<===###################################


class AcademicYearListView(ListView):
    model = Year
    template_name = 'years/year_list.html'
    context_object_name = 'years'


class AcademicYearCreateView(CreateView):
    model = Year
    template_name = 'years/year_create.html'
    fields = ('school', 'start_month', 'end_month', 'is_running', 'note')

    def get_form(self):
        form = super().get_form()
        form.fields['start_month'].widget = MonthPickerInput()
        form.fields['end_month'].widget = MonthPickerInput()
        return form

    def form_valid(self, form):
        year = form.save(commit=False)
        year.save()
        return redirect('year_list')


class AcademicYearUpdateView(UpdateView):
    model = Year
    template_name = 'years/year_update.html'
    pk_url_kwarg = 'year_pk'
    fields = ('school', 'start_month', 'end_month', 'is_running', 'note')

    def form_valid(self, form):
        year = form.save(commit=False)
        year.save()
        return redirect('year_list')


def save_year_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            years = Year.objects.all()
            data['html_year_list'] = render_to_string('years/includes/partial_year_list.html', {
                'years': years
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def year_delete(request, year_pk):
    year = get_object_or_404(Year, pk=year_pk)
    data = dict()
    if request.method == 'POST':
        year.delete()
        data['form_is_valid'] = True
        years = Year.objects.all()
        data['html_year_list'] = render_to_string('years/includes/partial_year_list.html', {
            'years': years
        })
    else:
        context = {'year': year}
        data['html_form'] = render_to_string('years/includes/partial_year_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)

    # ###################################===>END OF Academic YEAR MODULE<===###################################

    # ######################################===>BEGINNING OF TEACHER MODULE<===#################################


class TeacherListView(ListView):
    model = Teacher
    template_name = 'teachers/teacher_list.html'
    context_object_name = 'teachers'


def save_teacher_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            teachers = Teacher.objects.all()
            data['html_teacher_list'] = render_to_string('teachers/includes/partial_teacher_list.html', {
                'teachers': teachers
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def teacher_create(request):
    form = UserForm(request.POST or None, request.FILES or None)
    teacher_form = TeacherForm(request.POST or None, request.FILES or None)

    if form.is_valid() and teacher_form.is_valid():
        user = form.save(commit=False)
        user.is_teacher = True
        user.save()

        user.teacher.school = teacher_form.cleaned_data.get('school')
        user.teacher.responsibility = teacher_form.cleaned_data.get('responsibility')
        user.teacher.salary_grade = teacher_form.cleaned_data.get('salary_grade')
        user.teacher.salary_type = teacher_form.cleaned_data.get('salary_type')
        user.teacher.roles = teacher_form.cleaned_data.get('roles')
        user.teacher.resume = teacher_form.cleaned_data.get('resume')
        user.teacher.Is_View_on_Web = teacher_form.cleaned_data.get('Is_View_on_Web')
        user.teacher.facebook_url = teacher_form.cleaned_data.get('facebook_url')
        user.teacher.linkedIn_url = teacher_form.cleaned_data.get('linkedIn_url')
        user.teacher.twitter_url = teacher_form.cleaned_data.get('twitter_url')
        user.teacher.google_plus_url = teacher_form.cleaned_data.get('google_plus_url')
        user.teacher.instagram_url = teacher_form.cleaned_data.get('instagram_url')
        user.teacher.youtube_url = teacher_form.cleaned_data.get('youtube_url')
        user.teacher.pinterest_url = teacher_form.cleaned_data.get('pinterest_url')
        user.teacher.save()

        teacher_url = reverse('teacher_list')
        return redirect(teacher_url)

    context = {
        'form': form,
        'teacher_form': teacher_form,
    }
    return render(request, 'teachers/teacher_create.html', context)


def teacher_view(request, teacher_pk):
    teacher = get_object_or_404(Teacher, pk=teacher_pk)
    if request.method == 'POST':
        form = TeacherForm(request.POST, instance=teacher)
    else:
        form = TeacherForm(instance=teacher)
    return save_teacher_form(request, form, 'teachers/includes/partial_teacher_view.html')


def teacher_update(request, teacher_pk):
    user = get_object_or_404(User, pk=teacher_pk)
    teacher = get_object_or_404(Teacher, pk=teacher_pk)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=teacher.user)
        teacher_form = TeacherForm(request.POST, instance=teacher)
    else:
        form = TeacherForm(instance=teacher.user)
        teacher_form = TeacherForm(request.POST, instance=teacher)
    context = {
        'form': form,
        'teacher_form': teacher_form
    }
    return render(request, 'teachers/teacher_update.html', context)


def teacher_delete(request, teacher_pk):
    teacher = get_object_or_404(Teacher, pk=teacher_pk)
    data = dict()
    if request.method == 'POST':
        teacher.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        teachers = Teacher.objects.all()
        data['html_teacher_list'] = \
            render_to_string(
                'teachers/includes/partial_teacher_list.html', {
                    'teachers': teachers
                })
    else:
        context = {'teacher': teacher}
        data['html_form'] = \
            render_to_string(
                'teachers/includes/partial_teacher_delete.html',
                context,
                request=request,
            )
    return JsonResponse(data)


# #######################################===>END OF TEACHER MODULE<===###############################################

# #######################################===>BEGINNING OF STUDENT TYPE MODULE<===#####################################


class StudentTypeListView(ListView):
    model = StudentType
    template_name = 'student_types/student_type_list.html'
    context_object_name = 'student_types'


class StudentTypeCreateView(CreateView):
    model = StudentType
    template_name = 'student_types/student_type_create.html'
    fields = ('school', 'student_type', 'note')

    def form_valid(self, form):
        student_type = form.save(commit=False)
        student_type.save()
        return redirect('student_type_list')


class StudentTypeUpdateView(UpdateView):
    model = StudentType
    template_name = 'student_types/student_type_update.html'
    pk_url_kwarg = 'student_type_pk'
    fields = ('school', 'student_type', 'note')

    def form_valid(self, form):
        student_type = form.save(commit=False)
        student_type.save()
        return redirect('student_type_list')


def save_student_type_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            student_types = StudentType.objects.all()
            data['html_student_type_list'] = render_to_string('student_types/includes/partial_student_type_list.html', {
                'student_types': student_types
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def student_type_delete(request, student_type_pk):
    student_type = get_object_or_404(StudentType, pk=student_type_pk)
    data = dict()
    if request.method == 'POST':
        student_type.delete()
        data['form_is_valid'] = True
        student_types = StudentType.objects.all()
        data['html_student_type_list'] = render_to_string('student_types/includes/partial_student_type_list.html', {
            'student_types': student_types
        })
    else:
        context = {'student_type': student_type}
        data['html_form'] = render_to_string('student_types/includes/partial_student_type_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF STUDENT TYPE MODULE<===#####################################


# #######################################===>BEGINNING OF ACTIVITY MODULE<===#####################################


class ActivityListView(ListView):
    model = Activity
    template_name = 'activity/activity_list.html'
    context_object_name = 'activity'


class ActivityCreateView(CreateView):
    model = Activity
    template_name = 'activity/activity_create.html'
    fields = ('school', 'classroom', 'section', 'student', 'activity_date', 'activity')

    def form_valid(self, form):
        activity = form.save(commit=False)
        activity.save()
        return redirect('activity_list')


class ActivityUpdateView(UpdateView):
    model = Activity
    template_name = 'activity/update_activity.html'
    pk_url_kwarg = 'activity_pk'
    fields = ('school', 'classroom', 'section', 'student', 'activity_date', 'activity')

    def form_valid(self, form):
        activity = form.save(commit=False)
        activity.save()
        return redirect('activity_list')


def activity_view(request, activity_pk):
    activity = get_object_or_404(Activity, pk=activity_pk)
    if request.method == 'POST':
        form = ActivityForm(request.POST, instance=activity)
    else:
        form = ActivityForm(instance=activity)
    return save_activity_form(request, form, 'activity/includes/partial_activity_view.html')


def save_activity_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            activitys = Activity.objects.all()
            data['html_activity_list'] = render_to_string('activity/includes/partial_activity_list.html', {
                'activitys': activitys
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def activity_delete(request, activity_pk):
    activity = get_object_or_404(Activity, pk=activity_pk)
    data = dict()
    if request.method == 'POST':
        activity.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        activitys = Activity.objects.all()
        data['html_activity_list'] = render_to_string('activity/includes/partial_activity_list.html', {
            'activitys': activitys
        })
    else:
        context = {'activity': activity}
        data['html_form'] = render_to_string('activity/includes/partial_activity_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF ACTIVITY MODULE<===##########################################


# #######################################===>BEGINNING OF SYLLABUS MODULE<===#####################################


class SyllabusListView(ListView):
    model = Syllabus
    template_name = 'syllabus/syllabus_list.html'
    context_object_name = 'syllabus'


class SyllabusCreateView(CreateView):
    model = Syllabus
    template_name = 'syllabus/syllabus_create.html'
    fields = ('school', 'syllabus_title', 'classroom', 'subject_name', 'syllabus', 'note')

    def form_valid(self, form):
        syllabus = form.save(commit=False)
        syllabus.save()
        return redirect('syllabus_list')


class SyllabusUpdateView(UpdateView):
    model = Syllabus
    template_name = 'syllabus/update_syllabus.html'
    pk_url_kwarg = 'syllabus_pk'
    fields = ('school', 'syllabus_title', 'classroom', 'subject_name', 'syllabus', 'note')

    def form_valid(self, form):
        syllabus = form.save(commit=False)
        syllabus.save()
        return redirect('syllabus_list')


def syllabus_view(request, syllabus_pk):
    syllabus = get_object_or_404(Syllabus, pk=syllabus_pk)
    if request.method == 'POST':
        form = SyllabusForm(request.POST, instance=syllabus)
    else:
        form = SyllabusForm(instance=syllabus)
    return save_syllabus_form(request, form, 'syllabus/includes/partial_syllabus_view.html')


def save_syllabus_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            syllabuss = Syllabus.objects.all()
            data['html_syllabus_list'] = render_to_string('syllabus/includes/partial_syllabus_list.html', {
                'syllabuss': syllabuss
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def syllabus_delete(request, syllabus_pk):
    syllabus = get_object_or_404(Syllabus, pk=syllabus_pk)
    data = dict()
    if request.method == 'POST':
        syllabus.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        syllabuss = Syllabus.objects.all()
        data['html_syllabus_list'] = render_to_string('syllabus/includes/partial_syllabus_list.html', {
            'syllabuss': syllabuss
        })
    else:
        context = {'syllabus': syllabus}
        data['html_form'] = render_to_string('syllabus/includes/partial_syllabus_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF SYLLABUS MODULE<===##########################################


# #######################################===>BEGINNING OF CARD MODULE<===#####################################


class CardListView(ListView):
    model = Card
    template_name = 'card/card_list.html'
    context_object_name = 'cards'


class CardCreateView(CreateView):
    model = Card
    template_name = 'card/card_create.html'
    fields = ('school', 'border_color', 'top_background', 'card_school_name', 'school_name_font_size',
              'school_name_color', 'school_address', 'school_address_color', 'admit_card_font_size',
              'admit_card_color', 'admit_card_background', 'title_font_size', 'title_color', 'value_font_size',
              'value_color', 'exam_font_size', 'exam_color', 'subject_font_size', 'subject_color',
              'bottom_signature', 'signature_background', 'signature_color', 'signature_align', 'admit_card_logo')

    def form_valid(self, form):
        card = form.save(commit=False)
        card.save()
        return redirect('card_list')


class CardUpdateView(UpdateView):
    model = Card
    template_name = 'card/update_card.html'
    pk_url_kwarg = 'card_pk'
    fields = ('school', 'border_color', 'top_background', 'card_school_name', 'school_name_font_size',
              'school_name_color', 'school_address', 'school_address_color', 'admit_card_font_size',
              'admit_card_color', 'admit_card_background', 'title_font_size', 'title_color', 'value_font_size',
              'value_color', 'exam_font_size', 'exam_color', 'subject_font_size', 'subject_color',
              'bottom_signature', 'signature_background', 'signature_color', 'signature_align', 'admit_card_logo')

    def form_valid(self, form):
        card = form.save(commit=False)
        card.save()
        return redirect('card_list')


def card_view(request, card_pk):
    card = get_object_or_404(Card, pk=card_pk)
    if request.method == 'POST':
        form = CardForm(request.POST, instance=card)
    else:
        form = CardForm(instance=card)
    return save_card_form(request, form, 'card/includes/partial_card_view.html')


def save_card_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            cards = Card.objects.all()
            data['html_card_list'] = render_to_string('card/includes/partial_card_list.html', {
                'cards': cards
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def card_delete(request, card_pk):
    card = get_object_or_404(Card, pk=card_pk)
    data = dict()
    if request.method == 'POST':
        card.delete()
        data['form_is_valid'] = True
        cards = Card.objects.all()
        data['html_card_list'] = render_to_string('card/includes/partial_card_list.html', {
            'cards': cards
        })
    else:
        context = {'card': card}
        data['html_form'] = render_to_string('card/includes/partial_card_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF CARD MODULE<===##########################################


# #######################################===>BEGINNING OF ADMIT MODULE<===#####################################


class AdmitListView(ListView):
    model = Card
    template_name = 'card/card_list.html'
    context_object_name = 'cards'


class AdmitCreateView(CreateView):
    model = Card
    template_name = 'card/card_create.html'
    fields = ('school', 'border_color', 'top_background', 'card_school_name', 'school_name_font_size',
              'school_name_color', 'school_address', 'school_address_color', 'admit_card_font_size',
              'admit_card_color', 'admit_card_background', 'title_font_size', 'title_color', 'value_font_size',
              'value_color', 'exam_font_size', 'exam_color', 'subject_font_size', 'subject_color',
              'bottom_signature', 'signature_background', 'signature_color', 'signature_align', 'admit_card_logo')

    def form_valid(self, form):
        card = form.save(commit=False)
        card.save()
        return redirect('card_list')


class AdmitUpdateView(UpdateView):
    model = Card
    template_name = 'card/update_card.html'
    pk_url_kwarg = 'admit_pk'
    fields = ('school', 'border_color', 'top_background', 'card_school_name', 'school_name_font_size',
              'school_name_color', 'school_address', 'school_address_color', 'admit_card_font_size',
              'admit_card_color', 'admit_card_background', 'title_font_size', 'title_color', 'value_font_size',
              'value_color', 'exam_font_size', 'exam_color', 'subject_font_size', 'subject_color',
              'bottom_signature', 'signature_background', 'signature_color', 'signature_align', 'admit_card_logo')

    def form_valid(self, form):
        card = form.save(commit=False)
        card.save()
        return redirect('card_list')


def admit_view(request, admit_pk):
    card = get_object_or_404(Card, pk=admit_pk)
    if request.method == 'POST':
        form = CardForm(request.POST, instance=card)
    else:
        form = CardForm(instance=card)
    return save_card_form(request, form, 'card/includes/partial_card_view.html')


def admit_delete(request, admit_pk):
    card = get_object_or_404(Card, pk=admit_pk)
    data = dict()
    if request.method == 'POST':
        card.delete()
        data['form_is_valid'] = True
        cards = Card.objects.all()
        data['html_card_list'] = render_to_string('card/includes/partial_card_list.html', {
            'cards': cards
        })
    else:
        context = {'card': card}
        data['html_form'] = render_to_string('card/includes/partial_card_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF ADMIT MODULE<===##########################################


# #######################################===>BEGINNING OF MATERIAL MODULE<===#####################################


class MaterialListView(ListView):
    model = Material
    template_name = 'material/material_list.html'
    context_object_name = 'material'


class MaterialCreateView(CreateView):
    model = Material
    template_name = 'material/material_create.html'
    fields = ('school', 'material_title', 'classroom', 'subject', 'material', 'description')

    def form_valid(self, form):
        material = form.save(commit=False)
        material.save()
        return redirect('material_list')


class MaterialUpdateView(UpdateView):
    model = Material
    template_name = 'material/update_material.html'
    pk_url_kwarg = 'material_pk'
    fields = ('school', 'material_title', 'classroom', 'subject', 'material', 'description')

    def form_valid(self, form):
        material = form.save(commit=False)
        material.save()
        return redirect('material_list')


def material_view(request, material_pk):
    material = get_object_or_404(Material, pk=material_pk)
    if request.method == 'POST':
        form = MaterialForm(request.POST, instance=material)
    else:
        form = MaterialForm(instance=material)
    return save_material_form(request, form, 'material/includes/partial_material_view.html')


def save_material_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            materials = Material.objects.all()
            data['html_material_list'] = render_to_string('material/includes/partial_material_list.html', {
                'materials': materials
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def material_delete(request, material_pk):
    material = get_object_or_404(Material, pk=material_pk)
    data = dict()
    if request.method == 'POST':
        material.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        materials = Material.objects.all()
        data['html_material_list'] = render_to_string('material/includes/partial_material_list.html', {
            'materials': materials
        })
    else:
        context = {'material': material}
        data['html_form'] = render_to_string('material/includes/partial_material_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF MATERIAL MODULE<===#####################################

# #######################################===>BEGINNING OF SUBJECT MODULE<===#####################################

class SubjectListView(ListView):
    model = Subject
    template_name = 'subjects/subject_list.html'
    context_object_name = 'subjects'


class SubjectCreateView(CreateView):
    model = Subject
    template_name = 'subjects/subject_create.html'
    fields = ('school', 'subject_name', 'subject_code', 'author', 'type', 'classroom', 'subject_teacher', 'note')

    def form_valid(self, form):
        subject = form.save(commit=False)
        subject.save()
        return redirect('subject_list')


class SubjectUpdateView(UpdateView):
    model = Subject
    template_name = 'subjects/update_subject.html'
    pk_url_kwarg = 'subject_pk'
    fields = ('school', 'subject_name', 'subject_code', 'author', 'type', 'classroom', 'subject_teacher', 'note')

    def form_valid(self, form):
        subject = form.save(commit=False)
        subject.save()
        return redirect('subject_list')


def subject_view(request, subject_pk):
    subject = get_object_or_404(Subject, pk=subject_pk)
    if request.method == 'POST':
        form = SubjectForm(request.POST, instance=subject)
    else:
        form = SubjectForm(instance=subject)
    return save_subject_form(request, form, 'subjects/includes/partial_subject_view.html')


def save_subject_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            subjects = Subject.objects.all()
            data['html_subject_list'] = render_to_string('subjects/includes/partial_subject_list.html', {
                'subjects': subjects
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def subject_delete(request, subject_pk):
    subject = get_object_or_404(Subject, pk=subject_pk)
    data = dict()
    if request.method == 'POST':
        subject.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        subjects = Subject.objects.all()
        data['html_subject_list'] = render_to_string('subjects/includes/partial_subject_list.html', {
            'subjects': subjects
        })
    else:
        context = {'subject': subject}
        data['html_form'] = render_to_string('subjects/includes/partial_subject_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF SUBJECT MODULE<===##########################################

# #######################################===>BEGINNING OF ROUTINE MODULE<===#####################################


def routine_list(request):
    schools = School.objects.all()
    classrooms = Classroom.objects.all()

    # Filters
    classrooms_filter = request.POST.get('classroom')

    schedule_dict = dict()
    if classrooms_filter:
        schedule = Routine.objects.filter(section__classroom=classrooms_filter).distinct().prefetch_related(
            'teacher')

        if schedule:
            for day in DAYS_OF_THE_WEEK:
                schedule_dict[day[1]] = schedule.filter(day=day[0])
    context = {
        'TimeList': TimeList,
        'days': DAYS_OF_THE_WEEK[0:5],
        'schedule': schedule_dict,
        'classrooms': classrooms,
        'schools': schools,
    }
    return render(request, 'routines/routine_list.html', context)


def save_routine_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            routines = Routine.objects.all()
            data['html_routine_list'] = render_to_string('routines/includes/partial_routine_list.html', {
                'routines': routines
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


# def routine_create(request):
#     form = RoutineForm(request.POST or None, request.FILES or None)
#     if form.is_valid():
#         slot = form.save(commit=False)
#         slot.save()
#
#         slot.school = form.cleaned_data.get('school')
#         slot.classroom = form.cleaned_data.get('classroom')
#         slot.section = form.cleaned_data.get('section')
#         slot.subject = form.cleaned_data.get('subject')
#         slot.day = form.cleaned_data.get('day')
#         slot.teacher = form.cleaned_data.get('teacher')
#         slot.start_time = form.cleaned_data.get('start_time')
#         slot.end_time = form.cleaned_data.get('end_time')
#         slot.room_number = form.cleaned_data.get('room_number')
#         slot.save()
#
#         routine_url = reverse('routine_list')
#         return redirect(routine_url)
#
#     context = {
#         'form': form,
#     }
#     return render(request, 'routines/routine_create.html', context)

class RoutineCreateView(CreateView):
    model = Routine
    template_name = 'routines/routine_create.html'
    fields = ('school', 'classroom', 'section', 'subject_name', 'day', 'teacher', 'start_time', 'end_time', 'room_no')

    def get_form(self):
        form = super().get_form()
        form.fields['start_time'].widget = TimePickerInput()
        form.fields['end_time'].widget = TimePickerInput()
        return form

    def form_valid(self, form):
        routine = form.save(commit=False)
        routine.save()
        return redirect('routine_list')


class RoutineUpdateView(UpdateView):
    model = Routine
    template_name = 'routines/update_routine.html'
    pk_url_kwarg = 'routine_pk'
    fields = ('school', 'classroom', 'section', 'subject_name', 'day', 'teacher', 'start_time', 'end_time', 'room_no')

    def get_form(self):
        form = super().get_form()
        form.fields['start_time'].widget = TimePickerInput()
        form.fields['end_time'].widget = TimePickerInput()
        return form

    def form_valid(self, form):
        routine = form.save(commit=False)
        routine.save()
        return redirect('routine_list')


def routine_delete(request, pk):
    routine = get_object_or_404(Routine, pk=pk)
    data = dict()
    if request.method == 'POST':
        routine.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        routines = Routine.objects.all()
        data['html_routine_list'] = render_to_string('routines/includes/partial_routine_list.html', {
            'routines': routines
        })
    else:
        context = {'routine': routine}
        data['html_form'] = render_to_string('routines/includes/partial_routine_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF ROUTINE MODULE<===##########################################


# #######################################===>BEGINNING OF DISPATCH MODULE<===#####################################


class DispatchListView(ListView):
    model = Dispatch
    template_name = 'dispatch/dispatch_list.html'
    context_object_name = 'dispatch'


class DispatchCreateView(CreateView):
    model = Dispatch
    template_name = 'dispatch/dispatch_create.html'
    fields = ('school', 'to_Title', 'reference', 'address', 'from_Title', 'dispatch_date', 'note', 'postal_Attachment')

    def form_valid(self, form):
        dispatch = form.save(commit=False)
        dispatch.save()
        return redirect('dispatch_list')


class DispatchUpdateView(UpdateView):
    model = Dispatch
    template_name = 'dispatch/update_dispatch.html'
    pk_url_kwarg = 'dispatch_pk'
    fields = ('school', 'to_Title', 'reference', 'address', 'from_Title', 'dispatch_date', 'note', 'postal_Attachment')

    def form_valid(self, form):
        dispatch = form.save(commit=False)
        dispatch.save()
        return redirect('dispatch_list')


def dispatch_view(request, dispatch_pk):
    dispatch = get_object_or_404(Dispatch, pk=dispatch_pk)
    if request.method == 'POST':
        form = DispatchForm(request.POST, instance=dispatch)
    else:
        form = DispatchForm(instance=dispatch)
    return save_dispatch_form(request, form, 'dispatch/includes/partial_dispatch_view.html')


def save_dispatch_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            dispatchs = Dispatch.objects.all()
            data['html_dispatch_list'] = render_to_string('dispatch/includes/partial_dispatch_list.html', {
                'dispatchs': dispatchs
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def dispatch_delete(request, dispatch_pk):
    dispatch = get_object_or_404(Dispatch, pk=dispatch_pk)
    data = dict()
    if request.method == 'POST':
        dispatch.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        dispatchs = Dispatch.objects.all()
        data['html_dispatch_list'] = render_to_string('dispatch/includes/partial_dispatch_list.html', {
            'dispatchs': dispatchs
        })
    else:
        context = {'dispatch': dispatch}
        data['html_form'] = render_to_string('dispatch/includes/partial_dispatch_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF DISPATCH MODULE<===#####################################


# #######################################===>BEGINNING OF RECEIVE MODULE<===#####################################


class ReceiveListView(ListView):
    model = Receive
    template_name = 'receive/receive_list.html'
    context_object_name = 'receive'


class ReceiveCreateView(CreateView):
    model = Receive
    template_name = 'receive/receive_create.html'
    fields = ('school', 'to_Title', 'reference', 'address', 'from_Title', 'receive_date', 'note', 'postal_Attachment')

    def form_valid(self, form):
        receive = form.save(commit=False)
        receive.save()
        return redirect('receive_list')


class ReceiveUpdateView(UpdateView):
    model = Receive
    template_name = 'receive/update_receive.html'
    pk_url_kwarg = 'receive_pk'
    fields = ('school', 'to_Title', 'reference', 'address', 'from_Title', 'receive_date', 'note', 'postal_Attachment')

    def form_valid(self, form):
        receive = form.save(commit=False)
        receive.save()
        return redirect('receive_list')


def receive_view(request, receive_pk):
    receive = get_object_or_404(Receive, pk=receive_pk)
    if request.method == 'POST':
        form = ReceiveForm(request.POST, instance=receive)
    else:
        form = ReceiveForm(instance=receive)
    return save_receive_form(request, form, 'receive/includes/partial_receive_view.html')


def save_receive_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            receives = Receive.objects.all()
            data['html_receive_list'] = render_to_string('receive/includes/partial_receive_list.html', {
                'receives': receives
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def receive_delete(request, receive_pk):
    receive = get_object_or_404(Receive, pk=receive_pk)
    data = dict()
    if request.method == 'POST':
        receive.delete()
        data['form_is_valid'] = True
        receives = Receive.objects.all()
        data['html_receive_list'] = render_to_string('receive/includes/partial_receive_list.html', {
            'receives': receives
        })
    else:
        context = {'receive': receive}
        data['html_form'] = render_to_string('receive/includes/partial_receive_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF RECEIVE MODULE<===#####################################


# #######################################===>BEGINNING OF LEAVE MODULE<===##########################################


class LeaveListView(ListView):
    model = Leave
    template_name = 'leaves/leave_list.html'
    context_object_name = 'leaves'


class LeaveCreateView(CreateView):
    model = Leave
    template_name = 'leaves/leave_create.html'
    fields = ('school', 'applicant_type', 'leave_Type', 'total_Type')

    def form_valid(self, form):
        leave = form.save(commit=False)
        leave.save()
        return redirect('leave_list')


class LeaveUpdateView(UpdateView):
    model = Leave
    template_name = 'leaves/update_leave.html'
    pk_url_kwarg = 'leave_pk'
    fields = ('school', 'applicant_type', 'leave_Type', 'total_Type')

    def form_valid(self, form):
        leave = form.save(commit=False)
        leave.save()
        return redirect('leave_list')


def save_leave_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            leaves = Leave.objects.all()
            data['html_leave_list'] = render_to_string('leaves/includes/partial_leave_list.html', {
                'leaves': leaves
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def leave_delete(request, leave_pk):
    leave = get_object_or_404(Leave, pk=leave_pk)
    data = dict()
    if request.method == 'POST':
        leave.delete()
        data['form_is_valid'] = True
        leaves = Leave.objects.all()
        data['html_leave_list'] = render_to_string('leaves/includes/partial_leave_list.html', {
            'leaves': leaves
        })
    else:
        context = {'leave': leave}
        data['html_form'] = render_to_string('leaves/includes/partial_leave_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF LEAVE MODULE<===#################################################


# #######################################===>BEGINNING OF APPLICATION MODULE<===######################################


class ApplicationListView(ListView):
    model = Application
    template_name = 'applications/application_list.html'
    context_object_name = 'applications'


class WaitingApplicationListView(ListView):
    model = Application
    template_name = 'applications/waiting_list.html'
    context_object_name = 'applications'


class ApprovedApplicationListView(ListView):
    model = Application
    template_name = 'applications/approved_list.html'
    context_object_name = 'applications'


class DeclinedApplicationListView(ListView):
    model = Application
    template_name = 'applications/declined_list.html'
    context_object_name = 'applications'


class ApplicationCreateView(CreateView):
    model = Application
    template_name = 'applications/application_create.html'
    fields = ('school', 'applicant_type', 'applicant', 'leave_Type', 'application_Date', 'leave_From', 'leave_To',
              'leave_Reason', 'leave_attachment')

    def form_valid(self, form):
        application = form.save(commit=False)
        application.save()
        return redirect('application_list')


class ApplicationUpdateView(UpdateView):
    model = Application
    template_name = 'applications/update_application.html'
    pk_url_kwarg = 'application_pk'
    fields = ('school', 'applicant_type', 'applicant', 'leave_Type', 'application_Date', 'leave_From', 'leave_To',
              'leave_Reason', 'leave_attachment')

    def form_valid(self, form):
        application = form.save(commit=False)
        application.save()
        return redirect('application_list')


def save_application_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            applications = Application.objects.all()
            data['html_application_list'] = render_to_string('applications/includes/partial_application_list.html', {
                'applications': applications
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def application_delete(request, application_pk):
    application = get_object_or_404(Application, pk=application_pk)
    data = dict()
    if request.method == 'POST':
        application.delete()
        data['form_is_valid'] = True
        applications = Application.objects.all()
        data['html_application_list'] = render_to_string('applications/includes/partial_application_list.html', {
            'applications': applications
        })
    else:
        context = {'application': application}
        data['html_form'] = render_to_string('applications/includes/partial_application_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF APPLICATION MODULE<===#############################################


# #######################################===>BEGINNING OF BULK STUDENT<===###########################################


def save_bulk_student_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            bulk_students = BulkStudent.objects.all()
            data['html_bulk_student_list'] = render_to_string('bulk_students/includes/partial_bulk_student_list.html', {
                'bulk_students': bulk_students
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def bulk_student_list(request):
    bulk_students = BulkStudent.objects.all()
    return render(request, 'bulk_students/bulk_student_list.html', {'bulk_students': bulk_students})


def bulk_student_create(request):
    if request.method == 'POST':
        form = BulkStudentForm(request.POST)
    else:
        form = BulkStudentForm()
    return save_bulk_student_form(request, form, 'bulk_students/includes/partial_bulk_student_create.html')


# #######################################===>END OF BULK STUDENT MODULE<===##########################################

# #######################################===>BEGINNING OF ATTENDANCE MODULE<===#####################################


def attendance_student(request):
    context = {}

    school = request.GET.get('school')
    classroom = request.GET.get('classroom')
    context['form'] = StudentAttendanceForm(school, classroom)
    # Filter
    q = request.GET.get('section')
    if q:
        q = q.replace('.', '')
        students = Student.objects.filter(section=str(q))
        context['students'] = students

    return render(request, 'attendance/student_list.html', context)


def attendance_teacher(request):
    teacher_attendance = TeacherAttendance.objects.all()
    return render(request, 'attendance/teacher_attendance_list.html', {'teacher_attendance': teacher_attendance})


def attendance_employee(request):
    employee_attendance = EmployeeAttendance.objects.all()
    return render(request, 'attendance/employee_attendance_list.html', {'employee_attendance': employee_attendance})


# #######################################===>END OF ATTENDANCE MODULE<===##########################################

# #######################################===>BEGINNING OF ASSIGNMENT MODULE<===#####################################


class AssignmentListView(ListView):
    model = Assignment
    template_name = 'assignments/assignment_list.html'
    context_object_name = 'assignments'


class AssignmentCreateView(CreateView):
    model = Assignment
    template_name = 'assignments/assignment_create.html'
    fields = ('school', 'assignment_title', 'classroom', 'subject', 'deadline', 'assignment', 'note')

    def form_valid(self, form):
        assignment = form.save(commit=False)
        assignment.save()
        return redirect('assignment_list')


class AssignmentUpdateView(UpdateView):
    model = Assignment
    template_name = 'assignments/update_assignment.html'
    pk_url_kwarg = 'assignment_pk'
    fields = ('school', 'assignment_title', 'classroom', 'subject', 'deadline', 'assignment', 'note')

    def form_valid(self, form):
        assignment = form.save(commit=False)
        assignment.save()
        return redirect('assignment_list')


def assignment_view(request, assignment_pk):
    assignment = get_object_or_404(Assignment, pk=assignment_pk)
    if request.method == 'POST':
        form = AssignmentForm(request.POST, instance=assignment)
    else:
        form = AssignmentForm(instance=assignment)
    return save_assignment_form(request, form, 'assignments/includes/partial_assignment_view.html')


def save_assignment_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            assignments = Assignment.objects.all()
            data['html_assignment_list'] = render_to_string('assignments/includes/partial_assignment_list.html', {
                'assignments': assignments
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def assignment_delete(request, assignment_pk):
    assignment = get_object_or_404(Assignment, pk=assignment_pk)
    data = dict()
    if request.method == 'POST':
        assignment.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        assignments = Assignment.objects.all()
        data['html_assignment_list'] = render_to_string('assignments/includes/partial_assignment_list.html', {
            'assignments': assignments
        })
    else:
        context = {'assignment': assignment}
        data['html_form'] = render_to_string('assignments/includes/partial_assignment_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF ASSIGNMENT MODULE<===##########################################

# #######################################===>BEGINNING OF MARK MODULE<===##########################################


def manage_mark(request):
    form = MarkForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        mark = form.save(commit=False)
        mark.save()

        mark.school = form.cleaned_data.get('school')
        mark.classroom = form.cleaned_data.get('classroom')
        mark.exam = form.cleaned_data.get('exam')
        mark.section = form.cleaned_data.get('section')
        mark.subject = form.cleaned_data.get('subject')
        mark.save()

        mark_url = reverse('manage_mark')
        return redirect(mark_url)
    context = {
        'form': form,
    }
    return render(request, 'marks/manage_marks.html', context)


# #######################################===>END OF MARK MODULE<===#################################################

# #######################################===>BEGINNING OF EXAM GRADE MODULE<===#####################################


class ExamGradeListView(ListView):
    model = ExamGrade
    template_name = 'exam_grades/exam_grade_list.html'
    context_object_name = 'exam_grades'


class ExamGradeCreateView(CreateView):
    model = ExamGrade
    template_name = 'exam_grades/exam_grade_create.html'
    fields = ('school', 'exam_grade', 'grade_point', 'mark_from', 'mark_to', 'note')

    def form_valid(self, form):
        exam_grade = form.save(commit=False)
        exam_grade.save()
        return redirect('exam_grade_list')


class ExamGradeUpdateView(UpdateView):
    model = ExamGrade
    template_name = 'exam_grades/update_exam_grade.html'
    pk_url_kwarg = 'exam_grade_pk'
    fields = ('school', 'exam_grade', 'grade_point', 'mark_from', 'mark_to', 'note')

    def form_valid(self, form):
        exam_grade = form.save(commit=False)
        exam_grade.save()
        return redirect('exam_grade_list')


def save_exam_grade_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            exam_grades = ExamGrade.objects.all()
            data['html_exam_grade_list'] = render_to_string('exam_grades/includes/partial_exam_grade_list.html', {
                'exam_grades': exam_grades
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def exam_grade_delete(request, exam_grade_pk):
    exam_grade = get_object_or_404(ExamGrade, pk=exam_grade_pk)
    data = dict()
    if request.method == 'POST':
        exam_grade.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        exam_grades = ExamGrade.objects.all()
        data['html_exam_grade_list'] = render_to_string('exam_grades/includes/partial_exam_grade_list.html', {
            'exam_grades': exam_grades
        })
    else:
        context = {'exam_grade': exam_grade}
        data['html_form'] = render_to_string('exam_grades/includes/partial_exam_grade_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF EXAM GRADE MODULE<===##########################################

# #######################################===>BEGINNING OF EXAM MODULE<===##########################################


class ExamListView(ListView):
    model = Exam
    template_name = 'exams/exam_list.html'
    context_object_name = 'exams'


class ExamCreateView(CreateView):
    model = Exam
    template_name = 'exams/exam_create.html'
    fields = ('school', 'exam_title', 'start_date', 'note')

    def get_form(self):
        form = super().get_form()
        form.fields['start_date'].widget = DatePickerInput()
        return form

    def form_valid(self, form):
        exam = form.save(commit=False)
        exam.save()
        return redirect('exam_list')


class ExamUpdateView(UpdateView):
    model = Exam
    template_name = 'exams/update_exam.html'
    pk_url_kwarg = 'exam_pk'
    fields = ('school', 'exam_title', 'start_date', 'note')

    def get_form(self):
        form = super().get_form()
        form.fields['start_date'].widget = DatePickerInput()
        return form

    def form_valid(self, form):
        exam = form.save(commit=False)
        exam.save()
        return redirect('exam_list')


def save_exam_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            exams = Exam.objects.all()
            data['html_exam_list'] = render_to_string('exams/includes/partial_exam_list.html', {
                'exams': exams
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def exam_delete(request, exam_pk):
    exam = get_object_or_404(Exam, pk=exam_pk)
    data = dict()
    if request.method == 'POST':
        exam.delete()
        data['form_is_valid'] = True
        exams = Exam.objects.all()
        data['html_exam_list'] = render_to_string('exams/includes/partial_exam_list.html', {
            'exams': exams
        })
    else:
        context = {'exam': exam}
        data['html_form'] = render_to_string('exams/includes/partial_exam_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF EXAM MODULE<===#################################################

# #######################################===>BEGINNING OF EXAM SCHEDULE MODULE<===###################################


class ExamScheduleListView(ListView):
    model = ExamSchedule
    template_name = 'exam_schedules/exam_schedule_list.html'
    context_object_name = 'exam_schedules'


class ExamScheduleCreateView(CreateView):
    model = ExamSchedule
    template_name = 'exam_schedules/exam_schedule_create.html'
    fields = ('school', 'exam', 'classroom', 'subject', 'exam_date', 'start_time', 'end_time', 'room_no', 'note')

    def get_form(self):
        form = super().get_form()
        form.fields['exam_date'].widget = DatePickerInput()
        return form

    def form_valid(self, form):
        exam = form.save(commit=False)
        exam.save()
        return redirect('exam_schedule_list')


class ExamScheduleUpdateView(UpdateView):
    model = ExamSchedule
    template_name = 'exam_schedules/update_exam_schedule.html'
    pk_url_kwarg = 'exam_schedule_pk'
    fields = ('school', 'exam', 'classroom', 'subject', 'exam_date', 'start_time', 'end_time', 'room_no', 'note')

    def get_form(self):
        form = super().get_form()
        form.fields['exam_date'].widget = DatePickerInput()
        return form

    def form_valid(self, form):
        exam_schedule = form.save(commit=False)
        exam_schedule.save()
        return redirect('exam_schedule_list')


def save_exam_schedule_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            exam_schedules = ExamSchedule.objects.all()
            data['html_exam_schedule_list'] = render_to_string(
                'exam_schedules/includes/partial_exam_schedule_list.html', {
                    'exam_schedules': exam_schedules
                })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def exam_schedule_delete(request, exam_schedule_pk):
    exam_schedule = get_object_or_404(ExamSchedule, pk=exam_schedule_pk)
    data = dict()
    if request.method == 'POST':
        exam_schedule.delete()
        data['form_is_valid'] = True
        exam_schedules = ExamSchedule.objects.all()
        data['html_exam_schedule_list'] = render_to_string('exam_schedules/includes/partial_exam_schedule_list.html', {
            'exam_schedules': exam_schedules
        })
    else:
        context = {'exam_schedule': exam_schedule}
        data['html_form'] = render_to_string('exam_schedules/includes/partial_exam_schedule_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF EXAM SCHEDULE MODULE<===##########################################

# #######################################===>BEGINNING OF EXAM SUGGESTION MODULE<===##################################


class ExamSuggestionListView(ListView):
    model = ExamSuggestion
    template_name = 'exam_suggestions/exam_suggestion_list.html'
    context_object_name = 'exam_suggestions'


class ExamSuggestionCreateView(CreateView):
    model = ExamSuggestion
    template_name = 'exam_suggestions/exam_suggestion_create.html'
    fields = ('school', 'suggestion_title', 'exam', 'classroom', 'subject', 'suggestion', 'note')

    def form_valid(self, form):
        exam_suggestion = form.save(commit=False)
        exam_suggestion.save()
        return redirect('exam_suggestion_list')


class ExamSuggestionUpdateView(UpdateView):
    model = ExamSuggestion
    template_name = 'exam_suggestions/update_exam_suggestion.html'
    pk_url_kwarg = 'exam_suggestion_pk'
    fields = ('school', 'suggestion_title', 'exam', 'classroom', 'subject', 'suggestion', 'note')

    def form_valid(self, form):
        exam_suggestion = form.save(commit=False)
        exam_suggestion.save()
        return redirect('exam_suggestion_list')


def save_exam_suggestion_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            exam_suggestions = ExamSuggestion.objects.all()
            data['html_exam_suggestion_list'] = render_to_string(
                'exam_suggestions/includes/partial_exam_suggestion_list.html', {
                    'exam_suggestions': exam_suggestions
                })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def exam_suggestion_delete(request, exam_suggestion_pk):
    exam_suggestion = get_object_or_404(ExamSuggestion, pk=exam_suggestion_pk)
    data = dict()
    if request.method == 'POST':
        exam_suggestion.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        exam_suggestions = ExamSuggestion.objects.all()
        data['html_exam_suggestion_list'] = render_to_string(
            'exam_suggestions/includes/partial_exam_suggestion_list.html', {
                'exam_suggestions': exam_suggestions
            })
    else:
        context = {'exam_suggestion': exam_suggestion}
        data['html_form'] = render_to_string('exam_suggestions/includes/partial_exam_suggestion_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF EXAM SUGGESTION MODULE<===#########################################

# #######################################===>BEGINNING OF CERTIFICATE MODULE<===#######################################


class CertificateListView(ListView):
    model = CertificateType
    template_name = 'certificates/certificate_list.html'
    context_object_name = 'certificates'


class CertificateCreateView(CreateView):
    model = CertificateType
    template_name = 'certificates/certificate_create.html'
    fields = ('school', 'certificate_name', 'school_name', 'certificate_text', 'footer_left_text', 'footer_middle_text',
              'footer_right_text', 'background')

    def form_valid(self, form):
        certificate = form.save(commit=False)
        certificate.save()
        return redirect('certificate_list')


class CertificateUpdateView(UpdateView):
    model = CertificateType
    template_name = 'certificates/update_certificate.html'
    pk_url_kwarg = 'certificate_pk'
    fields = ('school', 'certificate_name', 'school_name', 'certificate_text', 'footer_left_text', 'footer_middle_text',
              'footer_right_text', 'background')

    def form_valid(self, form):
        certificate = form.save(commit=False)
        certificate.save()
        return redirect('certificate_list')


def save_certificate_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            certificates = CertificateType.objects.all()
            data['html_certificate_list'] = render_to_string('certificates/includes/partial_certificate_list.html', {
                'certificates': certificates
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def certificate_delete(request, certificate_pk):
    certificate = get_object_or_404(CertificateType, pk=certificate_pk)
    data = dict()
    if request.method == 'POST':
        certificate.delete()
        data['form_is_valid'] = True
        certificates = CertificateType.objects.all()
        data['html_certificate_list'] = render_to_string('certificates/includes/partial_certificate_list.html', {
            'certificates': certificates
        })
    else:
        context = {'certificate': certificate}
        data['html_form'] = render_to_string('certificates/includes/partial_certificate_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF CERTIFICATE MODULE<===#####################################

# #######################################===>BEGINNING OF BOOK MODULE<===#####################################


class BookListView(ListView):
    model = Book
    template_name = 'books/book_list.html'
    context_object_name = 'books'


class BookCreateView(CreateView):
    model = Book
    template_name = 'books/book_create.html'
    fields = ('school', 'book_title', 'book_ID', 'ISBN_no', 'edition', 'author', 'language', 'price', 'quantity',
              'almira_no', 'book_cover')

    def form_valid(self, form):
        book = form.save(commit=False)
        book.save()
        return redirect('book_list')


class BookUpdateView(UpdateView):
    model = Book
    template_name = 'books/update_book.html'
    pk_url_kwarg = 'book_pk'
    fields = ('school', 'book_title', 'book_ID', 'ISBN_no', 'edition', 'author', 'language', 'price', 'quantity',
              'almira_no', 'book_cover')

    def form_valid(self, form):
        book = form.save(commit=False)
        book.save()
        return redirect('book_list')


def save_book_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            books = Book.objects.all()
            data['html_book_list'] = render_to_string('books/includes/partial_book_list.html', {
                'books': books
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def book_view(request, book_pk):
    book = get_object_or_404(Book, pk=book_pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
    else:
        form = BookForm(instance=book)
    return save_book_form(request, form, 'books/includes/partial_book_view.html')


def book_delete(request, book_pk):
    book = get_object_or_404(Book, pk=book_pk)
    data = dict()
    if request.method == 'POST':
        book.delete()
        data['form_is_valid'] = True
        books = Book.objects.all()
        data['html_book_list'] = render_to_string('books/includes/partial_book_list.html', {
            'books': books
        })
    else:
        context = {'book': book}
        data['html_form'] = render_to_string('books/includes/partial_book_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF BOOK MODULE<===##################################################


# #######################################===>BEGINNING OF PURPOSE MODULE<===#####################################


class PurposeListView(ListView):
    model = Purpose
    template_name = 'purposes/purpose_list.html'
    context_object_name = 'purposes'


class PurposeCreateView(CreateView):
    model = Purpose
    template_name = 'purposes/purpose_create.html'
    fields = ('school', 'visitor_purpose')

    def form_valid(self, form):
        purpose = form.save(commit=False)
        purpose.save()
        return redirect('purpose_list')


class PurposeUpdateView(UpdateView):
    model = Purpose
    template_name = 'purposes/update_purpose.html'
    pk_url_kwarg = 'purpose_pk'
    fields = ('school', 'visitor_purpose')

    def form_valid(self, form):
        purpose = form.save(commit=False)
        purpose.save()
        return redirect('purpose_list')


def save_purpose_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            purposes = Purpose.objects.all()
            data['html_purpose_list'] = render_to_string('purposes/includes/partial_purpose_list.html', {
                'purposes': purposes
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def purpose_delete(request, purpose_pk):
    purpose = get_object_or_404(Purpose, pk=purpose_pk)
    data = dict()
    if request.method == 'POST':
        purpose.delete()
        data['form_is_valid'] = True
        purposes = Purpose.objects.all()
        data['html_purpose_list'] = render_to_string('purposes/includes/partial_purpose_list.html', {
            'purposes': purposes
        })
    else:
        context = {'purpose': purpose}
        data['html_form'] = render_to_string('purposes/includes/partial_purpose_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF PURPOSE MODULE<===##################################################


# #######################################===>BEGINNING OF E-PURPOSE MODULE<===#####################################


class EBookListView(ListView):
    model = EBook
    template_name = 'ebooks/ebook_list.html'
    context_object_name = 'ebooks'


class EBookCreateView(CreateView):
    model = EBook
    template_name = 'ebooks/ebook_create.html'
    fields = ('school', 'classroom', 'subject', 'EBook_title', 'edition', 'author', 'language', 'cover_image', 'e_book')

    def form_valid(self, form):
        ebook = form.save(commit=False)
        ebook.save()
        return redirect('ebook_list')


class EBookUpdateView(UpdateView):
    model = EBook
    template_name = 'ebooks/update_ebook.html'
    pk_url_kwarg = 'ebook_pk'
    fields = ('school', 'classroom', 'subject', 'EBook_title', 'edition', 'author', 'language', 'cover_image', 'e_book')

    def form_valid(self, form):
        eBook = form.save(commit=False)
        eBook.save()
        return redirect('ebook_list')


def save_ebook_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            eBooks = EBook.objects.all()
            data['html_ebook_list'] = render_to_string('ebooks/includes/partial_ebook_list.html', {
                'eBooks': eBooks
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def ebook_view(request, ebook_pk):
    eBook = get_object_or_404(EBook, pk=ebook_pk)
    if request.method == 'POST':
        form = EBookForm(request.POST, instance=eBook)
    else:
        form = EBookForm(instance=eBook)
    return save_ebook_form(request, form, 'eBooks/includes/partial_eBook_view.html')


def ebook_delete(request, ebook_pk):
    ebook = get_object_or_404(EBook, pk=ebook_pk)
    data = dict()
    if request.method == 'POST':
        ebook.delete()
        data['form_is_valid'] = True
        ebooks = EBook.objects.all()
        data['html_ebook_list'] = render_to_string('ebooks/includes/partial_ebook_list.html', {
            'ebooks': ebooks
        })
    else:
        context = {'ebook': ebook}
        data['html_form'] = render_to_string('ebooks/includes/partial_ebook_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF E-BOOK MODULE<===##################################################


# #######################################===>BEGINNING OF LIBRARY MEMBER MODULE<===###################################


class LibraryMemberListView(ListView):
    model = LibraryMember
    template_name = 'library_members/library_member_list.html'
    context_object_name = 'library_members'


class LibraryMemberCreateView(CreateView):
    model = LibraryMember
    template_name = 'library_members/library_member_create.html'
    fields = ('school', 'photo', 'library_ID', 'name', 'classroom', 'section', 'roll_no')

    def form_valid(self, form):
        library_member = form.save(commit=False)
        library_member.save()
        return redirect('library_member_list')


class LibraryMemberUpdateView(UpdateView):
    model = LibraryMember
    template_name = 'library_members/update_library_member.html'
    pk_url_kwarg = 'library_member_pk'
    fields = ('school', 'photo', 'library_ID', 'name', 'classroom', 'section', 'roll_no')

    def form_valid(self, form):
        library_member = form.save(commit=False)
        library_member.save()
        return redirect('library_member_list')


def save_library_member_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            library_members = LibraryMember.objects.all()
            data['html_library_member_list'] = render_to_string(
                'library_members/includes/partial_library_member_list.html', {
                    'library_members': library_members
                })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def library_member_delete(request, library_member_pk):
    library_member = get_object_or_404(LibraryMember, pk=library_member_pk)
    data = dict()
    if request.method == 'POST':
        library_member.delete()
        data['form_is_valid'] = True
        library_members = LibraryMember.objects.all()
        data['html_library_member_list'] = render_to_string('library_members/includes/partial_library_member_list.html',
                                                            {
                                                                'library_members': library_members
                                                            })
    else:
        context = {'library_member': library_member}
        data['html_form'] = render_to_string('library_members/includes/partial_library_member_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF LIBRARY MEMBER MODULE<===#######################################

# #######################################===>BEGINNING OF ISSUE MODULE<===##########################################


class IssueListView(ListView):
    model = Issue
    template_name = 'issues/issue_list.html'
    context_object_name = 'issues'


class IssueCreateView(CreateView):
    model = Issue
    template_name = 'issues/issue_create.html'
    fields = (
        'school', 'select_book', 'library_member', 'ISBN_no', 'edition', 'author', 'language', 'price', 'quantity',
        'almira_no', 'book_cover', 'return_date')

    def get_form(self):
        form = super().get_form()
        form.fields['return_date'].widget = DatePickerInput()
        return form

    def form_valid(self, form):
        issue = form.save(commit=False)
        issue.save()
        return redirect('issue_list')


class IssueUpdateView(UpdateView):
    model = Issue
    template_name = 'issues/update_issue.html'
    pk_url_kwarg = 'issue_pk'
    fields = (
        'school', 'select_book', 'library_member', 'ISBN_no', 'edition', 'author', 'language', 'price', 'quantity',
        'almira_no', 'book_cover', 'return_date')

    def get_form(self):
        form = super().get_form()
        form.fields['return_date'].widget = DatePickerInput()
        return form

    def form_valid(self, form):
        issue = form.save(commit=False)
        issue.save()
        return redirect('issue_list')


def save_issue_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            issues = Issue.objects.all()
            data['html_issue_list'] = render_to_string('issues/includes/partial_issue_list.html', {
                'issues': issues
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def issue_delete(request, issue_pk):
    issue = get_object_or_404(Issue, pk=issue_pk)
    data = dict()
    if request.method == 'POST':
        issue.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        issues = Issue.objects.all()
        data['html_issue_list'] = render_to_string('issues/includes/partial_issue_list.html', {
            'issues': issues
        })
    else:
        context = {'issue': issue}
        data['html_form'] = render_to_string('issues/includes/partial_issue_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF ISSUE MODULE<===#################################################

# #######################################===>BEGINNING OF VEHICLE MODULE<===##########################################

class VehicleListView(ListView):
    model = Vehicle
    template_name = 'vehicles/vehicle_list.html'
    context_object_name = 'vehicles'


class VehicleCreateView(CreateView):
    model = Vehicle
    template_name = 'vehicles/vehicle_create.html'
    fields = ('school', 'vehicle_number', 'vehicle_model', 'driver', 'vehicle_licence', 'vehicle_contact', 'note')

    def form_valid(self, form):
        vehicle = form.save(commit=False)
        vehicle.save()
        return redirect('vehicle_list')


class VehicleUpdateView(UpdateView):
    model = Vehicle
    template_name = 'vehicles/update_vehicle.html'
    pk_url_kwarg = 'vehicle_pk'
    fields = ('school', 'vehicle_number', 'vehicle_model', 'driver', 'vehicle_licence', 'vehicle_contact', 'note')

    def form_valid(self, form):
        vehicle = form.save(commit=False)
        vehicle.save()
        return redirect('vehicle_list')


def save_vehicle_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            vehicles = Vehicle.objects.all()
            data['html_vehicle_list'] = render_to_string('vehicles/includes/partial_vehicle_list.html', {
                'vehicles': vehicles
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def vehicle_view(request, vehicle_pk):
    vehicle = get_object_or_404(Vehicle, pk=vehicle_pk)
    if request.method == 'POST':
        form = VehicleForm(request.POST, instance=vehicle)
    else:
        form = VehicleForm(instance=vehicle)
    return save_vehicle_form(request, form, 'vehicles/includes/partial_vehicle_view.html')


def vehicle_delete(request, vehicle_pk):
    vehicle = get_object_or_404(Vehicle, pk=vehicle_pk)
    data = dict()
    if request.method == 'POST':
        vehicle.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        vehicles = Vehicle.objects.all()
        data['html_vehicle_list'] = render_to_string('vehicles/includes/partial_vehicle_list.html', {
            'vehicles': vehicles
        })
    else:
        context = {'vehicle': vehicle}
        data['html_form'] = render_to_string('vehicles/includes/partial_vehicle_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF VEHICLE MODULE<===#################################################

# #######################################===>BEGINNING OF ROUTE MODULE<===##########################################


class RouteListView(ListView):
    model = Route
    template_name = 'routes/route_list.html'
    context_object_name = 'routes'


class RouteCreateView(CreateView):
    model = Route
    template_name = 'routes/route_create.html'
    fields = ('school', 'route_title', 'route_start', 'route_end', 'vehicle_for_route', 'stop_name', 'stop_km',
              'stop_fare', 'note')

    def form_valid(self, form):
        route = form.save(commit=False)
        route.save()
        return redirect('route_list')


class RouteUpdateView(UpdateView):
    model = Route
    template_name = 'routes/update_route.html'
    pk_url_kwarg = 'route_pk'
    fields = ('school', 'route_title', 'route_start', 'route_end', 'vehicle_for_route', 'stop_name', 'stop_km',
              'stop_fare', 'note')

    def form_valid(self, form):
        route = form.save(commit=False)
        route.save()
        return redirect('route_list')


def save_route_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            routes = Route.objects.all()
            data['html_route_list'] = render_to_string('routes/includes/partial_route_list.html', {
                'routes': routes
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def route_view(request, route_pk):
    route = get_object_or_404(Route, pk=route_pk)
    if request.method == 'POST':
        form = RouteForm(request.POST, instance=route)
    else:
        form = RouteForm(instance=route)
    return save_vehicle_form(request, form, 'routes/includes/partial_route_view.html')


def route_delete(request, route_pk):
    route = get_object_or_404(Route, pk=route_pk)
    data = dict()
    if request.method == 'POST':
        route.delete()
        data['form_is_valid'] = True
        routes = Route.objects.all()
        data['html_route_list'] = render_to_string('routes/includes/partial_route_list.html', {
            'routes': routes
        })
    else:
        context = {'route': route}
        data['html_form'] = render_to_string('routes/includes/partial_route_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF ROUTE MODULE<===#################################################

# ###################################===>BEGINNING OF TRANSPORT MEMBER MODULE<===#####################################


class TransportMemberListView(ListView):
    model = TransportMember
    template_name = 'transport_members/transport_member_list.html'
    context_object_name = 'transport_members'


class TransportMemberCreateView(CreateView):
    model = TransportMember
    template_name = 'transport_members/transport_member_create.html'
    fields = ('school', 'photo', 'name', 'classroom', 'section', 'roll_no', 'transport_route_name', 'stop_Name',
              'stop_KM', 'stop_Fare')

    def form_valid(self, form):
        transport_member = form.save(commit=False)
        transport_member.save()
        return redirect('transport_member_list')


class TransportMemberUpdateView(UpdateView):
    model = TransportMember
    template_name = 'transport_members/update_transport_member.html'
    pk_url_kwarg = 'transport_member_pk'
    fields = ('school', 'photo', 'name', 'classroom', 'section', 'roll_no', 'transport_route_name', 'stop_Name',
              'stop_KM', 'stop_Fare')

    def form_valid(self, form):
        transport_member = form.save(commit=False)
        transport_member.save()
        return redirect('transport_member_list')


def save_transport_member_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            transport_members = TransportMember.objects.all()
            data['html_transport_member_list'] = render_to_string(
                'transport_members/includes/partial_transport_member_list.html', {
                    'transport_members': transport_members
                })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def transport_member_delete(request, pk):
    transport_member = get_object_or_404(TransportMember, pk=pk)
    data = dict()
    if request.method == 'POST':
        transport_member.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        transport_members = TransportMember.objects.all()
        data['html_transport_member_list'] = render_to_string(
            'transport_members/includes/partial_transport_member_list.html', {
                'transport_members': transport_members
            })
    else:
        context = {'transport_member': transport_member}
        data['html_form'] = render_to_string('transport_members/includes/partial_transport_member_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF TRANSPORT MEMBER MODULE<===######################################

# ###################################===>BEGINNING OF HOSTEL MODULE<===##############################################


class HostelListView(ListView):
    model = Hostel
    template_name = 'hostels/hostel_list.html'
    context_object_name = 'hostels'


class HostelCreateView(CreateView):
    model = Hostel
    template_name = 'hostels/hostel_create.html'
    fields = ('school', 'hostel_name', 'hostel_type', 'address', 'note')

    def form_valid(self, form):
        hostel = form.save(commit=False)
        hostel.save()
        return redirect('hostel_list')


class HostelUpdateView(UpdateView):
    model = Hostel
    template_name = 'hostels/update_hostel.html'
    pk_url_kwarg = 'hostel_pk'
    fields = ('school', 'hostel_name', 'hostel_type', 'address', 'note')

    def form_valid(self, form):
        hostel = form.save(commit=False)
        hostel.save()
        return redirect('hostel_list')


def save_hostel_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            hostels = Hostel.objects.all()
            data['html_hostel_list'] = render_to_string('hostels/includes/partial_hostel_list.html', {
                'hostels': hostels
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def hostel_view(request, hostel_pk):
    hostel = get_object_or_404(Hostel, pk=hostel_pk)
    if request.method == 'POST':
        form = HostelForm(request.POST, instance=hostel)
    else:
        form = HostelForm(instance=hostel)
    return save_vehicle_form(request, form, 'hostels/includes/partial_hostel_view.html')


def hostel_delete(request, hostel_pk):
    hostel = get_object_or_404(Hostel, pk=hostel_pk)
    data = dict()
    if request.method == 'POST':
        hostel.delete()
        data['form_is_valid'] = True
        hostels = Hostel.objects.all()
        data['html_hostel_list'] = render_to_string('hostels/includes/partial_hostel_list.html', {
            'hostels': hostels
        })
    else:
        context = {'hostel': hostel}
        data['html_form'] = render_to_string('hostels/includes/partial_hostel_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF HOSTEL MODULE<===#############################################

# ###################################===>BEGINNING OF ROOM MODULE<===##############################################

class RoomListView(ListView):
    model = Room
    template_name = 'rooms/room_list.html'
    context_object_name = 'rooms'


class RoomCreateView(CreateView):
    model = Room
    template_name = 'rooms/room_create.html'
    fields = ('school', 'room_no', 'room_type', 'seat_total', 'hostel', 'cost_per_seat', 'note')

    def form_valid(self, form):
        room = form.save(commit=False)
        room.save()
        return redirect('room_list')


class RoomUpdateView(UpdateView):
    model = Room
    template_name = 'rooms/update_room.html'
    pk_url_kwarg = 'room_pk'
    fields = ('school', 'room_no', 'room_type', 'seat_total', 'hostel', 'cost_per_seat', 'note')

    def form_valid(self, form):
        room = form.save(commit=False)
        room.save()
        return redirect('room_list')


def save_room_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            rooms = Room.objects.all()
            data['html_room_list'] = render_to_string('rooms/includes/partial_room_list.html', {
                'rooms': rooms
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def room_view(request, room_pk):
    room = get_object_or_404(Room, pk=room_pk)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
    else:
        form = RoomForm(instance=room)
    return save_vehicle_form(request, form, 'rooms/includes/partial_room_view.html')


def room_delete(request, room_pk):
    room = get_object_or_404(Room, pk=room_pk)
    data = dict()
    if request.method == 'POST':
        room.delete()
        data['form_is_valid'] = True
        rooms = Room.objects.all()
        data['html_room_list'] = render_to_string('rooms/includes/partial_room_list.html', {
            'rooms': rooms
        })
    else:
        context = {'room': room}
        data['html_form'] = render_to_string('rooms/includes/partial_room_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF ROOM MODULE<===################################################

# ###################################===>BEGINNING OF HOSTEL MEMBER MODULE<===#####################################


class HostelMemberListView(ListView):
    model = HostelMember
    template_name = 'hostel_members/hostel_member_list.html'
    context_object_name = 'hostel_members'


class HostelMemberCreateView(CreateView):
    model = HostelMember
    template_name = 'hostel_members/hostel_member_create.html'
    fields = ('school', 'photo', 'name', 'classroom', 'section', 'roll_no', 'hostel_name', 'room_no',
              'room_type')

    def form_valid(self, form):
        hostel_member = form.save(commit=False)
        hostel_member.save()
        return redirect('hostel_member_list')


class HostelMemberUpdateView(UpdateView):
    model = HostelMember
    template_name = 'hostel_members/update_hostel_member.html'
    pk_url_kwarg = 'member_pk'
    fields = ('school', 'photo', 'name', 'classroom', 'section', 'roll_no', 'hostel_name', 'room_no', 'room_type')

    def form_valid(self, form):
        hostel_member = form.save(commit=False)
        hostel_member.save()
        return redirect('hostel_member_list')


def save_hostel_member_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            hostel_members = HostelMember.objects.all()
            data['html_hostel_member_list'] = render_to_string(
                'hostel_members/includes/partial_hostel_member_list.html', {
                    'hostel_members': hostel_members
                })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def hostel_member_delete(request, member_pk):
    hostel_member = get_object_or_404(HostelMember, pk=member_pk)
    data = dict()
    if request.method == 'POST':
        hostel_member.delete()
        data['form_is_valid'] = True
        hostel_members = HostelMember.objects.all()
        data['html_hostel_member_list'] = render_to_string(
            'hostel_members/includes/partial_hostel_member_list.html', {
                'hostel_members': hostel_members
            })
    else:
        context = {'hostel_member': hostel_member}
        data['html_form'] = render_to_string('hostel_members/includes/partial_hostel_member_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF HOSTEL MEMBER MODULE<===##########################################

# ###################################===>BEGINNING OF EMAIL MODULE<===###############################################


class EmailListView(ListView):
    model = Email
    template_name = 'emails/email_list.html'
    context_object_name = 'emails'


class EmailCreateView(CreateView):
    model = Email
    template_name = 'emails/email_create.html'
    fields = ('school_name', 'receiver_type', 'receiver', 'subject', 'email_body', 'attachment')

    def form_valid(self, form):
        email = form.save(commit=False)
        email.save()
        return redirect('email_list')


def save_email_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            emails = Email.objects.all()
            data['html_email_list'] = render_to_string('emails/includes/partial_email_list.html', {
                'emails': emails
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def email_view(request, email_pk):
    email = get_object_or_404(Email, pk=email_pk)
    if request.method == 'POST':
        form = EmailForm(request.POST, instance=email)
    else:
        form = EmailForm(instance=email)
    return save_vehicle_form(request, form, 'emails/includes/partial_email_view.html')


def email_delete(request, email_pk):
    email = get_object_or_404(Email, pk=email_pk)
    data = dict()
    if request.method == 'POST':
        email.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        emails = Email.objects.all()
        data['html_email_list'] = render_to_string('emails/includes/partial_email_list.html', {
            'emails': emails
        })
    else:
        context = {'email': email}
        data['html_form'] = render_to_string('emails/includes/partial_email_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF EMAIL MODULE<===##########################################

# ###################################===>BEGINNING OF SMS MODULE<===###############################################


class SMSListView(ListView):
    model = SMS
    template_name = 'sms/sms_list.html'
    context_object_name = 'sms'


class SMSCreateView(CreateView):
    model = SMS
    template_name = 'sms/sms_create.html'
    fields = ('school', 'receiver_type', 'receiver', 'SMS', 'gateway')

    def form_valid(self, form):
        sms = form.save(commit=False)
        sms.save()
        return redirect('sms_list')


def save_sms_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            smss = SMS.objects.all()
            data['html_sms_list'] = render_to_string('sms/includes/partial_sms_list.html', {
                'sms': smss
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def sms_view(request, SMS_pk):
    sms = get_object_or_404(SMS, pk=SMS_pk)
    if request.method == 'POST':
        form = SMSForm(request.POST, instance=sms)
    else:
        form = SMSForm(instance=sms)
    return save_vehicle_form(request, form, 'sms/includes/partial_sms_view.html')


def sms_delete(request, SMS_pk):
    sms = get_object_or_404(SMS, pk=SMS_pk)
    data = dict()
    if request.method == 'POST':
        sms.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        smss = SMS.objects.all()
        data['html_sms_list'] = render_to_string('sms/includes/partial_sms_list.html', {
            'sms': smss
        })
    else:
        context = {'sms': sms}
        data['html_form'] = render_to_string('sms/includes/partial_sms_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF SMS MODULE<===##################################################

# ###################################===>BEGINNING OF NOTICE MODULE<===###############################################


class NoticeListView(ListView):
    model = Notice
    template_name = 'notices/notice_list.html'
    context_object_name = 'notices'


class NoticeCreateView(CreateView):
    model = Notice
    template_name = 'notices/notice_create.html'
    fields = ('school', 'notice_title', 'date', 'notice_for', 'notice', 'Is_View_on_Web')

    def form_valid(self, form):
        notice = form.save(commit=False)
        notice.save()
        return redirect('notice_list')


class NoticeUpdateView(UpdateView):
    model = Notice
    template_name = 'notices/update_notice.html'
    pk_url_kwarg = 'notice_pk'
    fields = ('school', 'notice_title', 'date', 'notice_for', 'notice', 'Is_View_on_Web')

    def get_form(self):
        form = super().get_form()
        form.fields['date'].widget = DatePickerInput()
        return form

    def form_valid(self, form):
        notice = form.save(commit=False)
        notice.save()
        return redirect('notice_list')


def save_notice_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            notices = Notice.objects.all()
            data['html_notice_list'] = render_to_string('notices/includes/partial_notice_list.html', {
                'notices': notices
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def notice_view(request, notice_pk):
    notice = get_object_or_404(Notice, pk=notice_pk)
    if request.method == 'POST':
        form = NoticeForm(request.POST, instance=notice)
    else:
        form = NoticeForm(instance=notice)
    return save_vehicle_form(request, form, 'notices/includes/partial_notice_view.html')


def notice_delete(request, notice_pk):
    notice = get_object_or_404(Notice, pk=notice_pk)
    data = dict()
    if request.method == 'POST':
        notice.delete()
        data['form_is_valid'] = True
        notices = Notice.objects.all()
        data['html_notice_list'] = render_to_string('notices/includes/partial_notice_list.html', {
            'notices': notices
        })
    else:
        context = {'notice': notice}
        data['html_form'] = render_to_string('notices/includes/partial_notice_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF NOTICE MODULE<===##################################################

# ###################################===>BEGINNING OF NEWS MODULE<===###############################################


class NewsListView(ListView):
    model = News
    template_name = 'news/news_list.html'
    context_object_name = 'news'


class NewsCreateView(CreateView):
    model = News
    template_name = 'news/news_create.html'
    fields = ('school', 'news_title', 'date', 'image', 'news', 'Is_View_on_Web')

    def get_form(self):
        form = super().get_form()
        form.fields['date'].widget = DatePickerInput()
        return form

    def form_valid(self, form):
        news = form.save(commit=False)
        news.save()
        return redirect('news_list')


class NewsUpdateView(UpdateView):
    model = News
    template_name = 'news/update_news.html'
    pk_url_kwarg = 'news_pk'
    fields = ('school', 'news_title', 'date', 'image', 'news', 'Is_View_on_Web')

    def get_form(self):
        form = super().get_form()
        form.fields['date'].widget = DatePickerInput()
        return form

    def form_valid(self, form):
        news = form.save(commit=False)
        news.save()
        return redirect('news_list')


def save_news_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            newss = News.objects.all()
            data['html_news_list'] = render_to_string('news/includes/partial_news_list.html', {
                'news': newss
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def news_view(request, news_pk):
    news = get_object_or_404(News, pk=news_pk)
    if request.method == 'POST':
        form = NewsForm(request.POST, instance=news)
    else:
        form = NewsForm(instance=news)
    return save_vehicle_form(request, form, 'news/includes/partial_news_view.html')


def news_delete(request, news_pk):
    news = get_object_or_404(News, pk=news_pk)
    data = dict()
    if request.method == 'POST':
        news.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        news = News.objects.all()
        data['html_news_list'] = render_to_string('news/includes/partial_news_list.html', {
            'news': news
        })
    else:
        context = {'news': news}
        data['html_form'] = render_to_string('news/includes/partial_news_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF NEWS MODULE<===##################################################

# ###################################===>BEGINNING OF HOLIDAY MODULE<===###############################################


class HolidayListView(ListView):
    model = Holiday
    template_name = 'holidays/holiday_list.html'
    context_object_name = 'holidays'


class HolidayCreateView(CreateView):
    model = Holiday
    template_name = 'holidays/holiday_create.html'
    fields = ('school', 'holiday_title', 'from_date', 'to_date', 'note', 'Is_View_on_Web')

    def get_form(self):
        form = super().get_form()
        form.fields['from_date'].widget = DatePickerInput()
        form.fields['to_date'].widget = DatePickerInput()
        return form

    def form_valid(self, form):
        holiday = form.save(commit=False)
        holiday.save()
        return redirect('holiday_list')


class HolidayUpdateView(UpdateView):
    model = Holiday
    template_name = 'holidays/update_holiday.html'
    pk_url_kwarg = 'holiday_pk'
    fields = ('school', 'holiday_title', 'from_date', 'to_date', 'note', 'Is_View_on_Web')

    def get_form(self):
        form = super().get_form()
        form.fields['from_date'].widget = DatePickerInput()
        form.fields['to_date'].widget = DatePickerInput()
        return form

    def form_valid(self, form):
        holiday = form.save(commit=False)
        holiday.save()
        return redirect('holiday_list')


def save_holiday_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            holidays = Holiday.objects.all()
            data['html_holiday_list'] = render_to_string('holidays/includes/partial_holiday_list.html', {
                'holidays': holidays
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def holiday_view(request, holiday_pk):
    holiday = get_object_or_404(Holiday, pk=holiday_pk)
    if request.method == 'POST':
        form = HolidayForm(request.POST, instance=holiday)
    else:
        form = HolidayForm(instance=holiday)
    return save_vehicle_form(request, form, 'holidays/includes/partial_holiday_view.html')


def holiday_delete(request, holiday_pk):
    holiday = get_object_or_404(Holiday, pk=holiday_pk)
    data = dict()
    if request.method == 'POST':
        holiday.delete()
        data['form_is_valid'] = True
        holidays = Holiday.objects.all()
        data['html_holiday_list'] = render_to_string('holidays/includes/partial_holiday_list.html', {
            'holidays': holidays
        })
    else:
        context = {'holiday': holiday}
        data['html_form'] = render_to_string('holidays/includes/partial_holiday_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF HOLIDAY MODULE<===##################################################

# ###################################===>BEGINNING OF EVENT MODULE<===###############################################


class EventListView(ListView):
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'


class EventCreateView(CreateView):
    model = Event
    template_name = 'events/event_create.html'
    fields = ('school', 'event_title', 'event_for', 'event_place', 'from_date', 'to_date', 'image', 'note',
              'Is_View_on_Web')

    def get_form(self):
        form = super().get_form()
        form.fields['from_date'].widget = DatePickerInput()
        form.fields['to_date'].widget = DatePickerInput()
        return form

    def form_valid(self, form):
        event = form.save(commit=False)
        event.save()
        return redirect('event_list')


class EventUpdateView(UpdateView):
    model = Event
    template_name = 'events/update_event.html'
    pk_url_kwarg = 'event_pk'
    fields = ('school', 'event_title', 'event_for', 'event_place', 'from_date', 'to_date', 'image', 'note',
              'Is_View_on_Web')

    def get_form(self):
        form = super().get_form()
        form.fields['from_date'].widget = DatePickerInput()
        form.fields['to_date'].widget = DatePickerInput()
        return form

    def form_valid(self, form):
        event = form.save(commit=False)
        event.save()
        return redirect('event_list')


def save_event_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            events = Event.objects.all()
            data['html_event_list'] = render_to_string('events/includes/partial_event_list.html', {
                'events': events
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def event_view(request, event_pk):
    event = get_object_or_404(Event, pk=event_pk)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
    else:
        form = EventForm(instance=event)
    return save_vehicle_form(request, form, 'events/includes/partial_event_view.html')


def event_delete(request, event_pk):
    event = get_object_or_404(Event, pk=event_pk)
    data = dict()
    if request.method == 'POST':
        event.delete()
        data['form_is_valid'] = True
        events = Event.objects.all()
        data['html_event_list'] = render_to_string('events/includes/partial_event_list.html', {
            'events': events
        })
    else:
        context = {'event': event}
        data['html_form'] = render_to_string('events/includes/partial_event_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF EVENT MODULE<===##################################################


# ###################################===>BEGINNING OF TYPE MODULE<===###############################################


class TypeListView(ListView):
    model = Type
    template_name = 'types/type_list.html'
    context_object_name = 'types'


class TypeCreateView(CreateView):
    model = Type
    template_name = 'types/type_create.html'
    fields = ('school', 'complain_type')

    def form_valid(self, form):
        type = form.save(commit=False)
        type.save()
        return redirect('type_list')


class TypeUpdateView(UpdateView):
    model = Type
    template_name = 'types/update_type.html'
    pk_url_kwarg = 'type_pk'
    fields = ('school', 'complain_type')

    def form_valid(self, form):
        type = form.save(commit=False)
        type.save()
        return redirect('type_list')


def save_type_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            types = Type.objects.all()
            data['html_type_list'] = render_to_string('types/includes/partial_type_list.html', {
                'types': types
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def type_delete(request, type_pk):
    type = get_object_or_404(Type, pk=type_pk)
    data = dict()
    if request.method == 'POST':
        type.delete()
        data['form_is_valid'] = True
        types = Type.objects.all()
        data['html_type_list'] = render_to_string('types/includes/partial_type_list.html', {
            'types': types
        })
    else:
        context = {'type': type}
        data['html_form'] = render_to_string('types/includes/partial_type_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF TYPE MODULE<===##################################################

# ###################################===>BEGINNING OF COMPLAIN MODULE<===###############################################


class ComplainListView(ListView):
    model = Complain
    template_name = 'complains/complain_list.html'
    context_object_name = 'complains'


class ComplainCreateView(CreateView):
    model = Complain
    template_name = 'complains/complain_create.html'
    fields = ('school', 'complain_user_type', 'complain_user', 'complain_type', 'complain_date', 'complain',
              'action_date')

    def get_form(self):
        form = super().get_form()
        form.fields['complain_date'].widget = DatePickerInput()
        form.fields['action_date'].widget = DatePickerInput()
        return form

    def form_valid(self, form):
        complain = form.save(commit=False)
        complain.save()
        return redirect('complain_list')


class ComplainUpdateView(UpdateView):
    model = Complain
    template_name = 'complains/update_complain.html'
    pk_url_kwarg = 'complain_pk'
    fields = ('school', 'complain_user_type', 'complain_user', 'complain_type', 'complain_date', 'complain',
              'action_date')

    def get_form(self):
        form = super().get_form()
        form.fields['complain_date'].widget = DatePickerInput()
        form.fields['action_date'].widget = DatePickerInput()
        return form

    def form_valid(self, form):
        complain = form.save(commit=False)
        complain.save()
        return redirect('complain_list')


def save_complain_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            complains = Complain.objects.all()
            data['html_complain_list'] = render_to_string('complains/includes/partial_complain_list.html', {
                'complains': complains
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def complain_view(request, complain_pk):
    complain = get_object_or_404(Complain, pk=complain_pk)
    if request.method == 'POST':
        form = ComplainForm(request.POST, instance=complain)
    else:
        form = ComplainForm(instance=complain)
    return save_vehicle_form(request, form, 'complains/includes/partial_complain_view.html')


def complain_delete(request, complain_pk):
    complain = get_object_or_404(Complain, pk=complain_pk)
    data = dict()
    if request.method == 'POST':
        complain.delete()
        data['form_is_valid'] = True
        complains = Complain.objects.all()
        data['html_complain_list'] = render_to_string('complains/includes/partial_complain_list.html', {
            'complains': complains
        })
    else:
        context = {'complain': complain}
        data['html_form'] = render_to_string('complains/includes/partial_complain_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF COMPLAIN MODULE<===################################################


# ###################################===>BEGINNING OF VISITOR MODULE<===###############################################


class VisitorListView(ListView):
    model = Visitor
    template_name = 'visitors/visitor_list.html'
    context_object_name = 'visitors'


class VisitorCreateView(CreateView):
    model = Visitor
    template_name = 'visitors/visitor_create.html'
    fields = ('school', 'name', 'phone', 'to_meet_user_type', 'to_meet_user', 'visitor_purpose',
              'check_in', 'check_out', 'note')

    def form_valid(self, form):
        visitor = form.save(commit=False)
        visitor.save()
        return redirect('visitor_list')


class VisitorUpdateView(UpdateView):
    model = Visitor
    template_name = 'visitors/update_visitor.html'
    pk_url_kwarg = 'visitor_pk'
    fields = ('school', 'name', 'phone', 'to_meet_user_type', 'to_meet_user', 'visitor_purpose',
              'check_in', 'check_out', 'note')

    def form_valid(self, form):
        visitor = form.save(commit=False)
        visitor.save()
        return redirect('visitor_list')


def save_visitor_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            visitors = Visitor.objects.all()
            data['html_visitor_list'] = render_to_string('visitors/includes/partial_visitor_list.html', {
                'visitors': visitors
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def visitor_view(request, visitor_pk):
    visitor = get_object_or_404(Visitor, pk=visitor_pk)
    if request.method == 'POST':
        form = VisitorForm(request.POST, instance=visitor)
    else:
        form = VisitorForm(instance=visitor)
    return save_visitor_form(request, form, 'visitors/includes/partial_visitor_view.html')


def visitor_delete(request, visitor_pk):
    visitor = get_object_or_404(Visitor, pk=visitor_pk)
    data = dict()
    if request.method == 'POST':
        visitor.delete()
        data['form_is_valid'] = True
        visitors = Visitor.objects.all()
        data['html_visitor_list'] = render_to_string('visitors/includes/partial_visitor_list.html', {
            'visitors': visitors
        })
    else:
        context = {'visitor': visitor}
        data['html_form'] = render_to_string('visitors/includes/partial_visitor_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF VISITOR MODULE<===###########################################

# #######################################===>BEGINNING OF SALARY GRADE<===########################################


class SalaryGradeListView(ListView):
    model = SalaryGrade
    template_name = 'salary_grades/salary_grade_list.html'
    context_object_name = 'salary_grades'


class SalaryGradeCreateView(CreateView):
    model = SalaryGrade
    template_name = 'salary_grades/salary_grade_create.html'
    fields = ('school', 'grade_name', 'basic_salary', 'house_rent', 'transport_allowance', 'medical_allowance',
              'over_time_hourly_pay', 'provident_fund', 'hourly_rate', 'total_allowance', 'total_deduction',
              'gross_salary', 'net_salary', 'note')

    def form_valid(self, form):
        school = form.save(commit=False)
        school.save()
        return redirect('salary_grade_list')


class SalaryGradeUpdateView(UpdateView):
    model = SalaryGrade
    template_name = 'salary_grades/salary_grade_update.html'
    pk_url_kwarg = 'salary_pk'
    fields = ('school', 'grade_name', 'basic_salary', 'house_rent', 'transport_allowance', 'medical_allowance',
              'over_time_hourly_pay', 'provident_fund', 'hourly_rate', 'total_allowance', 'total_deduction',
              'gross_salary', 'net_salary', 'note')

    def form_valid(self, form):
        school = form.save(commit=False)
        school.save()
        return redirect('salary_grade_list')


def save_salary_grade_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            salary_grades = SalaryGrade.objects.all()
            data['html_salary_grade_list'] = render_to_string('salary_grades/includes/partial_salary_grade_list.html', {
                'salary_grades': salary_grades
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def salary_grade_view(request, salary_pk):
    salary_grade = get_object_or_404(SalaryGrade, pk=salary_pk)
    if request.method == 'POST':
        form = SalaryGradeForm(request.POST, instance=salary_grade)
    else:
        form = SalaryGradeForm(instance=salary_grade)
    return save_salary_grade_form(request, form, 'salary_grades/includes/partial_salary_grade_view.html')


def salary_grade_delete(request, salary_pk):
    salary_grade = get_object_or_404(SalaryGrade, pk=salary_pk)
    data = dict()
    if request.method == 'POST':
        salary_grade.delete()
        data['form_is_valid'] = True
        salary_grades = SalaryGrade.objects.all()
        data['html_salary_grade_list'] = render_to_string('salary_grades/includes/partial_salary_grade_list.html', {
            'salary_grades': salary_grades
        })
    else:
        context = {'salary_grade': salary_grade}
        data['html_form'] = render_to_string('salary_grades/includes/partial_salary_grade_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)

    # #######################################===>END OF SALARY GRADE<===########################################

    # #######################################===>BEGINNING OF DISCOUNT GRADE<===########################################


class DiscountListView(ListView):
    model = Discount
    template_name = 'discounts/discount_list.html'
    context_object_name = 'discounts'


class DiscountCreateView(CreateView):
    model = Discount
    template_name = 'discounts/discount_create.html'
    fields = ('school', 'title', 'amount', 'note')

    def form_valid(self, form):
        discount = form.save(commit=False)
        discount.save()
        return redirect('discount_list')


class DiscountUpdateView(UpdateView):
    model = Discount
    template_name = 'discounts/update_discount.html'
    pk_url_kwarg = 'discount_pk'
    fields = ('school', 'title', 'amount', 'note')

    def form_valid(self, form):
        discount = form.save(commit=False)
        discount.save()
        return redirect('discount_list')


def save_discount_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            discounts = Discount.objects.all()
            data['html_discount_list'] = render_to_string('discounts/includes/partial_discount_list.html', {
                'discounts': discounts
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def discount_delete(request, discount_pk):
    discount = get_object_or_404(Discount, pk=discount_pk)
    data = dict()
    if request.method == 'POST':
        discount.delete()
        data['form_is_valid'] = True
        discounts = Discount.objects.all()
        data['html_discount_list'] = render_to_string('discounts/includes/partial_discount_list.html', {
            'discounts': discounts
        })
    else:
        context = {'discount': discount}
        data['html_form'] = render_to_string('discounts/includes/partial_discount_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)

    # #######################################===>END OF DISCOUNT MODULE<===############################################

    # #######################################===>BEGINNING OF FEE TYPE MODULE<===######################################


class FeeTypeListView(ListView):
    model = FeeType
    template_name = 'fee_types/fee_type_list.html'
    context_object_name = 'fee_types'


class FeeTypeCreateView(CreateView):
    model = FeeType
    template_name = 'fee_types/fee_type_create.html'
    fields = ('school', 'fee_type', 'fee_title', 'note')

    def form_valid(self, form):
        fee_type = form.save(commit=False)
        fee_type.save()
        return redirect('fee_type_list')


class FeeTypeUpdateView(UpdateView):
    model = FeeType
    template_name = 'fee_types/update_fee_type.html'
    pk_url_kwarg = 'fee_type_pk'
    fields = ('school', 'fee_type', 'fee_title', 'note')

    def form_valid(self, form):
        fee_type = form.save(commit=False)
        fee_type.save()
        return redirect('fee_type_list')


def save_fee_type_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            fee_types = FeeType.objects.all()
            data['html_fee_type_list'] = render_to_string('fee_types/includes/partial_fee_type_list.html', {
                'fee_types': fee_types
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def fee_type_delete(request, fee_type_pk):
    fee_type = get_object_or_404(FeeType, pk=fee_type_pk)
    data = dict()
    if request.method == 'POST':
        fee_type.delete()
        data['form_is_valid'] = True
        fee_types = FeeType.objects.all()
        data['html_fee_type_list'] = render_to_string('fee_types/includes/partial_fee_type_list.html', {
            'fee_types': fee_types
        })
    else:
        context = {'fee_type': fee_type}
        data['html_form'] = render_to_string('fee_types/includes/partial_fee_type_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF FEE TYPE MODULE<===############################################

# #######################################===>BEGINNING OF INVOICE MODULE<===######################################


class InvoiceListView(ListView):
    model = Invoice
    template_name = 'invoices/invoice_list.html'
    context_object_name = 'invoices'


# class InvoiceCreateView(CreateView):
#     model = Invoice
#     template_name = 'invoices/invoice_create.html'
#     fields = ('school', 'classroom', 'student', 'fee_type', 'fee_amount', 'discount', 'month',
#               'is_discount_applicable', 'paid_status', 'gross_amount', 'invoice_number', 'note', 'date')
#
#     def form_valid(self, form):
#         invoice = form.save(commit=False)
#         invoice.save()
#         return redirect('invoice_list')
#

def invoice_create(request):
    form = InvoiceForm(request.POST or None, request.FILES or None)
    def get_form(self):
        form = super().get_form()
        form.fields['date'].widget = MonthPickerInput()
        return form

    if form.is_valid():
        invoice = form.save(commit=False)
        invoice.save()

        invoice.school = form.cleaned_data.get('school')
        invoice.classroom = form.cleaned_data.get('classroom')
        invoice.student = form.cleaned_data.get('student')
        invoice.fee_type = form.cleaned_data.get('fee_type')
        invoice.fee_amount = form.cleaned_data.get('fee_amount')
        invoice.discount = form.cleaned_data.get('discount')
        invoice.month = form.cleaned_data.get('month')
        invoice.is_discount_applicable = form.cleaned_data.get('is_discount_applicable')
        invoice.paid_status = form.cleaned_data.get('paid_status')
        invoice.gross_amount = form.cleaned_data.get('gross_amount')
        invoice.invoice_number = form.cleaned_data.get('invoice_number')
        invoice.note = form.cleaned_data.get('note')
        invoice.date = form.cleaned_data.get('date')
        invoice.save()

        invoice_url = reverse('invoice_list')
        return redirect(invoice_url)
    context = {
        'form': form,
    }
    return render(request, 'invoices/invoice_create.html', context)


class InvoiceUpdateView(UpdateView):
    model = Invoice
    template_name = 'invoices/update_invoice.html'
    pk_url_kwarg = 'invoice_pk'
    fields = ('school', 'classroom', 'student', 'fee_type', 'fee_amount', 'discount', 'month',
              'is_discount_applicable', 'paid_status', 'gross_amount', 'invoice_number', 'note', 'date')

    def form_valid(self, form):
        invoice = form.save(commit=False)
        invoice.save()
        return redirect('invoice_list')


def save_invoice_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            invoices = Invoice.objects.all()
            data['html_invoice_list'] = render_to_string('invoices/includes/partial_invoice_list.html', {
                'invoices': invoices
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def invoice_view(request, invoice_pk):
    invoice = get_object_or_404(Invoice, pk=invoice_pk)
    if request.method == 'POST':
        form = InvoiceForm(request.POST, instance=invoice)
    else:
        form = InvoiceForm(instance=invoice)
    context = {'form': form}
    return render(request, 'invoices/invoice_view.html', context)


def invoice_delete(request, invoice_pk):
    invoice = get_object_or_404(Invoice, pk=invoice_pk)
    data = dict()
    if request.method == 'POST':
        invoice.delete()
        data['form_is_valid'] = True
        invoices = Invoice.objects.all()
        data['html_invoice_list'] = render_to_string('invoices/includes/partial_invoice_list.html', {
            'invoices': invoices
        })
    else:
        context = {'invoice': invoice}
        data['html_form'] = render_to_string('invoices/includes/partial_invoice_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF INVOICE MODULE<===############################################

# #######################################===>BEGINNING OF BULK INVOICE MODULE<===######################################


def bulk_invoice_list(request):
    bulk_invoices = BulkInvoice.objects.all()
    return render(request, 'bulk_invoices/bulk_invoice_list.html', {'bulk_invoices': bulk_invoices})


def save_bulk_invoice_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            bulk_invoices = BulkInvoice.objects.all()
            data['html_bulk_invoice_list'] = render_to_string('bulk_invoices/includes/partial_bulk_invoice_list.html', {
                'bulk_invoices': bulk_invoices
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def bulk_invoice_create(request):
    if request.method == 'POST':
        form = BulkInvoiceForm(request.POST)
    else:
        form = BulkInvoiceForm()
    return save_bulk_invoice_form(request, form, 'bulk_invoices/includes/partial_bulk_invoice_create.html')


def bulk_invoice_update(request, pk):
    bulk_invoice = get_object_or_404(BulkInvoice, pk=pk)
    if request.method == 'POST':
        form = BulkInvoiceForm(request.POST, instance=bulk_invoice)
    else:
        form = BulkInvoiceForm(instance=bulk_invoice)
    return save_bulk_invoice_form(request, form, 'bulk_invoices/includes/partial_bulk_invoice_update.html')


def bulk_invoice_delete(request, pk):
    bulk_invoice = get_object_or_404(BulkInvoice, pk=pk)
    data = dict()
    if request.method == 'POST':
        bulk_invoice.delete()
        data['form_is_valid'] = True
        bulk_invoices = BulkInvoice.objects.all()
        data['html_bulk_invoice_list'] = render_to_string('bulk_invoices/includes/partial_bulk_invoice_list.html', {
            'bulk_invoices': bulk_invoices
        })
    else:
        context = {'bulk_invoice': bulk_invoice}
        data['html_form'] = render_to_string('bulk_invoices/includes/partial_bulk_invoice_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF BULK INVOICE MODULE<===#############################################


# #######################################===>BEGINNING OF DUE FEE MODULE<===######################################

def due_fee_list(request):
    invoices = Invoice.objects.filter(paid_status__icontains='Pending')
    return render(request, 'invoices/due_list.html', {'invoices': invoices})

# #######################################===>END OF DUE FEE MODULE<===######################################


# ###################################===>BEGINNING OF DUE FEE EMAIL MODULE<===#########################################


class DueEmailListView(ListView):
    model = DueFeeEmail
    template_name = 'due_fee_emails/due_fee_email_list.html'
    context_object_name = 'due_fee_emails'


class DueEmailCreateView(CreateView):
    model = DueFeeEmail
    template_name = 'due_fee_emails/due_fee_email_create.html'
    fields = ('school', 'receiver_role', 'classroom', 'due_fee_student', 'template', 'subject', 'email_body',
              'attachment')

    def form_valid(self, form):
        due_fee_emails = form.save(commit=False)
        due_fee_emails.save()
        return redirect('due_fee_email_list')


def save_due_fee_email_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            due_fee_emails = DueFeeEmail.objects.all()
            data['html_due_fee_email_list'] = render_to_string('due_fee_emails/includes/partial_due_fee_email_list.html', {
                'due_fee_emails': due_fee_emails
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def due_fee_email_view(request, due_fee_email_pk):
    due_fee_email = get_object_or_404(DueFeeEmail, pk=due_fee_email_pk)
    if request.method == 'POST':
        form = DueFeeEmailForm(request.POST, instance=due_fee_email)
    else:
        form = DueFeeEmailForm(instance=due_fee_email)
    return save_due_fee_email_form(request, form, 'due_fee_emails/includes/partial_due_fee_email_view.html')


def due_fee_email_delete(request, due_fee_email_pk):
    due_fee_email = get_object_or_404(DueFeeEmail, pk=due_fee_email_pk)
    data = dict()
    if request.method == 'POST':
        due_fee_email.delete()
        data['form_is_valid'] = True
        due_fee_emails = DueFeeEmail.objects.all()
        data['html_due_fee_email_list'] = render_to_string('due_fee_emails/includes/partial_due_fee_email_list.html', {
            'due_fee_emails': due_fee_emails
        })
    else:
        context = {'due_fee_email': due_fee_email}
        data['html_form'] = render_to_string('due_fee_emails/includes/partial_due_fee_email_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF DUE FEE EMAIL MODULE<===###########################################

# ###################################===>BEGINNING OF DUE FEE SMS MODULE<===###########################################


class DueSmsListView(ListView):
    model = DueFeeSMS
    template_name = 'due_fee_smss/due_fee_sms_list.html'
    context_object_name = 'due_fee_smss'


class DueSmsCreateView(CreateView):
    model = DueFeeSMS
    template_name = 'due_fee_smss/due_fee_sms_create.html'
    fields = ('school', 'receiver_type', 'classroom', 'due_fee_student', 'template', 'SMS', 'gateway')

    def form_valid(self, form):
        due_fee_smss = form.save(commit=False)
        due_fee_smss.save()
        return redirect('due_fee_sms_list')


def save_due_fee_sms_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            due_fee_smss = DueFeeSMS.objects.all()
            data['html_due_fee_sms_list'] = render_to_string('due_fee_smss/includes/partial_due_fee_sms_list.html', {
                'due_fee_smss': due_fee_smss
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def due_fee_sms_view(request, due_fee_sms_pk):
    due_fee_sms = get_object_or_404(DueFeeSMS, pk=due_fee_sms_pk)
    if request.method == 'POST':
        form = DueFeeSMSForm(request.POST, instance=due_fee_sms)
    else:
        form = DueFeeSMSForm(instance=due_fee_sms)
    return save_due_fee_sms_form(request, form, 'due_fee_smss/includes/partial_due_fee_sms_view.html')


def due_fee_sms_delete(request, due_fee_sms_pk):
    due_fee_sms = get_object_or_404(DueFeeSMS, pk=due_fee_sms_pk)
    data = dict()
    if request.method == 'POST':
        due_fee_sms.delete()
        data['form_is_valid'] = True
        due_fee_smss = DueFeeSMS.objects.all()
        data['html_due_fee_sms_list'] = render_to_string('due_fee_smss/includes/partial_due_fee_sms_list.html', {
            'due_fee_smss': due_fee_smss
        })
    else:
        context = {'due_fee_sms': due_fee_sms}
        data['html_form'] = render_to_string('due_fee_smss/includes/partial_due_fee_sms_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF DUE FEE SMS MODULE<===#############################################

# ###################################===>BEGINNING OF INCOME HEAD MODULE<===###########################################


class IncomeHeadListView(ListView):
    model = IncomeHead
    template_name = 'income_heads/income_head_list.html'
    context_object_name = 'income_heads'


class IncomeHeadCreateView(CreateView):
    model = IncomeHead
    template_name = 'income_heads/income_head_create.html'
    fields = ('school', 'income_head', 'note')

    def form_valid(self, form):
        income_head = form.save(commit=False)
        income_head.save()
        return redirect('income_head_list')


class IncomeHeadUpdateView(UpdateView):
    model = IncomeHead
    template_name = 'income_heads/update_income_head.html'
    pk_url_kwarg = 'income_head_pk'
    fields = ('school', 'income_head', 'note')

    def form_valid(self, form):
        income_head = form.save(commit=False)
        income_head.save()
        return redirect('income_head_list')


def save_income_head_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            income_heads = IncomeHead.objects.all()
            data['html_income_head_list'] = render_to_string('income_heads/includes/partial_income_head_list.html', {
                'income_heads': income_heads
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def income_head_delete(request, income_head_pk):
    income_head = get_object_or_404(IncomeHead, pk=income_head_pk)
    data = dict()
    if request.method == 'POST':
        income_head.delete()
        data['form_is_valid'] = True
        income_heads = IncomeHead.objects.all()
        data['html_income_head_list'] = render_to_string('income_heads/includes/partial_income_head_list.html', {
            'income_heads': income_heads
        })
    else:
        context = {'income_head': income_head}
        data['html_form'] = render_to_string('income_heads/includes/partial_income_head_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF INCOME HEAD MODULE<===#############################################

# ###################################===>BEGINNING OF INCOME MODULE<===###############################################


class IncomeListView(ListView):
    model = Income
    template_name = 'incomes/income_list.html'
    context_object_name = 'incomes'


class IncomeCreateView(CreateView):
    model = Income
    template_name = 'incomes/income_create.html'
    fields = ('school', 'income_head', 'payment_method', 'amount', 'date', 'note')

    def form_valid(self, form):
        income = form.save(commit=False)
        income.save()
        return redirect('income_list')


class IncomeUpdateView(UpdateView):
    model = Income
    template_name = 'incomes/update_income.html'
    pk_url_kwarg = 'income_pk'
    fields = ('school', 'income_head', 'payment_method', 'amount', 'date', 'note')

    def form_valid(self, form):
        income = form.save(commit=False)
        income.save()
        return redirect('income_list')


def save_income_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            incomes = Income.objects.all()
            data['html_income_list'] = render_to_string('incomes/includes/partial_income_list.html', {
                'incomes': incomes
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def income_view(request, income_pk):
    income = get_object_or_404(Income, pk=income_pk)
    if request.method == 'POST':
        form = IncomeForm(request.POST, instance=income)
    else:
        form = IncomeForm(instance=income)
    return save_income_form(request, form, 'incomes/includes/partial_income_view.html')


def income_delete(request, income_pk):
    income = get_object_or_404(Income, pk=income_pk)
    data = dict()
    if request.method == 'POST':
        income.delete()
        data['form_is_valid'] = True
        incomes = Income.objects.all()
        data['html_income_list'] = render_to_string('incomes/includes/partial_income_list.html', {
            'incomes': incomes
        })
    else:
        context = {'income': income}
        data['html_form'] = render_to_string('incomes/includes/partial_income_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF INCOME MODULE<===#############################################

# ###################################===>BEGINNING OF EXPENDITURE HEAD MODULE<===#####################################


class ExpenditureHeadListView(ListView):
    model = ExpenditureHead
    template_name = 'expenditure_heads/expenditure_head_list.html'
    context_object_name = 'expenditure_heads'


class ExpenditureHeadCreateView(CreateView):
    model = ExpenditureHead
    template_name = 'expenditure_heads/expenditure_head_create.html'
    fields = ('school', 'expenditure_head', 'note')

    def form_valid(self, form):
        expenditure_head = form.save(commit=False)
        expenditure_head.save()
        return redirect('expenditure_head_list')


class ExpenditureHeadUpdateView(UpdateView):
    model = ExpenditureHead
    template_name = 'expenditure_heads/update_expenditure_head.html'
    pk_url_kwarg = 'expenditure_head_pk'
    fields = ('school', 'expenditure_head', 'note')

    def form_valid(self, form):
        expenditure_head = form.save(commit=False)
        expenditure_head.save()
        return redirect('expenditure_head_list')


def save_expenditure_head_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            expenditure_heads = ExpenditureHead.objects.all()
            data['html_expenditure_head_list'] = render_to_string('expenditure_heads/includes/partial_expenditure_head_list.html', {
                'expenditure_heads': expenditure_heads
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def expenditure_head_delete(request, expenditure_head_pk):
    expenditure_head = get_object_or_404(ExpenditureHead, pk=expenditure_head_pk)
    data = dict()
    if request.method == 'POST':
        expenditure_head.delete()
        data['form_is_valid'] = True
        expenditure_heads = ExpenditureHead.objects.all()
        data['html_expenditure_head_list'] = render_to_string('expenditure_heads/includes/partial_expenditure_head_list.html', {
            'expenditure_heads': expenditure_heads
        })
    else:
        context = {'expenditure_head': expenditure_head}
        data['html_form'] = render_to_string('expenditure_heads/includes/partial_expenditure_head_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF EXPENDITURE HEAD MODULE<===########################################

# ###################################===>BEGINNING OF EXPENDITURE MODULE<===###########################################


class ExpenditureListView(ListView):
    model = Expenditure
    template_name = 'expenditures/expenditure_list.html'
    context_object_name = 'expenditures'


class ExpenditureCreateView(CreateView):
    model = Expenditure
    template_name = 'expenditures/expenditure_create.html'
    fields = ('school', 'expenditure_head', 'expenditure_method', 'amount', 'date', 'note')

    def form_valid(self, form):
        expenditure = form.save(commit=False)
        expenditure.save()
        return redirect('expenditure_list')


class ExpenditureUpdateView(UpdateView):
    model = Expenditure
    template_name = 'expenditures/update_expenditure.html'
    pk_url_kwarg = 'expenditure_pk'
    fields = ('school', 'expenditure_head', 'expenditure_method', 'amount', 'date', 'note')

    def form_valid(self, form):
        expenditure = form.save(commit=False)
        expenditure.save()
        return redirect('expenditure_list')


def save_expenditure_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            expenditures = Expenditure.objects.all()
            data['html_expenditure_list'] = render_to_string('expenditures/includes/partial_expenditure_list.html', {
                'expenditures': expenditures
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def expenditure_view(request, expenditure_pk):
    expenditure = get_object_or_404(Expenditure, pk=expenditure_pk)
    if request.method == 'POST':
        form = ExpenditureForm(request.POST, instance=expenditure)
    else:
        form = ExpenditureForm(instance=expenditure)
    return save_expenditure_form(request, form, 'expenditures/includes/partial_expenditure_view.html')


def expenditure_delete(request, expenditure_pk):
    expenditure = get_object_or_404(Expenditure, pk=expenditure_pk)
    data = dict()
    if request.method == 'POST':
        expenditure.delete()
        data['form_is_valid'] = True
        expenditures = Expenditure.objects.all()
        data['html_expenditure_list'] = render_to_string('expenditures/includes/partial_expenditure_list.html', {
            'expenditures': expenditures
        })
    else:
        context = {'expenditure': expenditure}
        data['html_form'] = render_to_string('expenditures/includes/partial_expenditure_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF EXPENDITURE MODULE<===#############################################

# ###################################===>BEGINNING OF GALLERY MODULE<===###############################################


class GalleryListView(ListView):
    model = Gallery
    template_name = 'galleries/gallery_list.html'
    context_object_name = 'galleries'


class GalleryCreateView(CreateView):
    model = Gallery
    template_name = 'galleries/gallery_create.html'
    fields = ('school', 'gallery_title', 'note', 'Is_View_on_Web')

    def form_valid(self, form):
        gallery = form.save(commit=False)
        gallery.save()
        return redirect('gallery_list')


class GalleryUpdateView(UpdateView):
    model = Gallery
    template_name = 'galleries/update_gallery.html'
    pk_url_kwarg = 'gallery_pk'
    fields = ('school', 'gallery_title', 'note', 'Is_View_on_Web')

    def form_valid(self, form):
        gallery = form.save(commit=False)
        gallery.save()
        return redirect('gallery_list')


def save_gallery_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            gallerys = Gallery.objects.all()
            data['html_gallery_list'] = render_to_string('galleries/includes/partial_gallery_list.html', {
                'galleries': gallerys
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def gallery_delete(request, gallery_pk):
    gallery = get_object_or_404(Gallery, pk=gallery_pk)
    data = dict()
    if request.method == 'POST':
        gallery.delete()
        data['form_is_valid'] = True
        gallerys = Gallery.objects.all()
        data['html_gallery_list'] = render_to_string('galleries/includes/partial_gallery_list.html', {
            'galleries': gallerys
        })
    else:
        context = {'gallery': gallery}
        data['html_form'] = render_to_string('galleries/includes/partial_gallery_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF GALLERY MODULE<===##################################################

# ###################################===>BEGINNING OF IMAGE MODULE<===###############################################


class ImageListView(ListView):
    model = Image
    template_name = 'images/image_list.html'
    context_object_name = 'images'


class ImageCreateView(CreateView):
    model = Image
    template_name = 'images/image_create.html'
    fields = ('school', 'gallery_title', 'gallery_image', 'image_caption')

    def form_valid(self, form):
        image = form.save(commit=False)
        image.save()
        return redirect('image_list')


class ImageUpdateView(UpdateView):
    model = Image
    template_name = 'images/update_image.html'
    pk_url_kwarg = 'image_pk'
    fields = ('school', 'gallery_title', 'gallery_image', 'image_caption')

    def form_valid(self, form):
        image = form.save(commit=False)
        image.save()
        return redirect('image_list')


def save_image_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            images = Image.objects.all()
            data['html_image_list'] = render_to_string('images/includes/partial_image_list.html', {
                'images': images
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def image_view(request, image_pk):
    image = get_object_or_404(Image, pk=image_pk)
    if request.method == 'POST':
        form = ImageForm(request.POST, instance=image)
    else:
        form = ImageForm(instance=image)
    return save_image_form(request, form, 'images/includes/partial_image_view.html')


def image_delete(request, image_pk):
    image = get_object_or_404(Image, pk=image_pk)
    data = dict()
    if request.method == 'POST':
        image.delete()
        data['form_is_valid'] = True
        images = Image.objects.all()
        data['html_image_list'] = render_to_string('images/includes/partial_image_list.html', {
            'images': images
        })
    else:
        context = {'image': image}
        data['html_form'] = render_to_string('images/includes/partial_image_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF IMAGE MODULE<===##################################################

# ###################################===>BEGINNING OF PAGE MODULE<===###############################################


class PageListView(ListView):
    model = Page
    template_name = 'pages/page_list.html'
    context_object_name = 'pages'


class PageCreateView(CreateView):
    model = Page
    template_name = 'pages/page_create.html'
    fields = ('school', 'page_location', 'page_title', 'page_description', 'page_image')

    def form_valid(self, form):
        page = form.save(commit=False)
        page.save()
        return redirect('page_list')


class PageUpdateView(UpdateView):
    model = Page
    template_name = 'pages/update_page.html'
    pk_url_kwarg = 'page_pk'
    fields = ('school', 'page_location', 'page_title', 'page_description', 'page_image')

    def form_valid(self, form):
        page = form.save(commit=False)
        page.save()
        return redirect('page_list')


def save_page_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            pages = Page.objects.all()
            data['html_page_list'] = render_to_string('pages/includes/partial_page_list.html', {
                'pages': pages
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def page_view(request, page_pk):
    page = get_object_or_404(Page, pk=page_pk)
    if request.method == 'POST':
        form = PageForm(request.POST, instance=page)
    else:
        form = PageForm(instance=page)
    return save_page_form(request, form, 'pages/includes/partial_page_view.html')


def page_delete(request, page_pk):
    page = get_object_or_404(Page, pk=page_pk)
    data = dict()
    if request.method == 'POST':
        page.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        pages = Page.objects.all()
        data['html_page_list'] = render_to_string('pages/includes/partial_page_list.html', {
            'pages': pages
        })
    else:
        context = {'page': page}
        data['html_form'] = render_to_string('pages/includes/partial_page_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF PAGE MODULE<===##################################################

# ###################################===>BEGINNING OF SLIDER MODULE<===###############################################


class SliderListView(ListView):
    model = Slider
    template_name = 'sliders/slider_list.html'
    context_object_name = 'sliders'


class SliderCreateView(CreateView):
    model = Slider
    template_name = 'sliders/slider_create.html'
    fields = ('school', 'slider_image', 'image_title')

    def form_valid(self, form):
        slider = form.save(commit=False)
        slider.save()
        return redirect('slider_list')


class SliderUpdateView(UpdateView):
    model = Slider
    template_name = 'sliders/update_slider.html'
    pk_url_kwarg = 'slider_pk'
    fields = ('school', 'slider_image', 'image_title')

    def form_valid(self, form):
        slider = form.save(commit=False)
        slider.save()
        return redirect('slider_list')


def save_slider_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            sliders = Slider.objects.all()
            data['html_slider_list'] = render_to_string('sliders/includes/partial_slider_list.html', {
                'sliders': sliders
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def slider_view(request, slider_pk):
    slider = get_object_or_404(Slider, pk=slider_pk)
    if request.method == 'POST':
        form = SliderForm(request.POST, instance=slider)
    else:
        form = SliderForm(instance=slider)
    return save_slider_form(request, form, 'sliders/includes/partial_slider_view.html')


def slider_delete(request, slider_pk):
    slider = get_object_or_404(Slider, pk=slider_pk)
    data = dict()
    if request.method == 'POST':
        slider.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        sliders = Slider.objects.all()
        data['html_slider_list'] = render_to_string('sliders/includes/partial_slider_list.html', {
            'sliders': sliders
        })
    else:
        context = {'slider': slider}
        data['html_form'] = render_to_string('sliders/includes/partial_slider_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF SLIDER MODULE<===##################################################

# ###################################===>BEGINNING OF SLIDER MODULE<===###############################################


class AboutListView(ListView):
    model = About
    template_name = 'abouts/about_list.html'
    context_object_name = 'abouts'


class AboutCreateView(CreateView):
    model = About
    template_name = 'abouts/about_create.html'
    fields = ('school', 'about', 'about_image')

    def form_valid(self, form):
        about = form.save(commit=False)
        about.save()
        return redirect('about_list')


class AboutUpdateView(UpdateView):
    model = About
    template_name = 'abouts/update_about.html'
    pk_url_kwarg = 'about_pk'
    fields = ('school', 'about', 'about_image')

    def form_valid(self, form):
        about = form.save(commit=False)
        about.save()
        return redirect('about_list')


def save_about_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            abouts = About.objects.all()
            data['html_about_list'] = render_to_string('abouts/includes/partial_about_list.html', {
                'abouts': abouts
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def about_view(request, about_pk):
    about = get_object_or_404(About, pk=about_pk)
    if request.method == 'POST':
        form = AboutForm(request.POST, instance=about)
    else:
        form = AboutForm(instance=about)
    return save_about_form(request, form, 'abouts/includes/partial_about_view.html')


def about_delete(request, about_pk):
    about = get_object_or_404(About, pk=about_pk)
    data = dict()
    if request.method == 'POST':
        about.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        abouts = About.objects.all()
        data['html_about_list'] = render_to_string('abouts/includes/partial_about_list.html', {
            'abouts': abouts
        })
    else:
        context = {'about': about}
        data['html_form'] = render_to_string('abouts/includes/partial_about_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF ABOUT MODULE<===##################################################

# def paypal_update(request, school_pk, paypal_id):
#     paypal = get_object_or_404(Paypal, school_pk=school_pk, pk=paypal_id)
#     if request.method == 'POST':
#         form = PaypalForm(request.POST, instance=paypal)
#     else:
#         form = PaypalForm(instance=paypal)
#     return render(request, 'payments/paypal_update.html', {'paypal': paypal, 'form': form})
#

class PaypalView(UpdateView):
    model = Paypal
    template_name = 'payments/paypal_update.html'
    pk_url_kwarg = 'paypal_id'
    context_object_name = 'paypal'
    fields = ('paypal_email', 'is_demo', 'paypal_extra_charge', 'is_active')

    def form_valid(self, form):
        paypal = form.save(commit=False)
        paypal.save()
        return redirect('index')


class PaystackView(UpdateView):
    model = Paystack
    template_name = 'payments/paystack_update.html'
    pk_url_kwarg = 'paystack_id'
    context_object_name = 'paystack'
    fields = ('sk_key', 'pk_key', 'is_demo', 'extra_charge', 'is_active')

    def form_valid(self, form):
        paystack = form.save(commit=False)
        paystack.save()
        return redirect('index')


class PayTMView(UpdateView):
    model = PayTM
    template_name = 'payments/payTM_update.html'
    pk_url_kwarg = 'payTM_id'
    context_object_name = 'payTM'
    fields = ('payTM_merchant_key', 'payTM_merchant_MID', 'payTM_website', 'payTM_industry_type', 'is_demo',
              'payTM_extra_charge', 'is_active')

    def form_valid(self, form):
        payTM = form.save(commit=False)
        payTM.save()
        return redirect('index')


class PayUMoneyView(UpdateView):
    model = PayUMoney
    template_name = 'payments/payUMoney_update.html'
    pk_url_kwarg = 'payUMoney_id'
    context_object_name = 'payUMoney'
    fields = ('payUMoney_key', 'payUMoney_key_salt', 'is_demo', 'payUMoney_extra_charge', 'is_active')

    def form_valid(self, form):
        payumoney = form.save(commit=False)
        payumoney.save()
        return redirect('index')


def settings(request):
    return render(request, 'home/settings.html')


def theme(request):
    return render(request, 'home/theme.html')


def language(request):
    return render(request, 'home/language.html')


def student_attendance(request):
    context = {}
    school = request.GET.get('school')
    classroom = request.GET.get('classroom')
    context['form'] = AttendanceForm(school, classroom)
    # Filter
    q = request.GET.get('section')
    if q:
        q = q.replace('.', '')
        students = Student.objects.filter(section=str(q))
        context['students'] = students
    return render(request, 'attendance/student_attendance_list.html', context)


def present(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    try:
        if student.is_present:
            student.is_present = False
        else:
            student.is_present = True
        student.save()
    except (KeyError, Student.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})


def absent(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    try:
        if student.is_absent:
            student.is_absent = False
        else:
            student.is_absent = True
        student.save()
    except (KeyError, student.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})


def late(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    try:
        if student.is_late:
            student.is_late = False
        else:
            student.is_late = True
        student.save()
    except (KeyError, Student.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})


def classrooms_ajax(request):
    school = request.GET.get('school')
    classrooms = Classroom.objects.filter(school=school)
    context = {'classrooms': classrooms}
    return render(request, 'attendance/includes/_classrooms.html', context)


def classrooms_choices_ajax(request):
    school = request.GET.get('school')
    classrooms = Classroom.objects.filter(school=school)
    context = {'classrooms': classrooms}
    return render(request, 'attendance/includes/_classrooms_choices.html', context)


def sections_ajax(request):
    classroom = request.GET.get('classroom')
    sections = Section.objects.filter(classroom=classroom)
    context = {'sections': sections}
    return render(request, 'attendance/includes/_sections.html', context)


def sections_choices_ajax(request):
    classroom = request.GET.get('classroom')
    sections = Section.objects.filter(classroom=classroom)
    context = {'sections': sections}
    return render(request, 'attendance/includes/_sections_choices.html', context)


def load_classrooms(request):
    school_id = request.GET.get('school')
    classrooms = Classroom.objects.filter(school_id=school_id).order_by('classroom')
    return render(request, 'filter/classroom_dropdown_list_options.html', {'classrooms': classrooms})


def load_exams(request):
    school_id = request.GET.get('school')
    exams = Exam.objects.filter(school_id=school_id).order_by('exam_title')
    return render(request, 'filter/exam_dropdown_list_options.html', {'exams': exams})


def load_fee_types(request):
    school_id = request.GET.get('school')
    fee_types = FeeType.objects.filter(school_id=school_id).order_by('fee_type')
    return render(request, 'filter/fee_dropdown_list_options.html', {'fee_types': fee_types})


def load_sections(request):
    classroom_id = request.GET.get('classroom')
    sections = Section.objects.filter(classroom_id=classroom_id).order_by('section')
    return render(request, 'filter/section_dropdown_list_options.html', {'sections': sections})


def load_students(request):
    classroom_id = request.GET.get('classroom')
    students = Student.objects.filter(classroom_id=classroom_id).order_by('user')
    return render(request, 'filter/student_dropdown_list_options.html', {'students': students})


def load_roles(request):
    school_id = request.GET.get('school')
    roles = Role.objects.filter(school_id=school_id).order_by('role_name')
    return render(request, 'filter/role_dropdown_list_options.html', {'roles': roles})


def load_users(request):
    role_id = request.GET.get('user_type')
    users = User.objects.filter(roles_id=role_id).order_by('full_name')
    return render(request, 'filter/user_dropdown_list_options.html', {'users': users})


def load_subjects(request):
    classroom_id = request.GET.get('classroom')
    subjects = Subject.objects.filter(classroom_id=classroom_id).order_by('subject_name')
    return render(request, 'filter/subject_dropdown_list_options.html', {'subjects': subjects})
