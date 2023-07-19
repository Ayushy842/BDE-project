from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from requests import session
from app import models
import datetime
from django.contrib import messages
from django.utils.dateparse import parse_date


# Create your views here.
def dashboard(request):
    projects = models.Project.objects.all()
    all_data = []

    for project in projects:
        data = {
            'project_id':project.id,
            'project_name': project.project_name,
            'technology': project.technology,
            'project_date': project.date,
            'round1_date': '',  # Default value or placeholder for Round1
            'round2_date': '',  # Default value or placeholder for Round2
            'round3_date': '',  # Default value or placeholder for Round3
        }

        try:
            round1 = models.Round1.objects.get(project=project)
            data['round1_date'] = round1.date
        except models.Round1.DoesNotExist:
            pass

        try:
            round2 = models.Round2.objects.get(project=project)
            data['round2_date'] = round2.date
        except models.Round2.DoesNotExist:
            pass

        try:
            round3 = models.Round3.objects.get(project=project)
            data['round3_date'] = round3.date
        except models.Round3.DoesNotExist:
            pass

        all_data.append(data)

    return render(request, 'dashboard.html', {'all_data': all_data})


def logout(request):
    del request.session['user']
    return redirect('login')


def success(request):
    return render(request,'success.html')


def delete(request, project_id):
    project = models.Project.objects.get(id=project_id)
    project.delete()
    return redirect('dashboard')
               

def login(request):
    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            bde_user = models.BDE_User.objects.get(username=username)
            if bde_user.password==password:
                request.session['user']=username
                # return render(request,'project.html',{'bde_user':bde_user})
                return redirect('dashboard')
            else:
                return render(request,'login.html',{'errors':'Invalid password.'})
        except models.BDE_User.DoesNotExist:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'login.html',{'errors':'Invalid username or password.'})
        except Exception as e:
            messages.error(request, 'Something went wrong, Sorry!')
            return render(request, 'login.html',{'errors':'Something Went Wrong'})
    else:
        return render(request,'login.html')


def project(request):
    if request.method == "POST":
        try:
            project_name = request.POST.get('project_name')
            technology = request.POST.get('technology')
            date = datetime.datetime.strptime(request.POST.get('date'), '%Y-%m-%d').date()
            print("date",date)
            resume_shared = request.POST.get('resume_shared', 'NO') 
            logged_in_user = models.BDE_User.objects.get(username=request.session['user'])
            
            if resume_shared == 'NO':
                project = models.Project(project_name=project_name, date=date, technology=technology, resume_shared=False, edited_by=logged_in_user)
                project.save()
                return redirect('dashboard')
            project = models.Project(project_name=project_name, date=date, technology=technology, resume_shared=True, edited_by=logged_in_user)

            project.save()
            print("Project ID: ", project.id)
            return redirect('dashboard')
            # return redirect('round1', project_id=project.id)
        except Exception as e:
            print("Error in project View")
            return render(request, 'project.html', {'errors': 'Something went wrong. Sorry!'})
    else:
        
        return render(request, 'project.html')


def round1(request, project_id):
    project = models.Project.objects.get(id=project_id)
    round1_data, created = models.Round1.objects.get_or_create(project=project)
    if request.method == "POST":
        try:
            date = request.POST.get('date')
            if date:
                date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
            else:
                date = None
            screenshot_shared = request.FILES.get('screenshot_shared')
            our_review = request.POST.get('our_review')
            client_review = request.POST.get('client_review')
            logged_in_user = models.BDE_User.objects.get(username=request.session['user'])

            # Check if Round1 object already exists for the given project
            round1_obj = models.Round1.objects.filter(project=project).first()

            if round1_obj:
                # Update the existing Round1 object
                round1_obj.date = date
                round1_obj.screenshot_shared = screenshot_shared
                round1_obj.our_review = our_review
                round1_obj.client_review = client_review
                round1_obj.edited_by = logged_in_user
                round1_obj.save()
            else:
                # Create a new Round1 object
                round1_obj = models.Round1(
                    project=project,
                    date=date,
                    screenshot_shared=screenshot_shared,
                    our_review=our_review,
                    client_review=client_review,
                    edited_by=logged_in_user
                )
                round1_obj.save()

            return redirect('round2', project_id=project.id)
        except Exception as e:
            print("Error in round1 view")
            return render(request, 'round1.html', {'errors': 'Something Went Wrong, Sorry!'})
    else:
        return render(request, 'round1.html', {'project_id': project_id,'round1_data': round1_data,})
    

