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

class Settings_table(models.Model):
    #id - the key of the object
    id = models.IntegerField(primary_key=True)
    #the min values to filter on these fields
    domain_rating = models.IntegerField()
    domain_traffic = models.IntegerField()
    organic_keywords = models.IntegerField()
    referringDomains_backlinks_ratio = models.IntegerField()
    #sorting priorities of the fields:
    domain_rating_priority = models.IntegerField()
    domain_traffic_priority = models.IntegerField()
    organic_keywords_priority = models.IntegerField()
    referringDomains_backlinks_ratio_priority = models.IntegerField()
    #cometitors bolean fields (True if selected, else False):
    avatrae = models.BooleanField(default=False)
    robinhood = models.BooleanField(default=False)
    etoro = models.BooleanField(default=False)
    IG = models.BooleanField(default=False)
    CMC_markets = models.BooleanField(default=False)
    #the email template
    email_template = models.CharField(max_length=10000)
