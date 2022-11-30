from django.db import models
from django.utils import timezone
from .extensions.utils import jalali_converter


# my manager
class ArticleManager(models.Manager):
    def published(self):
        return self.filter(status='p')


# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100, unique=True)
    status = models.BooleanField(default=True, verbose_name='status')
    position = models.IntegerField(verbose_name='position')

    class meta():
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        ordering = ['position']

    def __str__(self):
        return self.title


class Article(models.Model):
    STATUS_CHOICES = [
        ('d', 'Draft'),
        ('p', 'Publish'),
    ]
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100, unique=True)
    category = models.ManyToManyField(Category, related_name='articles')
    description = models.TextField()
    thumbnail = models.ImageField(upload_to='images')
    publish = models.DateField(default=timezone.now)
    create = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)

    class meta():
        verbose_name = 'article'
        verbose_name_plural = 'articles'
        ordering = ['-publish']

    def __str__(self):
        return self.title

    def jpublish(self):
        return jalali_converter(self.publish)

    jpublish.short_description = 'publish'

    def category_publish(self):
        return self.category.filter(status=True)

    objects = ArticleManager()
