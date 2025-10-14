from django.db import models

# Create your models here.
class TypeArticle(models.Model):
    type = models.CharField(max_length=15)

class Article(models.Model):
    type = models.ForeignKey(TypeArticle, on_delete=models.CASCADE) #Тип статьи
    title = models.CharField(max_length=40) #Наименование статьи
    description = models.CharField(max_length=999) #Описание статьи
    date = models.DateField() #Дата публикации
    image = models.ImageField() #Изображение
    source = models.CharField(max_length=50) #Ссылка на источник