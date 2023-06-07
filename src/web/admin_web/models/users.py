from django.db import models


class Users(models.Model):
    class Meta:
        db_table = 'users'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Все Пользователи'

    id = models.BigIntegerField(primary_key=True)

    username = models.CharField(max_length=1000, verbose_name='Никнейм')
    fullname = models.CharField(max_length=1000, verbose_name='Имя')
    is_admin = models.BooleanField(default=False, verbose_name="Админ")
    locale = models.CharField(default="en", verbose_name="Язык")

    created_at = models.DateTimeField(default=False, verbose_name="Время создания")

    def __str__(self):
        return f"{self.id} - {self.username}"
