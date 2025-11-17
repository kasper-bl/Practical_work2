from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator

class CustomerUser(AbstractUser):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название категории")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class Application(models.Model):

    STATUS_CHOICES = (
        ('new', 'Новая'),
        ('accepted', 'Принято в работу'),
        ('done', 'Выполнено')
    )

    title = models.CharField(verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Категория')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    comment = models.TextField(blank=True, verbose_name="Комментарий")
    img_Application = models.ImageField(upload_to='images/', verbose_name='Изображение', validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'bmp'])],)
    status = models.CharField(verbose_name='статус', choices = STATUS_CHOICES, default='new',)
    user = models.ForeignKey(CustomerUser, on_delete=models.CASCADE, verbose_name='Пользователь')

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        ordering = ['-created_at']