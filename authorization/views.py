from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect
from .forms import AudioUploadForm
from .models import AudioFile


def login_page(request):
    error_message = None

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect(reverse('upload_audio'))
            else:
                error_message = "Такого пользователя не существует"
    else:
        form = AuthenticationForm()

    return render(request, 'authorization/authorization.html', {'form': form, 'error_message': error_message})


def process_audio(audio_file):
    # Обработка аудио файла
    result = "Результат обработки аудио файла"
    return result


@login_required
def upload_audio(request):
    if request.method == 'POST':
        form = AudioUploadForm(request.POST, request.FILES)
        if form.is_valid():
            audio_file = form.save(commit=False)
            audio_file.user = request.user  # Установите связь с текущим пользователем
            audio_file.result = process_audio(audio_file.audio)
            audio_file.save()
            return redirect('upload_audio')
    else:
        form = AudioUploadForm()

    audio_files = AudioFile.objects.filter(user=request.user)
    return render(request, 'authorization/audio.html', {'form': form, 'audio_files': audio_files})
