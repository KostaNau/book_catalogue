from django.db import models
from django.contrib.auth.models import User

from .behaviors import Timestampable
from .behaviors import Isactiveable
from .behaviors import Titleable
from .behaviors import IsVoidable

from . import utils


class Author(Isactiveable, Timestampable, IsVoidable, models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)

    class Meta:
        default_related_name = 'authors'

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

    @property
    def full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)


class Publisher(Titleable, Isactiveable, Timestampable, IsVoidable, models.Model):

    class Meta:
        default_related_name = 'publishers'

    def __str__(self):
        return self.title


class Category(Titleable, Isactiveable, Timestampable, IsVoidable, models.Model):

    class Meta:
        verbose_name_plural = 'Categories'
        default_related_name = 'categories'

    def __str__(self):
        return self.title


class Book(Titleable, Isactiveable, Timestampable, IsVoidable, models.Model):
    original_author = models.CharField(max_length=255, blank=True)
    original_title = models.CharField(max_length=255, blank=True)
    isbn = models.CharField(max_length=255, blank=True)
    author = models.ForeignKey(Author, models.CASCADE, blank=True, null=True)
    category = models.ForeignKey(Category, models.CASCADE, blank=True, null=True)
    publisher = models.ForeignKey(Publisher, models.CASCADE, blank=True, null=True)

    class Meta:
        default_related_name = 'books'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.isbn:
            google_data = utils.get_original_title_and_name(self.isbn)
            if google_data:
                self.original_author = google_data['author']
                self.original_title = google_data['title']
        super().save(*args, **kwargs)


class Bookmark(Isactiveable, Timestampable, IsVoidable, models.Model):
    user = models.ForeignKey(User, models.CASCADE, null=True)
    book = models.ForeignKey(Book, models.CASCADE, null=True)
    in_bookmarks = models.BooleanField(default=False)

    class Meta:
        default_related_name = 'bookmarks'

    def __str__(self):
        return "{} in bookmark".format(self.book.title)

