#-*- coding: utf-8 -*-
from django.shortcuts import render
from forms import *
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404, render_to_response, render
from django import forms
from django.contrib import messages
from website.models import *
import extras
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
import os
import json
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect, HttpResponse
import djcelery
djcelery.setup_loader()


class YT_Form(forms.Form):
    url = forms.CharField(max_length=100)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                # Redirect to a success page.
                messages.info(request, u"{0},\n zostałeś zalogowany".format(username))
                return redirect('index')
            else:
                # Return a 'disabled account' error message
                return render(request, 'login.html', {'error_message': "Konto wyłączone", })
        else:
            return render(request, 'login.html', {'error_message': u"Błąd logowania", })
            # Return an 'invalid login' error message.
    else:
        return render(request, 'login.html', {})


def logoutuser(request):
    from django.contrib.auth import logout
    logout(request)
    messages.info(request, "Zostałeś wylogowany ")
    return redirect('login_user')


@login_required(login_url='login_user')
def help(request):
    return render(request,'help.html')


@login_required(login_url='login_user')
def files(request):
    if not os.path.exists(settings.MAIN_MP3_DIR):
        messages.error(request, "Brak katalogu {}. Ustaw istniejący w settings.MAIN_MP3_DIR".format(settings.MAIN_MP3_DIR))
        return render(request, 'files.html')
    else:
        if not os.path.exists(settings.MAIN_MP3_DIR+"/"+str(request.user)):
            os.mkdir(settings.MAIN_MP3_DIR+"/"+str(request.user))
            messages.info(request, "Utworzyłem katalog użytkownika: {}.".format(settings.MAIN_MP3_DIR+"/"+str(request.user)))

        mp3_list = os.listdir(settings.MAIN_MP3_DIR+"/"+str(request.user))
        paginator = Paginator(mp3_list, 10)

        page = request.GET.get('page')
        try:
            files = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            files = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            files = paginator.page(paginator.num_pages)
        return render(request, 'files.html', {"files": files, "files_count": len(mp3_list) , "main_url": "/mp3/"+str(request.user)})


@login_required(login_url='login_user')
def delete_file(request, file):
    path = settings.MAIN_MP3_DIR+"/"+str(request.user)+"/"+file
    os.remove(path)
    message="Deleted file {}".format(path)
    messages.info(request, message)
    print(message)
    return redirect('files')


@login_required(login_url='login_user')
def index(request):
    if request.method == "POST":
        form = YT_Form(request.POST)
        if form.is_valid():
            try:
                from website.celery import download

                #dodanie urla do kolejki
                URL = YT_URL(url=form.cleaned_data["url"], status=1, user=request.user)
                URL.save()

                download.delay(URL, form.cleaned_data["url"], request.user)
                messages.info(request, u"Plik dodany do przetwarzania w tle")

            except:
                messages.info(request, u"Błąd pobierania pliku")
                raise
        else:
            messages.error(request, form.errors)
            return render(request, 'kontakt.html', {'form': form, 'error_message': form.errors})

    else:
        form = YT_Form()
    return render(request,'index.html', {'form': form})


@login_required(login_url='login_user')
def files_queued(request):
    #status 2 znaczy prztwarzany plik
    converted_files = YT_URL.objects.all().filter(status=1)
    queue = dict()
    for file in converted_files:
        queue[file.url]=str(file.status)
    return HttpResponse(json.dumps(queue), content_type="application/json")


@login_required(login_url='login_user')
def files_convert(request):
    #status 2 znaczy prztwarzany plik
    converted_files = YT_URL.objects.all().filter(status=2)
    queue = dict()
    for file in converted_files:
        queue[file.url]=str(file.status)
    return HttpResponse(json.dumps(queue), content_type="application/json")


@login_required(login_url='login_user')
def files_converted(request):
    #status 2 znaczy prztwarzany plik
    converted_files = YT_URL.objects.all().filter(status=3)[:5]
    queue = dict()
    for file in converted_files:
        queue[file.url]=str(file.status)
    return HttpResponse(json.dumps(queue), content_type="application/json")


@login_required(login_url='login_user')
def files_errors(request):
    #status 2 znaczy prztwarzany plik
    converted_files = YT_URL.objects.all().filter(status=4)
    queue = dict()
    for file in converted_files:
        queue[file.url]=str(file.status)
    return HttpResponse(json.dumps(queue), content_type="application/json")


def user_profile(request):
    from django.contrib.auth.models import User
    u = User.objects.get(username=request.user.username)
    if request.method == 'POST':
        form = UserPasswordForm(request.POST, request.FILES)
        if form.is_valid():
            if u.check_password(request.POST['old_password']) is True:
                if request.POST['new_password'] != request.POST['new_password2']:
                    messages.error(request, u"Hasła nie są identyczne")
                else:
                    u.set_password(request.POST['new_password'])
                    u.save()
                    messages.info(request, u"Hasło zostało zmienione")
            else:
                messages.error(request, u"Stare hasło jest niepoprawne")
    else:
        form = UserPasswordForm(request.POST, request.FILES)
    context = {
        'form': form,
        'USER':  u
    }
    return render(request, 'user_profile.html', context)





