from django.urls import path
from company import views
from django.contrib.auth.views import LoginView

urlpatterns = [
path('companyclick', views.companyclick_view),
path('companylogin', LoginView.as_view(template_name='company/companylogin.html'),name='companylogin'),
path('companysignup', views.company_signup_view,name='companysignup'),
path('company-dashboard', views.company_dashboard_view,name='company-dashboard'),
path('company-exam', views.company_exam_view,name='company-exam'),
path('company-add-exam', views.company_add_exam_view,name='company-add-exam'),
path('company-view-exam', views.company_view_exam_view,name='company-view-exam'),
path('delete-exam/<int:pk>', views.delete_exam_view,name='delete-exam'),


path('company-question', views.company_question_view,name='company-question'),
path('company-add-question', views.company_add_question_view,name='company-add-question'),
path('company-view-question', views.company_view_question_view,name='company-view-question'),
path('see-question/<int:pk>', views.see_question_view,name='see-question'),
path('remove-question/<int:pk>', views.remove_question_view,name='remove-question'),
]