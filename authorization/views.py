from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect
from pydub import AudioSegment

from .forms import AudioUploadForm
from .models import AudioFile

import os
import wave
from vosk import Model, KaldiRecognizer, SetLogLevel
import json
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences


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
    # Установите уровень логирования Vosk (опционально)
    SetLogLevel(0)

    # Загрузите модель для русского языка
    model = Model("authorization/vosk-model-small-ru-0.22")
    mp3_audio = AudioSegment.from_mp3(audio_file.name)
    audio_file = mp3_audio.export(audio_file.name.replace(".mp3", ".wav"), format="wav")

    # Откройте аудиофайл
    wf = wave.open(audio_file, "rb")

    # Создайте распознаватель
    rec = KaldiRecognizer(model, wf.getframerate())

    # Список для хранения результатов распознавания
    results = []

    # Читайте данные из аудиофайла и передавайте их распознавателю
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            results.append(result)
    text = ''
    for elem in results:
        text += list(elem.values())[0] + ' '

    model = load_model("my_model.h5")

    max_words = 10000  # Максимальное количество слов в словаре
    max_len = 100  # Максимальная длина последовательности

    tokenizer = Tokenizer(num_words=max_words, oov_token='<OOV>')
    tokenizer.fit_on_texts([text])
    sequences = tokenizer.texts_to_sequences([text])
    padded_sequence = pad_sequences(sequences, maxlen=max_len, padding='post', truncating='post')

    # Выполнение предсказания
    predictions = model.predict(padded_sequence)

    # Вывод результатов

    class_names = ['плохой', 'хороший']

    predicted_class_index = tf.argmax(predictions, axis=-1).numpy()[0]
    predicted_class = class_names[predicted_class_index]

    print("Предсказанный класс:", predicted_class)
    # Обработка аудио файла
    result = predicted_class
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
