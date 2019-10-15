from django.conf.urls import url, include
from django.urls import path
from . import views
from django.contrib.auth.views import *

urlpatterns = [

    url(r'^login_user/$', LoginView.as_view(template_name='home/login.html'), name='login_user'),
    url(r'^logout_user/$', LogoutView.as_view(), name='logout_user'),

    url(r'^profile/(?P<username>[\w.@+-]+)/$', views.UserProfileView.as_view(), name='profile'),
    url(r'^profile/update/$', views.ProfileUpdateView.as_view(), name='update'),

    url(r'^change-password/$', views.change_password, name='change_password'),
    url(r'^password-reset/$', PasswordResetView.as_view(template_name='home/reset_password.html'),
        name='password_reset'),
    url(r'^password-reset/done/$', PasswordResetDoneView.as_view(template_name='home/reset_password_done.html'),
        name='password_reset_done'),
    url(r'^reset-password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', PasswordResetConfirmView.as_view(),
        {'template_name': 'accounts/reset_password_confirm.html',
         'post_reset_redirect': 'accounts:password_reset_complete'}, name='password_reset_confirm'),
    url(r'^reset-password/complete/$', PasswordResetCompleteView.as_view(template_name='home/login.html'),
        {'template_name': 'accounts/reset_password_complete.html'}, name='password_reset_complete'),

    url(r'^dashboard/$', views.index, name='index'),
    url(r'^settings/$', views.SchoolSettingView.as_view(), name='settings'),
    url(r'^theme/$', views.theme, name='theme'),
    url(r'^language/$', views.language, name='language'),

    url(r'^administrator/school/index/$', views.SchoolListView.as_view(), name='school_list'),
    url(r'^administrator/school/add/$', views.SchoolCreateView.as_view(), name='school_create'),
    url(r'^administrator/school/update/(?P<school_pk>\d+)/$', views.SchoolUpdateView.as_view(), name='school_update'),
    url(r'^administrator/school/(?P<school_pk>\d+)/view/$', views.school_view, name='school_view'),
    url(r'^administrator/school/(?P<school_pk>\d+)/delete/$', views.school_delete, name='school_delete'),

    url(r'^administrator/role/index/$', views.RoleListView.as_view(), name='role_list'),
    url(r'^administrator/role/add/$', views.RoleCreateView.as_view(), name='role_create'),
    url(r'^administrator/role/update/(?P<role_pk>\d+)/$', views.RoleUpdateView.as_view(), name='role_update'),
    url(r'^administrator/role/(?P<role_pk>\d+)/delete/$', views.role_delete, name='role_delete'),

    url(r'^administrator/emailsetting/index/$', views.EmailSettingsListView.as_view(), name='emailsetting_list'),
    url(r'^administrator/emailsetting/add/$', views.EmailSettingsCreateView.as_view(), name='emailsetting_create'),
    url(r'^administrator/emailsetting/update/(?P<emailsetting_pk>\d+)/$', views.EmailSettingsUpdateView.as_view(),
        name='emailsetting_update'),
    url(r'^administrator/emailsetting/(?P<emailsetting_pk>\d+)/view/$', views.emailsetting_view,
        name='emailsetting_view'),
    url(r'^administrator/emailsetting/(?P<emailsetting_pk>\d+)/delete/$', views.emailsetting_delete,
        name='emailsetting_delete'),

    url(r'^school_settings/$', views.SchoolSettingView.as_view(), name='school_setting'),

    url(r'^paypal/(?P<paypal_id>\d+)/$', views.PaypalView.as_view(), name='paypal_update'),
    url(r'^payUMoney/(?P<payUMoney_id>\d+)/$', views.PayUMoneyView.as_view(), name='payUMoney_update'),
    url(r'^paystack/(?P<paystack_id>\d+)/$', views.PaystackView.as_view(), name='paystack_update'),
    url(r'^payTM/(?P<payTM_id>\d+)/$', views.PayTMView.as_view(), name='payTM_update'),

    url(r'^administrator/user/index/$', views.manage_user, name='manage_users'),
    url(r'^administrator/usercredential/index/$', views.manage_credential, name='manage_credential'),
    url(r'^administrator/activitylog/index/$', views.activity, name='activity'),
    url(r'^administrator/backup/index/$', views.backup, name='backup'),

    url(r'^frontoffice/purpose/index/$', views.PurposeListView.as_view(), name='purpose_list'),
    url(r'^frontoffice/purpose/add/$', views.PurposeCreateView.as_view(), name='purpose_create'),
    url(r'^frontoffice/purpose/edit/(?P<purpose_pk>\d+)/$', views.PurposeUpdateView.as_view(), name='purpose_update'),
    url(r'^frontoffice/purpose/(?P<purpose_pk>\d+)/$', views.purpose_delete, name='purpose_delete'),

    url(r'^administrator/superadmin/index/$', views.SuperuserListView.as_view(), name='superuser_list'),
    url(r'^administrator/superadmin/add/$', views.superuser_create, name='superuser_create'),
    url(r'^administrator/superadmin/update/(?P<superuser_pk>\d+)/$', views.superuser_update, name='superuser_update'),
    url(r'^administrator/superadmin/view/(?P<superuser_pk>\d+)/$', views.superuser_view, name='superuser_view'),
    url(r'^administrator/superadmin/delete/(?P<superuser_pk>\d+)/$', views.superuser_delete, name='superuser_delete'),

    url(r'^teacher/index/$', views.TeacherListView.as_view(), name='teacher_list'),
    url(r'^teacher/add/$', views.teacher_create, name='teacher_create'),
    url(r'^teacher/edit/(?P<teacher_pk>\d+)/$', views.teacher_update, name='teacher_update'),
    url(r'^teacher/view/(?P<teacher_pk>\d+)/$', views.teacher_view, name='teacher_view'),
    url(r'^teacher/delete/(?P<teacher_pk>\d+)/$', views.teacher_delete, name='teacher_delete'),

    url(r'^administrator/feedback/index/$', views.FeedbackListView.as_view(), name='feedback_list'),
    # url(r'^administrator/feedback/add/$', views.FeedbackCreateView.as_view(), name='feedback_create'),
    url(r'^administrator/feedback/edit/(?P<feedback_pk>\d+)/$', views.FeedbackUpdateView.as_view(),
        name='feedback_update'),
    url(r'^administrator/feedback/delete/(?P<feedback_pk>\d+)/$', views.feedback_delete, name='feedback_delete'),

    url(r'^hrm/designation/index/$', views.DesignationListView.as_view(), name='designation_list'),
    url(r'^hrm/designation/add/$', views.DesignationCreateView.as_view(), name='designation_create'),
    url(r'^hrm/designation/edit/(?P<designation_pk>\d+)/$', views.DesignationUpdateView.as_view(),
        name='designation_update'),
    url(r'^hrm/designation/delete/(?P<designation_pk>\d+)/$', views.designation_delete, name='designation_delete'),

    url(r'^administrator/emailtemplate/index/$', views.EmailtemplateListView.as_view(), name='emailtemplate_list'),
    url(r'^administrator/emailtemplate/add/$', views.EmailtemplateCreateView.as_view(), name='emailtemplate_create'),
    url(r'^administrator/emailtemplate/edit/(?P<emailtemplate_pk>\d+)/$', views.EmailtemplateUpdateView.as_view(),
        name='emailtemplate_update'),
    url(r'^administrator/emailtemplate/delete/(?P<emailtemplate_pk>\d+)/$', views.emailtemplate_delete,
        name='emailtemplate_delete'),

    url(r'^administrator/smstemplate/index/$', views.SmstemplateListView.as_view(), name='smstemplate_list'),
    url(r'^administrator/smstemplate/add/$', views.SmstemplateCreateView.as_view(), name='smstemplate_create'),
    url(r'^administrator/smstemplate/edit/(?P<smstemplate_pk>\d+)/$', views.SmstemplateUpdateView.as_view(), name='smstemplate_update'),
    url(r'^administrator/smstemplate/delete/(?P<smstemplate_pk>\d+)/$', views.smstemplate_delete, name='smstemplate_delete'),

    url(r'^hrm/employee/index/$', views.EmployeeListView.as_view(), name='employee_list'),
    url(r'^hrm/employee/add/$', views.employee_create, name='employee_create'),
    url(r'^hrm/employee/edit/(?P<employee_pk>\d+)/$', views.employee_update, name='employee_update'),
    url(r'^hrm/employee/view/(?P<employee_pk>\d+)/$', views.employee_view, name='employee_view'),
    url(r'^hrm/employee/delete/(?P<employee_pk>\d+)/$', views.employee_delete, name='employee_delete'),

    url(r'^student/type/index/$', views.StudentTypeListView.as_view(), name='student_type_list'),
    url(r'^student/type/add/$', views.StudentTypeCreateView.as_view(), name='student_type_create'),
    url(r'^student/type/edit/(?P<student_type_pk>\d+)/$', views.StudentTypeUpdateView.as_view(), name='student_type_update'),
    url(r'^student/type/delete/(?P<student_type_pk>\d+)/$', views.student_type_delete, name='student_type_delete'),

    url(r'^student/index/$', views.StudentListView.as_view(), name='student_list'),
    url(r'^student/admission/index/$', views.OnlineStudentListView.as_view(), name='online_student_list'),
    url(r'^student/add/$', views.student_create, name='student_create'),
    url(r'^student/edit/(?P<student_pk>\d+)/$', views.student_update, name='student_update'),
    url(r'^student/view/(?P<student_pk>\d+)/$', views.student_view, name='student_view'),
    url(r'^student/delete/(?P<student_pk>\d+)/$', views.student_delete, name='student_delete'),

    url(r'^student/activity/index/$', views.ActivityListView.as_view(), name='activity_list'),
    url(r'^student/activity/add/$', views.ActivityCreateView.as_view(), name='activity_create'),
    url(r'^student/activity/edit/(?P<activity_pk>\d+)/$', views.ActivityUpdateView.as_view(), name='activity_update'),
    url(r'^student/activity/view/(?P<activity_pk>\d+)/$', views.activity_view, name='activity_view'),
    url(r'^student/activity/delete/(?P<activity_pk>\d+)/$', views.activity_delete, name='activity_delete'),

    url(r'^card/admitsetting/index/$', views.CardListView.as_view(), name='card_list'),
    url(r'^card/admitsetting/add/$', views.CardCreateView.as_view(), name='card_create'),
    url(r'^card/admitsetting/edit/(?P<card_pk>\d+)/$', views.CardUpdateView.as_view(), name='card_update'),
    url(r'^card/admitsetting/view/(?P<card_pk>\d+)/$', views.card_view, name='card_view'),
    url(r'^card/admitsetting/delete/(?P<card_pk>\d+)/$', views.card_delete, name='card_delete'),

    url(r'^card/idsetting/index/$', views.AdmitListView.as_view(), name='admit_list'),
    url(r'^card/idsetting/add/$', views.AdmitCreateView.as_view(), name='admit_create'),
    url(r'^card/idsetting/edit/(?P<admit_pk>\d+)/$', views.AdmitUpdateView.as_view(), name='admit_update'),
    url(r'^card/idsetting/view/(?P<admit_pk>\d+)/$', views.admit_view, name='admit_view'),
    url(r'^card/idsetting/delete/(?P<admit_pk>\d+)/$', views.admit_delete, name='admit_delete'),

    url(r'^guardian/index/$', views.GuardianListView.as_view(), name='guardian_list'),
    url(r'^guardian/add/$', views.guardian_create, name='guardian_create'),
    url(r'^guardian/update/(?P<guardian_pk>\d+)/$', views.guardian_update, name='guardian_update'),
    url(r'^guardian/view/(?P<guardian_pk>\d+)/$', views.guardian_view, name='guardian_view'),
    url(r'^guardian/delete/(?P<guardian_pk>\d+)/$', views.guardian_delete, name='guardian_delete'),

    url(r'^academic/classes/index/$', views.ClassroomListView.as_view(), name='classroom_list'),
    url(r'^academic/classes/add/$', views.ClassroomCreateView.as_view(), name='classroom_create'),
    url(r'^academic/classes/update/(?P<classroom_pk>\d+)/$', views.ClassroomUpdateView.as_view(), name='classroom_update'),
    url(r'^academic/classes/delete/(?P<classroom_pk>\d+)/$', views.classroom_delete, name='classroom_delete'),

    url(r'^academic/section/index/$', views.SectionListView.as_view(), name='section_list'),
    url(r'^academic/section/add/$', views.SectionCreateView.as_view(), name='section_create'),
    url(r'^academic/section/update/(?P<section_pk>\d+)/$', views.SectionUpdateView.as_view(), name='section_update'),
    url(r'^academic/section/delete/(?P<section_pk>\d+)/$', views.section_delete, name='section_delete'),

    url(r'^administrator/year/$', views.AcademicYearListView.as_view(), name='year_list'),
    url(r'^administrator/year/add/$', views.AcademicYearCreateView.as_view(), name='year_create'),
    url(r'^administrator/year/update/(?P<year_pk>\d+)/$', views.AcademicYearUpdateView.as_view(), name='year_update'),
    url(r'^administrator/year/delete/(?P<year_pk>\d+)/$', views.year_delete, name='year_delete'),

    url(r'^academic/syllabus/index/$', views.SyllabusListView.as_view(), name='syllabus_list'),
    url(r'^academic/syllabus/add/$', views.SyllabusCreateView.as_view(), name='syllabus_create'),
    url(r'^academic/syllabus/edit/(?P<syllabus_pk>\d+)/$', views.SyllabusUpdateView.as_view(), name='syllabus_update'),
    url(r'^academic/syllabus/view/(?P<syllabus_pk>\d+)/$', views.syllabus_view, name='syllabus_view'),
    url(r'^academic/syllabus/delete/(?P<syllabus_pk>\d+)/$', views.syllabus_delete, name='syllabus_delete'),

    url(r'^frontoffice/receive/index/$', views.ReceiveListView.as_view(), name='receive_list'),
    url(r'^frontoffice/receive/add/$', views.ReceiveCreateView.as_view(), name='receive_create'),
    url(r'^frontoffice/receive/edit/(?P<receive_pk>\d+)/$', views.ReceiveUpdateView.as_view(), name='receive_update'),
    url(r'^frontoffice/receive/view/(?P<receive_pk>\d+)/$', views.receive_view, name='receive_view'),
    url(r'^frontoffice/receive/delete/(?P<receive_pk>\d+)/$', views.receive_delete, name='receive_delete'),

    url(r'^frontoffice/dispatch/index/$', views.DispatchListView.as_view(), name='dispatch_list'),
    url(r'^frontoffice/dispatch/add/$', views.DispatchCreateView.as_view(), name='dispatch_create'),
    url(r'^frontoffice/dispatch/edit/(?P<dispatch_pk>\d+)/$', views.DispatchUpdateView.as_view(), name='dispatch_update'),
    url(r'^frontoffice/dispatch/view/(?P<dispatch_pk>\d+)/$', views.dispatch_view, name='dispatch_view'),
    url(r'^frontoffice/dispatch/delete/(?P<dispatch_pk>\d+)/$', views.dispatch_delete, name='dispatch_delete'),

    url(r'^academic/subject/index/$', views.SubjectListView.as_view(), name='subject_list'),
    url(r'^academic/subject/add/$', views.SubjectCreateView.as_view(), name='subject_create'),
    url(r'^academic/subject/edit/(?P<subject_pk>\d+)/$', views.SubjectUpdateView.as_view(), name='subject_update'),
    url(r'^academic/subject/view/(?P<subject_pk>\d+)/$', views.subject_view, name='subject_view'),
    url(r'^academic/subject/delete/(?P<subject_pk>\d+)/$', views.subject_delete, name='subject_delete'),

    url(r'^academic/material/index/$', views.MaterialListView.as_view(), name='material_list'),
    url(r'^academic/material/add/$', views.MaterialCreateView.as_view(), name='material_create'),
    url(r'^academic/material/edit/(?P<material_pk>\d+)/$', views.MaterialUpdateView.as_view(), name='material_update'),
    url(r'^academic/material/view/(?P<material_pk>\d+)/$', views.material_view, name='material_view'),
    url(r'^academic/material/delete/(?P<material_pk>\d+)/$', views.material_delete, name='material_delete'),

    url(r'^academic/routine/index/$', views.routine_list, name='routine_list'),
    url(r'^academic/routine/add/$', views.RoutineCreateView.as_view(), name='routine_create'),
    url(r'^academic/routine/update/(?P<routine_pk>\d+)/$', views.RoutineUpdateView.as_view(), name='routine_update'),
    url(r'^academic/routine/delete/(?P<routine_pk>\d+)/$', views.routine_delete, name='routine_delete'),

    # path('schedule/', views.schedule_main, name='schedule_main'),
    # path('schedule/new/', views.create_edit_slot, name='create_slot'),
    # path('slot/<int:id>/edit/', views.create_edit_slot, name='edit_slot'),

    url(r'^leave/type/index/$', views.LeaveListView.as_view(), name='leave_list'),
    url(r'^leave/type/add/$', views.LeaveCreateView.as_view(), name='leave_create'),
    url(r'^leave/type/update/(?P<leave_pk>\d+)/$', views.LeaveUpdateView.as_view(), name='leave_update'),
    url(r'^leave/type/delete/(?P<leave_pk>\d+)/$', views.leave_delete, name='leave_delete'),

    url(r'^leave/application/index/$', views.ApplicationListView.as_view(), name='application_list'),
    url(r'^leave/application/add/$', views.ApplicationCreateView.as_view(), name='application_create'),
    url(r'^leave/waiting/index/$', views.WaitingApplicationListView.as_view(), name='waiting_application_list'),
    url(r'^leave/declined/index/$', views.DeclinedApplicationListView.as_view(), name='declined_application_list'),
    url(r'^leave/approved/add/$', views.ApprovedApplicationListView.as_view(), name='approved_application_list'),
    url(r'^leave/application/update/(?P<application_pk>\d+)/$', views.ApplicationUpdateView.as_view(), name='application_update'),
    url(r'^leave/application/delete/(?P<application_pk>\d+)/$', views.application_delete, name='application_delete'),

    url(r'^(?P<school_id>\d+)/bulk_students/$', views.bulk_student_list, name='bulk_student_list'),
    url(r'^(?P<school_id>\d+)/bulk_student/create/$', views.bulk_student_create, name='bulk_student_create'),

    url(r'^assignment/index/$', views.AssignmentListView.as_view(), name='assignment_list'),
    url(r'^assignment/add/$', views.AssignmentCreateView.as_view(), name='assignment_create'),
    url(r'^assignment/edit/(?P<assignment_pk>\d+)/$', views.AssignmentUpdateView.as_view(), name='assignment_update'),
    url(r'^assignment/view/(?P<assignment_pk>\d+)/$', views.assignment_view, name='assignment_view'),
    url(r'^assignment/delete/(?P<assignment_pk>\d+)/$', views.assignment_delete, name='assignment_delete'),

    url(r'^exam/mark/index/$', views.manage_mark, name='manage_mark'),

    url(r'^exam/grade/index/$', views.ExamGradeListView.as_view(), name='exam_grade_list'),
    url(r'^exam/grade/add/$', views.ExamGradeCreateView.as_view(), name='exam_grade_create'),
    url(r'^exam/grade/edit/(?P<exam_grade_pk>\d+)/$', views.ExamGradeUpdateView.as_view(), name='exam_grade_update'),
    url(r'^exam/grade/delete/(?P<exam_grade_pk>\d+)/$', views.exam_grade_delete, name='exam_grade_delete'),

    url(r'^exam/index/$', views.ExamListView.as_view(), name='exam_list'),
    url(r'^exam/add/$', views.ExamCreateView.as_view(), name='exam_create'),
    url(r'^exam/update/(?P<exam_pk>\d+)/$', views.ExamUpdateView.as_view(), name='exam_update'),
    url(r'^exam/delete/(?P<exam_pk>\d+)/$', views.exam_delete, name='exam_delete'),

    url(r'^exam/schedule/index/$', views.ExamScheduleListView.as_view(), name='exam_schedule_list'),
    url(r'^exam/schedule/add/$', views.ExamScheduleCreateView.as_view(), name='exam_schedule_create'),
    url(r'^exam/schedule/edit/(?P<exam_schedule_pk>\d+)/$', views.ExamScheduleUpdateView.as_view(),
        name='exam_schedule_update'),
    url(r'^exam/schedule/delete/(?P<exam_schedule_pk>\d+)/$', views.ExamScheduleUpdateView.as_view(),
        name='exam_schedule_delete'),

    url(r'^exam/suggestion/index/$', views.ExamSuggestionListView.as_view(), name='exam_suggestion_list'),
    url(r'^exam/suggestion/add/$', views.ExamSuggestionCreateView.as_view(), name='exam_suggestion_create'),
    url(r'^exam/suggestion/edit/(?P<exam_suggestion_pk>\d+)/$', views.ExamSuggestionUpdateView.as_view(),
        name='exam_suggestion_update'),
    url(r'^exam/suggestion/delete/(?P<exam_suggestion_pk>\d+)/$', views.exam_suggestion_delete,
        name='exam_suggestion_delete'),

    url(r'^certificate/type/index$', views.CertificateListView.as_view(), name='certificate_list'),
    url(r'^certificate/type/add/$', views.CertificateCreateView.as_view(), name='certificate_create'),
    url(r'^certificate/type/edit/(?P<certificate_pk>\d+)/$', views.CertificateUpdateView.as_view(),
        name='certificate_update'),
    url(r'^certificate/type/delete/(?P<certificate_pk>\d+)/$', views.certificate_delete, name='certificate_delete'),

    url(r'^frontoffice/calllog/index/$', views.LogListView.as_view(), name='log_list'),
    url(r'^frontoffice/calllog/add/$', views.LogCreateView.as_view(), name='log_create'),
    url(r'^frontoffice/calllog/edit/(?P<log_pk>\d+)/$', views.LogUpdateView.as_view(), name='log_update'),
    url(r'^frontoffice/calllog/view/(?P<log_pk>\d+)/$', views.log_view, name='log_view'),
    url(r'^frontoffice/calllog/delete/(?P<log_pk>\d+)/$', views.log_delete, name='log_delete'),

    url(r'^library/book/index/$', views.BookListView.as_view(), name='book_list'),
    url(r'^library/book/add/$', views.BookCreateView.as_view(), name='book_create'),
    url(r'^library/book/edit/(?P<book_pk>\d+)/$', views.BookUpdateView.as_view(), name='book_update'),
    url(r'^library/book/view/(?P<book_pk>\d+)/$', views.book_view, name='book_view'),
    url(r'^library/book/delete/(?P<book_pk>\d+)/$', views.book_delete, name='book_delete'),

    url(r'^library/ebook/index/$', views.EBookListView.as_view(), name='ebook_list'),
    url(r'^library/ebook/add/$', views.EBookCreateView.as_view(), name='ebook_create'),
    url(r'^library/ebook/edit/(?P<ebook_pk>\d+)/$', views.EBookUpdateView.as_view(), name='ebook_update'),
    url(r'^library/ebook/view/(?P<ebook_pk>\d+)/$', views.ebook_view, name='ebook_view'),
    url(r'^library/ebook/delete/(?P<ebook_pk>\d+)/$', views.ebook_delete, name='ebook_delete'),

    url(r'^library/member/index/$', views.LibraryMemberListView.as_view(), name='library_member_list'),
    url(r'^library/member/add/$', views.LibraryMemberCreateView.as_view(), name='library_member_create'),
    url(r'^library/member/edit/(?P<library_member_pk>\d+)/$', views.LibraryMemberUpdateView.as_view(),
        name='library_member_update'),
    url(r'^library/member/delete/(?P<library_member_pk>\d+)/$', views.library_member_delete,
        name='library_member_delete'),

    url(r'^library/issue/index/$', views.IssueListView.as_view(), name='issue_list'),
    url(r'^library/issue/add/$', views.IssueCreateView.as_view(), name='issue_create'),
    url(r'^library/issue/update/(?P<issue_pk>\d+)/$', views.IssueUpdateView.as_view(), name='issue_update'),
    url(r'^library/issue/delete/(?P<issue_pk>\d+)/$', views.issue_delete, name='issue_delete'),

    url(r'^transport/vehicle/index/$', views.VehicleListView.as_view(), name='vehicle_list'),
    url(r'^transport/vehicle/add/$', views.VehicleCreateView.as_view(), name='vehicle_create'),
    url(r'^transport/vehicle/edit/(?P<vehicle_pk>\d+)/$', views.VehicleUpdateView.as_view(), name='vehicle_update'),
    url(r'^transport/vehicle/view/(?P<vehicle_pk>\d+)/$', views.vehicle_view, name='vehicle_view'),
    url(r'^transport/vehicle/delete/(?P<vehicle_pk>\d+)/$', views.vehicle_delete, name='vehicle_delete'),

    url(r'^transport/route/index/$', views.RouteListView.as_view(), name='route_list'),
    url(r'^transport/route/add/$', views.RouteCreateView.as_view(), name='route_create'),
    url(r'^transport/route/update/(?P<route_pk>\d+)/$', views.RouteUpdateView.as_view(), name='route_update'),
    url(r'^transport/route/view/(?P<route_pk>\d+)/$', views.route_view, name='route_view'),
    url(r'^transport/route/delete/(?P<route_pk>\d+)/$', views.route_delete, name='route_delete'),

    url(r'^transport/member/index/$', views.TransportMemberListView.as_view(), name='transport_member_list'),
    url(r'^transport/member/add/$', views.TransportMemberCreateView.as_view(), name='transport_member_create'),
    url(r'^transport/member/update/(?P<transport_member_pk>\d+)/$', views.TransportMemberUpdateView.as_view(),
        name='transport_member_update'),
    url(r'^transport/member/delete/(?P<transport_member_pk>\d+)/$', views.transport_member_delete,
        name='transport_member_delete'),

    url(r'^hostel/index/$', views.HostelListView.as_view(), name='hostel_list'),
    url(r'^hostel/add/$', views.HostelCreateView.as_view(), name='hostel_create'),
    url(r'^hostel/edit/(?P<hostel_pk>\d+)/$', views.HostelUpdateView.as_view(), name='hostel_update'),
    url(r'^hostel/view/(?P<hostel_pk>\d+)/$', views.hostel_view, name='hostel_view'),
    url(r'^hostel/delete/(?P<hostel_pk>\d+)/$', views.hostel_delete, name='hostel_delete'),

    url(r'^hostel/room/index$', views.RoomListView.as_view(), name='room_list'),
    url(r'^hostel/room/add/$', views.RoomCreateView.as_view(), name='room_create'),
    url(r'^hostel/room/update/(?P<room_pk>\d+)/$', views.RoomUpdateView.as_view(), name='room_update'),
    url(r'^hostel/room/view/(?P<room_pk>\d+)/$', views.room_view, name='room_view'),
    url(r'^hostel/room/delete/(?P<room_pk>\d+)/$', views.room_delete, name='room_delete'),

    url(r'^hostel/member/index/$', views.HostelMemberListView.as_view(), name='hostel_member_list'),
    url(r'^hostel/member/add/$', views.HostelMemberCreateView.as_view(), name='hostel_member_create'),
    url(r'^hostel/member/edit/(?P<member_pk>\d+)/$', views.HostelMemberUpdateView.as_view(),
        name='hostel_member_update'),
    url(r'^hostel/member/delete/(?P<member_pk>\d+)/$', views.hostel_member_delete, name='hostel_member_delete'),

    url(r'^message/mail/index/$', views.EmailListView.as_view(), name='email_list'),
    url(r'^message/mail/add/$', views.EmailCreateView.as_view(), name='email_create'),
    url(r'^message/mail/view/(?P<email_pk>\d+)/$', views.email_view, name='email_view'),
    url(r'^message/mail/delete/(?P<email_pk>\d+)/$', views.email_delete, name='email_delete'),

    url(r'^message/text/index/$', views.SMSListView.as_view(), name='sms_list'),
    url(r'^message/text/add/$', views.SMSCreateView.as_view(), name='sms_create'),
    url(r'^message/text/view/(?P<SMS_pk>\d+)/$', views.sms_view, name='sms_view'),
    url(r'^message/text/sms/delete/(?P<SMS_pk>\d+)/$', views.sms_delete, name='sms_delete'),

    url(r'^announcement/notice/index/$', views.NoticeListView.as_view(), name='notice_list'),
    url(r'^announcement/notice/add/$', views.NoticeCreateView.as_view(), name='notice_create'),
    url(r'^announcement/notice/edit/(?P<notice_pk>\d+)/$', views.NoticeUpdateView.as_view(), name='notice_update'),
    url(r'^announcement/notice/view/(?P<notice_pk>\d+)/$', views.notice_view, name='notice_view'),
    url(r'^announcement/notice/delete/(?P<notice_pk>\d+)/$', views.notice_delete, name='notice_delete'),

    url(r'^announcement/news/index/$', views.NewsListView.as_view(), name='news_list'),
    url(r'^announcement/news/add/$', views.NewsCreateView.as_view(), name='news_create'),
    url(r'^announcement/news/update/(?P<news_pk>\d+)/$', views.NewsUpdateView.as_view(), name='news_update'),
    url(r'^announcement/news/view/(?P<news_pk>\d+)/$', views.news_view, name='news_view'),
    url(r'^announcement/news/delete/(?P<news_pk>\d+)/$', views.news_delete, name='news_delete'),

    url(r'^complain/type/index/$', views.TypeListView.as_view(), name='type_list'),
    url(r'^complain/type/add/$', views.TypeCreateView.as_view(), name='type_create'),
    url(r'^complain/type/update/(?P<type_pk>\d+)/$', views.TypeUpdateView.as_view(), name='type_update'),
    url(r'^complain/type/delete/(?P<type_pk>\d+)/$', views.type_delete, name='type_delete'),

    url(r'^complain/index/$', views.ComplainListView.as_view(), name='complain_list'),
    url(r'^complain/add/$', views.ComplainCreateView.as_view(), name='complain_create'),
    url(r'^complain/update/(?P<complain_pk>\d+)/$', views.ComplainUpdateView.as_view(), name='complain_update'),
    url(r'^complain/view/(?P<complain_pk>\d+)/$', views.complain_view, name='complain_view'),
    url(r'^complain/delete/(?P<complain_pk>\d+)/$', views.complain_delete, name='complain_delete'),

    url(r'^announcement/holiday/index/$', views.HolidayListView.as_view(), name='holiday_list'),
    url(r'^announcement/holiday/add/$', views.HolidayCreateView.as_view(), name='holiday_create'),
    url(r'^announcement/holiday/update/(?P<holiday_pk>\d+)/$', views.HolidayUpdateView.as_view(),
        name='holiday_update'),
    url(r'^announcement/holiday/view/(?P<holiday_pk>\d+)/$', views.holiday_view, name='holiday_view'),
    url(r'^announcement/holiday/delete/(?P<holiday_pk>\d+)/$', views.holiday_delete, name='holiday_delete'),

    url(r'^event/index/$', views.EventListView.as_view(), name='event_list'),
    url(r'^event/add/$', views.EventCreateView.as_view(), name='event_create'),
    url(r'^event/edit/(?P<event_pk>\d+)/$', views.EventUpdateView.as_view(), name='event_update'),
    url(r'^event/view/(?P<event_pk>\d+)/$', views.event_view, name='event_view'),
    url(r'^event/delete(?P<event_pk>\d+)/$', views.event_delete, name='event_delete'),

    url(r'^frontoffice/visitor/index/$', views.VisitorListView.as_view(), name='visitor_list'),
    url(r'^frontoffice/visitor/add/$', views.VisitorCreateView.as_view(), name='visitor_create'),
    url(r'^frontoffice/visitor/view/(?P<visitor_pk>\d+)/$', views.visitor_view, name='visitor_update'),
    url(r'^frontoffice/visitor/edit/(?P<visitor_pk>\d+)/$', views.VisitorUpdateView.as_view(), name='visitor_update'),
    url(r'^frontoffice/visitor/delete/(?P<visitor_pk>\d+)/$', views.visitor_delete, name='visitor_delete'),

    url(r'^payroll/grade/index/$', views.SalaryGradeListView.as_view(), name='salary_grade_list'),
    url(r'^payroll/grade/add/$', views.SalaryGradeCreateView.as_view(), name='salary_grade_create'),
    url(r'^payroll/grade/edit/(?P<salary_pk>\d+)/$', views.SalaryGradeUpdateView.as_view(), name='salary_grade_update'),
    url(r'^payroll/grade/delete/(?P<salary_pk>\d+)/$', views.salary_grade_delete, name='salary_grade_delete'),
    url(r'^payroll/grade/view/(?P<salary_pk>\d+)/$', views.salary_grade_view, name='salary_grade_view'),

    url(r'^accounting/discount/index/$', views.DiscountListView.as_view(), name='discount_list'),
    url(r'^accounting/discount/add/$', views.DiscountCreateView.as_view(), name='discount_create'),
    url(r'^accounting/discount/update/(?P<discount_pk>\d+)/$', views.DiscountUpdateView.as_view(),
        name='discount_update'),
    url(r'^accounting/discount/delete/(?P<discount_pk>\d+)/$', views.discount_delete, name='discount_delete'),

    url(r'^accounting/feetype/$', views.FeeTypeListView.as_view(), name='fee_type_list'),
    url(r'^accounting/feetype/add/$', views.FeeTypeCreateView.as_view(), name='fee_type_create'),
    url(r'^accounting/feetype/update/(?P<fee_type_pk>\d+)/$', views.FeeTypeUpdateView.as_view(),
        name='fee_type_update'),
    url(r'^accounting/feetype/delete/(?P<fee_type_pk>\d+)/$', views.fee_type_delete, name='fee_type_delete'),

    url(r'^accounting/duefeeemail/index/$', views.DueEmailListView.as_view(), name='due_fee_email_list'),
    url(r'^accounting/duefeeemail/create/$', views.DueEmailCreateView.as_view(), name='due_fee_email_create'),
    url(r'^accounting/duefeeemail/view/(?P<due_fee_email_pk>\d+)/$', views.due_fee_email_view, name='due_fee_email_view'),
    url(r'^accounting/duefeeemail/delete/(?P<due_fee_email_pk>\d+)/$', views.due_fee_email_delete, name='due_fee_email_delete'),

    url(r'^accounting/duefeeesms/index/$', views.DueSmsListView.as_view(), name='due_fee_sms_list'),
    url(r'^accounting/duefeeesms/create/$', views.DueSmsCreateView.as_view(), name='due_fee_sms_create'),
    url(r'^accounting/duefeeesms/update/(?P<due_fee_sms_pk>\d+)/$', views.due_fee_sms_view, name='due_fee_sms_view'),
    url(r'^accounting/duefeeesms/delete/(?P<due_fee_sms_pk>\d+)/$', views.due_fee_sms_delete, name='due_fee_sms_delete'),

    url(r'^accounting/income/index/$', views.IncomeListView.as_view(), name='income_list'),
    url(r'^accounting/income/create/$', views.IncomeCreateView.as_view(), name='income_create'),
    url(r'^accounting/income/update/(?P<income_pk>\d+)/$', views.IncomeUpdateView.as_view(), name='income_update'),
    url(r'^accounting/income/delete/(?P<income_pk>\d+)/$', views.income_delete, name='income_delete'),

    url(r'^accounting/incomehead/index/$', views.IncomeHeadListView.as_view(), name='income_head_list'),
    url(r'^accounting/incomehead/create/$', views.IncomeHeadCreateView.as_view(), name='income_head_create'),
    url(r'^accounting/incomehead/update/(?P<income_head_pk>\d+)/$', views.IncomeHeadUpdateView.as_view(), name='income_head_update'),
    url(r'^accounting/incomehead/delete/(?P<income_head_pk>\d+)/$', views.income_head_delete, name='income_head_delete'),

    url(r'^accounting/expenditure/index/$', views.ExpenditureListView.as_view(), name='expenditure_list'),
    url(r'^accounting/expenditure/create/$', views.ExpenditureCreateView.as_view(), name='expenditure_create'),
    url(r'^accounting/expenditure/update/(?P<expenditure_pk>\d+)/$', views.ExpenditureUpdateView.as_view(), name='expenditure_update'),
    url(r'^accounting/expenditure/delete/(?P<expenditure_pk>\d+)/$', views.expenditure_delete, name='expenditure_delete'),

    url(r'^accounting/exphead/index/$', views.ExpenditureHeadListView.as_view(), name='expenditure_head_list'),
    url(r'^accounting/exphead/create/$', views.ExpenditureHeadCreateView.as_view(),
        name='expenditure_head_create'),
    url(r'^accounting/exphead/update/(?P<expenditure_head_pk>\d+)/$', views.ExpenditureHeadUpdateView.as_view(),
        name='expenditure_head_update'),
    url(r'^accounting/exphead/delete/(?P<expenditure_head_pk>\d+)/$', views.expenditure_head_delete,
        name='expenditure_head_delete'),

    url(r'^accounting/invoice/due/$', views.due_fee_list, name='due_fee_list'),

    url(r'^accounting/invoice/index/$', views.InvoiceListView.as_view(), name='invoice_list'),
    url(r'^accounting/invoice/add/$', views.invoice_create, name='invoice_create'),
    url(r'^accounting/invoice/update/(?P<invoice_pk>\d+)/$', views.InvoiceUpdateView.as_view(), name='invoice_update'),
    url(r'^accounting/invoice/view/(?P<invoice_pk>\d+)/$', views.invoice_view, name='invoice_view'),
    url(r'^accounting/invoice/delete/(?P<invoice_pk>\d+)/$', views.invoice_delete, name='invoice_delete'),

    url(r'^gallery/index/$', views.GalleryListView.as_view(), name='gallery_list'),
    url(r'^gallery/add/$', views.GalleryCreateView.as_view(), name='gallery_create'),
    url(r'^gallery/update/(?P<gallery_pk>\d+)/$', views.GalleryUpdateView.as_view(), name='gallery_update'),
    url(r'^gallery/delete/(?P<gallery_pk>\d+)/$', views.gallery_delete, name='gallery_delete'),

    url(r'^gallery/image/index/$', views.ImageListView.as_view(), name='image_list'),
    url(r'^gallery/image/create/$', views.ImageCreateView.as_view(), name='image_create'),
    url(r'^gallery/image/update/(?P<image_pk>\d+)/$', views.ImageUpdateView.as_view(), name='image_update'),
    url(r'^gallery/image/view/(?P<image_pk>\d+)/$', views.image_view, name='image_view'),
    url(r'^gallery/image/delete/(?P<image_pk>\d+)/$', views.image_delete, name='image_delete'),

    url(r'^frontend/slider/index/$', views.SliderListView.as_view(), name='slider_list'),
    url(r'^frontend/slider/add/$', views.SliderCreateView.as_view(), name='slider_create'),
    url(r'^frontend/slider/update/(?P<slider_pk>\d+)/$', views.SliderUpdateView.as_view(), name='slider_update'),
    url(r'^frontend/slider/view/(?P<slider_pk>\d+)/$', views.slider_view, name='slider_view'),
    url(r'^frontend/slider/delete/(?P<slider_pk>\d+)/$', views.slider_delete, name='slider_delete'),

    url(r'^frontend/about/index/$', views.AboutListView.as_view(), name='about_list'),
    url(r'^frontend/about/add/$', views.AboutCreateView.as_view(), name='about_create'),
    url(r'^frontend/about/update/(?P<about_pk>\d+)/$', views.AboutUpdateView.as_view(), name='about_update'),
    url(r'^frontend/about/view/(?P<about_pk>\d+)/$', views.about_view, name='about_view'),
    url(r'^frontend/about/delete/(?P<about_pk>\d+)/$', views.about_delete, name='about_delete'),

    url(r'^frontend/index/$', views.PageListView.as_view(), name='page_list'),
    url(r'^frontend/add/$', views.PageCreateView.as_view(), name='page_create'),
    url(r'^frontend/update/(?P<page_pk>\d+)/$', views.PageUpdateView.as_view(), name='page_update'),
    url(r'^frontend/view/(?P<page_pk>\d+)/$', views.page_view, name='page_view'),
    url(r'^frontend/delete/(?P<page_pk>\d+)/$', views.page_delete, name='page_delete'),

    url(r'^attendance/students/$', views.attendance_student, name='attendance_student'),
    url(r'^attendance/teachers/$', views.attendance_teacher, name='attendance_teacher'),
    url(r'^attendance/employees/$', views.attendance_employee, name='attendance_employee'),

    path('student_attendance/', views.student_attendance, name='student_attendance'),
    url(r'^(?P<student_id>[0-9]+)/present/$', views.present, name='present'),
    url(r'^(?P<student_id>[0-9]+)/late/$', views.late, name='late'),
    url(r'^(?P<student_id>[0-9]+)/absent/$', views.absent, name='absent'),

    path('classrooms/ajax/', views.classrooms_ajax, name='classrooms_ajax'),
    path('classrooms/choices/ajax/', views.classrooms_choices_ajax, name='classrooms_choices_ajax'),
    path('sections/ajax/', views.sections_ajax, name='sections_ajax'),
    path('sections/choices/ajax/', views.sections_choices_ajax, name='sections_choices_ajax'),

    # path('profile/', views.profile, name='profile'),
    # path('profile/view/<int:id>/', views.user_profile, name='user_profile'),
    # path('profile/edit/', views.profile_update, name='edit_profile'),

    path('ajax/load-subjects/', views.load_subjects, name='ajax_load_subjects'),
    path('ajax/load-exams/', views.load_exams, name='ajax_load_exams'),
    path('ajax/load-classrooms/', views.load_classrooms, name='ajax_load_classrooms'),
    path('ajax/load-sections/', views.load_sections, name='ajax_load_sections'),
    path('ajax/load-roles/', views.load_roles, name='ajax_load_roles'),
    path('ajax/load-users/', views.load_users, name='ajax_load_users'),
    path('ajax/load-students/', views.load_students, name='ajax_load_students'),
    path('ajax/load-fee_types/', views.load_fee_types, name='ajax_load_fee_types'),
    path('ajax/load_fee_amount/', views.load_fee_amount, name='ajax_load_fee_amount'),
#
    path('create_fees_type/', views.create_fees_type, name='create_fees_type'),
    path('create_invoice/', views.create_invoice, name='create_invoice'),
    path('Incomes/index/Add/', views.Addincomehead, name='Addincomehead'),
    path('Incomes/index/List/', views.list_incomeheads, name='list_incomeheads'),
    url(r'^payroll/grade/index/$', views.addSalaryGrade, name='addSalaryGrade'),

]
