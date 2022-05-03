from django.db import models


# Create your models here.
class Plus500(models.Model):
    url_from = models.CharField(max_length=250)
    ahrefs_rank = models.IntegerField()
    domain_rating = models.IntegerField()

    def __str__(self):
        return self.url_from
