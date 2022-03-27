from django.db import models


# model for child table in the database to store the information of the kid of the current user
class child(models.Model):
    user_id = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    parent_contact_number = models.CharField(max_length=10)
    parent_email = models.EmailField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = "child"


#  model for meal table in the database to store the information of the meal of the current kid
class kid_meal(models.Model):
    kid_id = models.ForeignKey('child', on_delete=models.CASCADE)
    image_url = models.CharField(max_length=500)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    food_group = models.CharField(max_length=50)

    class Meta:
        db_table = "kid_meal"

    def __str__(self):
        return "meal for {} | {} ".format(self.kid_id.name, self.food_group)
