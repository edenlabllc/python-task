from django.db import models

class Repository(models.Model):
    '''
    Repository model
    '''

    id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=255)
    html_url = models.URLField()
    description = models.TextField(null=True, blank=True)
    stargazers_count = models.DecimalField(max_digits=5, decimal_places=0)
    lang = models.CharField(max_length=255)

    class Meta:
        db_table = 'repository'
