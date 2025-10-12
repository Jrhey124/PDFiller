from django.db import models

class DocumentTemplate(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    html_template = models.TextField()  # Store the actual HTML content

    def __str__(self):
        return self.name
