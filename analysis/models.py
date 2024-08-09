from django.db import models

class FinancialData(models.Model):
    csv_file = models.FileField(upload_to='csvs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.csv_file.name
