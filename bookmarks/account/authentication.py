from django.contrib.auth.models import User


# Аутентифицировать посредством адреса электронной почты.
class EmailAuthBackend:
# authenticate(): извлекается пользователь с данным адресом электронной почты, а  пароль проверяется посредством встроенного метода
#check_password() модели пользователя. Указанный метод хеширует пароль, чтобы сравнить данный пароль с  паролем, хранящимся в  базе данных.
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            return None
# get_user(): пользователь извлекается по его ИД, указанному в параметре user_id. Django использует аутентифицировавший пользователя
# бэкенд, чтобы извлечь объект User на время сеанса пользователя. pk (сокращение от primary key)
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
