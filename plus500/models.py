from django.db import models

# Create your models here.
class Plus500(models.Model):
    url_from = models.CharField(max_length=250, blank=True)
    url_to = models.CharField(max_length=250, blank=True)
    ahrefs_rank = models.IntegerField()
    domain_rating = models.IntegerField()
    title = models.CharField(max_length=900, blank=True)


    def __str__(self):
        return self.url_from
