from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import Profile
from django.contrib import messages


def user_login(request):
# создается экземпляр формы с переданными данными
    if request.method == 'POST':
        form = LoginForm(request.POST)
# Если она невалидна, то ошибки формы будут выведены позже в шаблоне (например, если пользователь не заполнил одно из полей)
        if form.is_valid():
# form.cleaned_data используется для получения очищенных данных из формы, которые были отправлены на сервер. Этот метод автоматически применяет все правила валидации, определенные в модели формы, и возвращает словарь, содержащий только допустимые данные. Он также удаляет все пробелы и специальные символы из данных, чтобы предотвратить возможные атаки на безопасность.
            cd = form.cleaned_data
# authenticate(). Указанный метод принимает объект request, параметры username и password и возвращает
# объект User, если пользователь был успешно аутентифицирован, либо None в противном случае. 
            user = authenticate(request, username=cd['username'], assword=cd['password'])

            if user is not None:
                if user.is_active:
# login Этот метод принимает запрос и объект пользователя и создает сеанс для пользователя, если он прошел проверку подлинности. 
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})

# Декоратор login_required проверяет аутентификацию текущего пользователя.
@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html', {'section': 'dashboard'})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Создать новый объект пользователя, но пока не сохранять его
            new_user = user_form.save(commit=False)
            # Установить выбранный пароль
            new_user.set_password(user_form.cleaned_data['password'])
            # Сохранить объект User
            new_user.save()
            # Создать профиль пользователя
            Profile.objects.create(user=new_user)
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})

# добавили новое представление edit, чтобы пользователи могли редактировать свою личную информацию
# добавили в него декоратор login_required, поскольку только аутентифицированные пользователи могут редактировать свои профили.
@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.success(request, 'Error updating yout profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request,
                'account/edit.html',
                {'user_form': user_form,
                'profile_form': profile_form})