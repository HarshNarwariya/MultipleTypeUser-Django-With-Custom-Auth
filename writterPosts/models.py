from django.db import models
from accounts.models import WritterMore, Writter

# Create your models here.
class Post(models.Model):
    owner = models.ForeignKey(Writter, on_delete=models.CASCADE)
    title = models.CharField(max_length=254, null=True)
