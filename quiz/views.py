from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from django.db.models import Q
from django.core.mail import send_mail
from company import models as TMODEL
from student import models as SMODEL
from company import forms as TFORM
from student import forms as SFORM
from django.contrib.auth.models import User



def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')  
    return render(request,'quiz/index.html')


def is_company(user):
    return user.groups.filter(name='COMPANY').exists()

def is_student(user):
    return user.groups.filter(name='STUDENT').exists()

def afterlogin_view(request):
    if is_student(request.user):      
        return redirect('student/student-dashboard')
                
    elif is_company(request.user):
        accountapproval=TMODEL.Company.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('company/company-dashboard')
        else:
            return render(request,'company/company_wait_for_approval.html')
    else:
        return redirect('admin-dashboard')



def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return HttpResponseRedirect('adminlogin')


@login_required(login_url='adminlogin')
def admin_dashboard_view(request):
    dict={
    'total_student':SMODEL.Student.objects.all().count(),
    'total_company':TMODEL.Company.objects.all().filter(status=True).count(),
    'total_course':models.Course.objects.all().count(),
    'total_question':models.Question.objects.all().count(),
    }
    return render(request,'quiz/admin_dashboard.html',context=dict)

@login_required(login_url='adminlogin')
def admin_company_view(request):
    dict={
    'total_company':TMODEL.Company.objects.all().filter(status=True).count(),
    'pending_company':TMODEL.Company.objects.all().filter(status=False).count(),
    
    }
    return render(request,'quiz/admin_company.html',context=dict)

@login_required(login_url='adminlogin')
def admin_view_company_view(request):
    companys= TMODEL.Company.objects.all().filter(status=True)
    return render(request,'quiz/admin_view_company.html',{'companys':companys})


@login_required(login_url='adminlogin')
def update_company_view(request,pk):
    company=TMODEL.Company.objects.get(id=pk)
    user=TMODEL.User.objects.get(id=company.user_id)
    userForm=TFORM.CompanyUserForm(instance=user)
    companyForm=TFORM.CompanyForm(request.FILES,instance=company)
    mydict={'userForm':userForm,'companyForm':companyForm}
    if request.method=='POST':
        userForm=TFORM.CompanyUserForm(request.POST,instance=user)
        companyForm=TFORM.CompanyForm(request.POST,request.FILES,instance=company)
        if userForm.is_valid() and companyForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            companyForm.save()
            return redirect('admin-view-company')
    return render(request,'quiz/update_company.html',context=mydict)



@login_required(login_url='adminlogin')
def delete_company_view(request,pk):
    company=TMODEL.Company.objects.get(id=pk)
    user=User.objects.get(id=company.user_id)
    user.delete()
    company.delete()
    return HttpResponseRedirect('/admin-view-company')




@login_required(login_url='adminlogin')
def admin_view_pending_company_view(request):
    companys= TMODEL.Company.objects.all().filter(status=False)
    return render(request,'quiz/admin_view_pending_company.html',{'companys':companys})


@login_required(login_url='adminlogin')
def approve_company_view(request,pk):
    company=TMODEL.Company.objects.get(id=pk)
    company.status=True
    company.save()
    
    return HttpResponseRedirect('/admin-view-pending-company')
    """ companySalary=forms.CompanySalaryForm()
    if request.method=='POST':
        companySalary=forms.CompanySalaryForm(request.POST)
        if companySalary.is_valid():
            
            print("form is invalid")
        else:
    return render(request,'quiz/salary_form.html',{'companySalary':companySalary}) """

@login_required(login_url='adminlogin')
def reject_company_view(request,pk):
    company=TMODEL.Company.objects.get(id=pk)
    user=User.objects.get(id=company.user_id)
    user.delete()
    company.delete()
    return HttpResponseRedirect('/admin-view-pending-company')

""" @login_required(login_url='adminlogin')
def admin_view_company_salary_view(request):
    companys= TMODEL.Company.objects.all().filter(status=True)
    return render(request,'quiz/admin_view_company_salary.html',{'companys':companys})
 """



@login_required(login_url='adminlogin')
def admin_student_view(request):
    dict={
    'total_student':SMODEL.Student.objects.all().count(),
    }
    return render(request,'quiz/admin_student.html',context=dict)

