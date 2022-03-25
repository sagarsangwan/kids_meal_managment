from django.db import models

# Create your models here.


class child(models.Model):
    user_id = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    parent_contact_number = models.IntegerField()
    parent_email = models.EmailField()

    class Meta:
        db_table = "child"
