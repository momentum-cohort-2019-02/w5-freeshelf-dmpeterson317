from django.db import models
from django.urls import reverse # Used to generate URLs by reversing the URL patterns
from django.utils.text import slugify


# class Author(models.Model):

class BookCategory(models.Model):
    """Model representing a book category"""
    name = models.CharField(max_length=100, help_text='Enter a book category (e.g. Django)')

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        """String for representing the Model object."""
        return self.name


class Book(models.Model):
    """Model representing a book (but not a specific copy of a book)."""

    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100, blank=True)
    # author = models.ManyToManyField(Author, help_text='Select the author/authors for this book')
    book_description = models.TextField(max_length=1000, help_text='Enter a brief description')
    book_url = models.URLField(default="")
    added_on = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField()
    book_category = models.CharField(max_length=100, blank=True, help_text='Select a category for this book')
    favorited_count = models.IntegerField(default=0)
    
    def save(self, *args, **kwargs):
        self.set_slug()
        super().save(*args, **kwargs)

    def set_slug(self):
        # If the slug is already set, stop here.
        if self.slug:
            return

        base_slug = slugify(self.title)
        slug = base_slug
        n = 0

        # while we can find a record already in the DB with the slug
        # we're trying to use
        while Book.objects.filter(slug=slug).count():
            n += 1
            slug = base_slug + "-" + str(n)

        self.slug = slug

    class Meta:
        ordering = ['-added_on']

    def display_book_category(self):
        """Create a string for BookCategory. This is required to display genre in Admin.     """
        return ', '.join(book_category.name for book_category in self.book_category.all()[:3])
    
    display_book_category.short_description = "Category"

    def __str__(self):
        """String for representing the Model object."""
        return self.title
    
    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse("book-detail", kwargs={"slug": self.slug})