@login_required(login_url='adminlogin')
def admin_view_student_view(request):
    students= SMODEL.Student.objects.all()
    return render(request,'quiz/admin_view_student.html',{'students':students})



@login_required(login_url='adminlogin')
def update_student_view(request,pk):
    student=SMODEL.Student.objects.get(id=pk)
    user=SMODEL.User.objects.get(id=student.user_id)
    userForm=SFORM.StudentUserForm(instance=user)
    studentForm=SFORM.StudentForm(request.FILES,instance=student)
    mydict={'userForm':userForm,'studentForm':studentForm}
    if request.method=='POST':
        userForm=SFORM.StudentUserForm(request.POST,instance=user)
        studentForm=SFORM.StudentForm(request.POST,request.FILES,instance=student)
        if userForm.is_valid() and studentForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            studentForm.save()
            return redirect('admin-view-student')
    return render(request,'quiz/update_student.html',context=mydict)



@login_required(login_url='adminlogin')
def delete_student_view(request,pk):
    student=SMODEL.Student.objects.get(id=pk)
    user=User.objects.get(id=student.user_id)
    user.delete()
    student.delete()
    return HttpResponseRedirect('/admin-view-student')


@login_required(login_url='adminlogin')
def admin_course_view(request):
    return render(request,'quiz/admin_course.html')


@login_required(login_url='adminlogin')
def admin_add_course_view(request):
    courseForm=forms.CourseForm()
    if request.method=='POST':
        courseForm=forms.CourseForm(request.POST)
        if courseForm.is_valid():        
            courseForm.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-view-course')
    return render(request,'quiz/admin_add_course.html',{'courseForm':courseForm})


@login_required(login_url='adminlogin')
def admin_view_course_view(request):
    courses = models.Course.objects.all()
    return render(request,'quiz/admin_view_course.html',{'courses':courses})

@login_required(login_url='adminlogin')
def delete_course_view(request,pk):
    course=models.Course.objects.get(id=pk)
    course.delete()
    return HttpResponseRedirect('/admin-view-course')



@login_required(login_url='adminlogin')
def admin_question_view(request):
    return render(request,'quiz/admin_question.html')


@login_required(login_url='adminlogin')
def admin_add_question_view(request):
    questionForm=forms.QuestionForm()
    if request.method=='POST':
        questionForm=forms.QuestionForm(request.POST)
        if questionForm.is_valid():
            question=questionForm.save(commit=False)
            course=models.Course.objects.get(id=request.POST.get('courseID'))
            question.course=course
            question.save()       
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-view-question')
    return render(request,'quiz/admin_add_question.html',{'questionForm':questionForm})


@login_required(login_url='adminlogin')
def admin_view_question_view(request):
    courses= models.Course.objects.all()
    return render(request,'quiz/admin_view_question.html',{'courses':courses})

@login_required(login_url='adminlogin')
def view_question_view(request,pk):
    questions=models.Question.objects.all().filter(course_id=pk)
    return render(request,'quiz/view_question.html',{'questions':questions})

@login_required(login_url='adminlogin')
def delete_question_view(request,pk):
    question=models.Question.objects.get(id=pk)
    question.delete()
    return HttpResponseRedirect('/admin-view-question')

@login_required(login_url='adminlogin')
def admin_view_student_marks_view(request):
    students= SMODEL.Student.objects.all()
    return render(request,'quiz/admin_view_student_marks.html',{'students':students})

@login_required(login_url='adminlogin')
def admin_view_marks_view(request,pk):
    courses = models.Course.objects.all()
    response =  render(request,'quiz/admin_view_marks.html',{'courses':courses})
    response.set_cookie('student_id',str(pk))
    return response

@login_required(login_url='adminlogin')
def admin_check_marks_view(request,pk):
    course = models.Course.objects.get(id=pk)
    student_id = request.COOKIES.get('student_id')
    student= SMODEL.Student.objects.get(id=student_id)

    results= models.Result.objects.all().filter(exam=course).filter(student=student)
    return render(request,'quiz/admin_check_marks.html',{'results':results})
    




def aboutus_view(request):
    return render(request,'quiz/aboutus.html')

def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return render(request, 'quiz/contactussuccess.html')
    return render(request, 'quiz/contactus.html', {'form':sub})


