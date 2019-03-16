from django.db import models
from django.urls import reverse # Used to generate URLs by reversing the URL patterns
from django.utils.text import slugify

class BookCategory(models.Model):
    """Model representing a book category"""
    name = models.CharField(max_length=200, null=True, blank=True, help_text='Enter a book category (e.g. Django)')
    slug = models.SlugField()

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        """String for representing the Model object."""
        return self.name
    
    def set_slug(self):
        # If the slug is already set, stop here.
        if self.slug:
            return
        
        base_slug = slugify(self.title)
        slug = base_slug
        n = 0

        while BookCategory.objects.filter(slug=slug).count():
            n += 1
            slug = base_slug + "-" + str(n)
        
        self.slug = slug
    
    def get_absolute_url(self):
        return reverse("category-detail", args=[str(self.slug)])


class Book(models.Model):
    """Model representing a book (but not a specific copy of a book)."""

    title = models.CharField(max_length=100)
    # author = models.ForeignKey('Author', on_delete=models.CASCADE, blank=True)
    author = models.CharField(max_length=255, default="Unknown Author")
    book_description = models.TextField(max_length=1000, help_text='Enter a brief description')
    book_url = models.URLField(default="")
    added_on = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField()
    book_categories = models.ManyToManyField(BookCategory)
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
        """Create a string for BookCategory. This is required to display genre in Admin."""
        return ', '.join(book_category.name for book_category in self.book_category.all()[:3])
    
    display_book_category.short_description = "Category"

    def __str__(self):
        """String for representing the Model object."""
        return self.title
    
    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse("book-detail", kwargs={"slug": self.slug})
