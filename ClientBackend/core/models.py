from django.db import models

# Create your models here.


class Order(models.Model):
    id = models.IntegerField(primary_key=True)
    number = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    expected_at = models.DateTimeField()

    def __str__(self):
        return f"Order {self.number}"
