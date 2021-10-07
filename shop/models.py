from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название категории')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class App(models.Model):
    ACTIVITY_CHOICES = [
        (True, 'Верифицированное ПО'),
        (False, 'Неверифицированое ПО')
    ]

    title = models.CharField(max_length=255, verbose_name='Название')
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name='Заставка', blank=True, upload_to='avatars/')
    description = models.TextField(verbose_name='Описание')
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE, related_name='apps')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата загрузка')
    file = models.FileField(upload_to='files/', verbose_name='Файл')
    flag = models.BooleanField(choices=ACTIVITY_CHOICES, default=False, verbose_name='Верификация')
    download_count = models.PositiveIntegerField(default=0, verbose_name='Количество скачиваний')
    user = models.ForeignKey(User, verbose_name='Пользователь', default=None, null=True, on_delete=models.CASCADE)

    # image придется скорее всего переделывать т.к. он хранит только одно изображение,
    # а нам нужно много скриншотов программы

    def __str__(self):
        return self.title



class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profiles', on_delete=models.CASCADE, verbose_name='Пользователь')
    information = models.TextField(blank=True, verbose_name='О себе')
    city = models.CharField(max_length=30, blank=True, verbose_name='Город')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Телефон')
    avatar = models.ImageField(blank=True, verbose_name='Аватар', upload_to='user_avatars/')


class Comments(models.Model):
    user_name = models.CharField(max_length=20, verbose_name='Имя пользователя', default=None, null=True)
    text = models.TextField(verbose_name='Комментарий')
    app = models.ForeignKey('App', verbose_name='Приложение', default=None, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name='Пользователь', default=None, null=True, on_delete=models.CASCADE)

    def short_text(self):
        if len(self.text) > 15:

            return self.text[:15] + '...'
        else:
            return self.text

    short_text.short_description = 'Текст комментария'