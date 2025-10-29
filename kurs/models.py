from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=20)
    
    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Article(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'draft'
        PUBLISHED = 'published'
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField(Tag)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.DRAFT)
    timestamp = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title