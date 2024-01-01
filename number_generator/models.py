from django.db import models

class Generation(models.Model):
    guid = models.UUIDField(primary_key=True)
    public_unique_identifier = models.PositiveIntegerField(unique=True)
    range_from = models.PositiveSmallIntegerField()
    range_to = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField()

class Number(models.Model):
    COLOR_ENUM = {
        "RED": "Red",
        "BLUE": "Blue",
        "GREEN": "Green",
        "PURPLE": "Purple",
    }

    guid = models.UUIDField(primary_key=True)
    generation = models.ForeignKey(Generation, on_delete=models.CASCADE)
    color = models.CharField(max_length=6, choices=COLOR_ENUM)
    number = models.PositiveSmallIntegerField()

