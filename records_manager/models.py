from django.db import models

# Create your models here.


class child(models.Model):
    user_id = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    parent_contact_number = models.IntegerField()
    parent_email = models.EmailField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = "child"


class kid_meal(models.Model):
    kid_id = models.ForeignKey('child', on_delete=models.CASCADE)
    image_url = models.CharField(max_length=200)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    food_group = models.CharField(max_length=50)

    class Meta:
        db_table = "kid_meal"

    def __str__(self):
        return self.meal_id

    class Meta:
        db_table = "kid_meal"
