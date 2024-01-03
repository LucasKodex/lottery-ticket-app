from django.db import models
from uuid import uuid4
from random import seed, randint, choice

class Generation(models.Model):
    guid = models.UUIDField(unique=True, default=uuid4)
    public_unique_identifier = models.BigAutoField(primary_key=True)
    range_from = models.PositiveSmallIntegerField()
    range_to = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def generateRandomNumbers(
        self,
        quantity: int,
    ):
        seed()
        numbers = list()
        generatedNumbers = set()

        while len(generatedNumbers) < quantity:
            randomInteger = randint(self.range_from, self.range_to)
            generatedNumbers.add(randomInteger)
        
        for generatedNumber in generatedNumbers:
            number = Number()
            number.generation = self.guid
            number.number = generatedNumber
            number.color = Number.randomColorEnum()
            numbers.insert(number)
        
        return numbers

class Number(models.Model):
    COLOR_ENUM = {
        "RED": "Red",
        "BLUE": "Blue",
        "GREEN": "Green",
        "PURPLE": "Purple",
    }

    guid = models.UUIDField(primary_key=True, default=uuid4)
    generation = models.ForeignKey(
        Generation,
        on_delete=models.CASCADE,
        to_field="guid"
    )
    color = models.CharField(max_length=6, choices=COLOR_ENUM)
    number = models.PositiveSmallIntegerField()

    @staticmethod
    def randomColorEnum():
        return choice(list(Number.COLOR_ENUM.keys()))
