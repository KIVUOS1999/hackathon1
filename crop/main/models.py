from django.db import models

class Desease(models.Model):
    desease_name = models.CharField(max_length = 200)
    desease_display_image = models.ImageField(null = True, blank = True)
    desease_description = models.TextField()
    desease_remidies = models.TextField()


    def __str__(self):
        return self.desease_name