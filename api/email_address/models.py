from django.db import models

class EmailAddress(models.Model):
  username=models.CharField(max_length=42)
  date=models.DateTimeField(null=True)
  REMOTE_ADDR=models.IPAddressField(blank=True)
  def __uni__(self):
    return self.address
