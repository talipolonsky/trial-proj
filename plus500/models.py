from django.db import models

class Plus500(models.Model):
    url_from = models.CharField(max_length=250, blank=True)
    url_to = models.CharField(max_length=250, blank=True)
    ahrefs_rank = models.IntegerField()
    domain_rating = models.IntegerField()
    title = models.CharField(max_length=900, blank=True)
    #category =  models.CharField(max_length=50, blank=True)
    #contact_email = models.EmailField()

    def __str__(self):
        return self.url_from

#class Settings_table(models.Model):
#    id = models.IntegerField()
#    domain_rating = models.IntegerField()
#    title = models.CharField(max_length=900, blank=True)
#    #category =  models.CharField(max_length=50, blank=True)

#    def __str__(self):
#        return self.url_from
