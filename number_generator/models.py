from django.db import models
from uuid import uuid4
from random import seed, randint, choice

class Generation(models.Model):
    guid = models.UUIDField(unique=True, default=uuid4)
    public_unique_identifier = models.BigAutoField(primary_key=True)
    range_from = models.PositiveSmallIntegerField()
    range_to = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def get_formatted_puid(self):
        return "#" + "%06d" % self.public_unique_identifier

    def generateRandomNumbers(
        self,
        quantity: int,
        rand_seed = None,
    ):
        seed(rand_seed)

        generatedNumbers = list()
        availableNumbers = [ x for x in range(self.range_from, self.range_to + 1) ]
        for _ in range(quantity):
            randomIndex = randint(0, len(availableNumbers) - 1)
            drawnNumber = availableNumbers.pop(randomIndex)
            generatedNumbers.append(drawnNumber)

        numbers = list()
        for generatedNumber in generatedNumbers:
            number = Number()
            number.generation = self
            number.number = generatedNumber
            number.color = Number.randomColorEnum()
            numbers.append(number)
        
        return numbers

    def get_numbers(self):
        return Number.objects.all().filter(generation=self.guid)
    
    def get_numbers_sorted(self):
        return self.get_numbers().order_by("number")

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