def round2(request, project_id):
    project = models.Project.objects.get(id=project_id)
    round2_data, created = models.Round2.objects.get_or_create(project=project)
    if request.method == "POST":
        try:
            date = request.POST.get('date')
            if date:
                date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
            else:
                date = None
            screenshot_shared = request.FILES.get('screenshot_shared')
            our_review = request.POST.get('our_review')
            client_review = request.POST.get('client_review')
            logged_in_user = models.BDE_User.objects.get(username=request.session['user'])

            # Check if Round2 object already exists for the given project
            round2_obj = models.Round2.objects.filter(project=project).first()

            if round2_obj:
                # Update the existing Round2 object
                round2_obj.date = date
                round2_obj.screenshot_shared = screenshot_shared
                round2_obj.our_review = our_review
                round2_obj.client_review = client_review
                round2_obj.edited_by = logged_in_user
                round2_obj.save()
            else:
                # Create a new Round2 object
                round2_obj = models.Round2(
                    project=project,
                    date=date,
                    screenshot_shared=screenshot_shared,
                    our_review=our_review,
                    client_review=client_review,
                    edited_by=logged_in_user
                )
                round2_obj.save()

            return redirect('round3', project_id=project_id)
        except Exception as e:
            return render(request, 'round2.html', {'errors': 'Something Went Wrong, Sorry!'})
    else:
        
        return render(request, 'round2.html', {'project_id': project_id,'round2_data':round2_data})

def round3(request, project_id):
    project = models.Project.objects.get(id=project_id)
    round3_data, created = models.Round3.objects.get_or_create(project=project)

    if request.method == "POST":
        try:
            date = request.POST.get('date')
            if date:
                date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
            else:
                date = None

            screenshot_shared = request.FILES.get('screenshot_shared')  # Get the uploaded file
            
            round3_obj = models.Round3.objects.filter(project=project).first()

            if round3_obj:
                # Update the existing Round3 object
                round3_obj.date = date
                round3_obj.our_review = request.POST.get('our_review')
                round3_obj.client_review = request.POST.get('client_review')
                round3_obj.edited_by = models.BDE_User.objects.get(username=request.session['user'])

                # Update the screenshot_shared field if a new file was uploaded
                if screenshot_shared:
                    round3_obj.screenshot_shared = screenshot_shared

                round3_obj.save()
            else:
                # Create a new Round3 object
                round3_obj = models.Round3(
                    project=project,
                    date=date,
                    screenshot_shared=screenshot_shared,
                    our_review=request.POST.get('our_review'),
                    client_review=request.POST.get('client_review'),
                    edited_by=models.BDE_User.objects.get(username=request.session['user'])
                )
                round3_obj.save()

            # Redirect to a success page or any other page
            return HttpResponseRedirect(reverse('success'))
        except ValueError:
            return render(request, 'round3.html', {'project_id': project_id, 'errors': 'Invalid date format'})
        except Exception as e:
            
            return render(request, 'round3.html', {'project_id': project_id, 'errors': str(e)})
    else:
        return render(request, 'round3.html', {'project_id': project_id, 'round3_data': round3_data})


def edit_project(request, project_id):
    project = get_object_or_404(models.Project, pk=project_id)
    if request.method == 'POST':
        try:
            project_name = request.POST.get('project_name')
            technology = request.POST.get('technology')
            date = request.POST.get('date')
            requirement_recieved = request.POST.get('requirement_recieved')
            edited_by = models.BDE_User.objects.get(username=request.session['user'])
            resume_shared = request.POST.get('resume_shared')

            # Check if the project object already exists
            if project:
                # Update the existing project object
                project.project_name = project_name
                project.technology = technology
                project.date = date
                project.requirement_recieved = requirement_recieved
                project.edited_by = edited_by
                if resume_shared == "no":
                    project.resume_shared = False
                    project.save()
                    return redirect('dashboard')
                project.resume_shared = True
                project.save()
            else:
                # Create a new project object
                project = models.Project(
                    project_name=project_name,
                    technology=technology,
                    date=date,
                    requirement_recieved=requirement_recieved,
                    edited_by=edited_by,
                    resume_shared=(resume_shared == "yes")
                )
                project.save()

            return redirect('round1', project_id=project.id)
        except Exception as e:
            print("Error in edit_project view")
            return render(request, 'edit_project.html', {'errors': 'Something Went Wrong, Sorry!'})
    else:
        context = {
            'project': project,
        }
        return render(request, 'edit_project.html', context)
