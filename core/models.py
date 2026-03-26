from django.db import models
from django.core.exceptions import ValidationError

class NavbarCategory(models.Model):
    category = models.OneToOneField('products.Category', on_delete=models.CASCADE, related_name='navbar_item', null=True, blank=True)
    position = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['position']
        verbose_name_plural = "Navbar Categories"

    def clean(self):
        # 🔥 Restrict max 5 categories
        if NavbarCategory.objects.count() >= 5 and not self.pk:
            raise ValidationError("You can only add maximum 5 categories!")

    def save(self, *args, **kwargs):
        self.clean()   # call validation
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Navbar - {self.category.name}"
    
class BusinessHour(models.Model):
    day = models.CharField(max_length=50)
    opening_time = models.CharField(max_length=50)
    closing_time = models.CharField(max_length=50)
    is_closed = models.BooleanField(default=False)

    def __str__(self):
        return self.day
    
class SocialMedia(models.Model):
    name = models.CharField(max_length=50)
    icon_class = models.CharField(max_length=100)  # e.g. fab fa-facebook
    url = models.URLField()

    def clean(self):
        if SocialMedia.objects.count() >= 5 and not self.pk:
            raise ValidationError("Maximum 5 social links allowed!")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class Newsletter(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
 
# Note: Category and Product models moved to products.models to avoid duplication


# 🔹 Slider
class Slider(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.TextField()
    image = models.ImageField(upload_to='slider/')

    def __str__(self):
        return self.title


# 🔹 Banner (Ads)
class Banner(models.Model):
    image = models.ImageField(upload_to='banners/')

    def __str__(self):
        return "Banner"


# 🔹 Blog
class Blog(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='blogs/')

    def __str__(self):
        return self.title


# 🔹 Instagram
class InstagramImage(models.Model):
    image = models.ImageField(upload_to='instagram/')
    

#--------------About Model------------------------

class About(models.Model):
    title = models.CharField(max_length=20)
    description = models.TextField()
    image = models.ImageField(upload_to='about/')
    
    def __str__(self):
        return self.title
    
class Service(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.title
    
class Team(models.Model):
    name = models.CharField(max_length=20)
    role = models.CharField(max_length=30)
    description = models.TextField()
    image = models.ImageField(upload_to='team/')
    
    def __str__(self):
        return self.name
    
