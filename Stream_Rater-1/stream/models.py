from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=32, unique=True)
    image = models.CharField(max_length=128, default=None)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Streamer(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=32)
    title = models.CharField(max_length=128,default=None)
    image = models.CharField(max_length =128,default=None)
    views = models.IntegerField(default=0)
    rating = models.FloatField(default=0, max_length=3)

    class Meta:
        verbose_name_plural = 'Streamers'

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username


# Main comments have rating and relate to a user with a one-to-many relationship
class Comment(models.Model):
    user_name = models.CharField(default="Unknown", max_length=32)
    streamer = models.ForeignKey(Streamer, related_name="comments", on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    text = models.TextField(blank=True)
    rating = models.PositiveIntegerField(null=False)
    # An array of sub comments could work here too, wouldn't require a query for view

    class Meta:
        verbose_name_plural = 'Comments'

    def __str__(self):
        return str(self.user_name + "/"
                + self.date.__str__() + "/"
                + self.rating.__str__() + "\n")

    def get_id(self):
        return self.id


# SubComments don't have rating and relate to a Comment with a one-to-many relationship
class SubComment(models.Model):
    user_name = models.CharField(default="Unknown", max_length=32)
    father_comment = models.ForeignKey(Comment, related_name="sub_comments", on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    text = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Sub_Comments'

    def __str__(self):
        return str(self.user_name + "\n"
                   + self.date.__str__() + "\n"
                   + self.text)
