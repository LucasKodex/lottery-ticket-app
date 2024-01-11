from django.test import TestCase
from django.urls import reverse

from .models import Generation

from unittest import skip

def new_generation(
    quantity = 6,
    range_from = 0,
    range_to = 99,
    rand_seed = None
    ):
    generation = Generation()
    generation.range_from = range_from
    generation.range_to = range_to
    generation.save()
    numbers = generation.generateRandomNumbers(quantity, rand_seed)
    for number in numbers:
        number.save()
    return generation

class GenerationListView(TestCase):
    URL = reverse("number_generator:generation_listing_page")
    
    def test_no_generations(self):
        """
        when there's no generation it should return
        an informative message
        """
        response = self.client.get(self.URL)
        NO_GENERATIONS_MESSAGE = "There's no generations yet"
        self.assertContains(response, NO_GENERATIONS_MESSAGE)
        
    def test_no_generations(self):
        """
        when there generations it shouldn't return
        the no generations message
        """
        new_generation()
        response = self.client.get(self.URL)
        NO_GENERATIONS_MESSAGE = "There's no generations yet"
        self.assertNotContains(response, NO_GENERATIONS_MESSAGE)
    
    def test_get_all_generations(self):
        """
        the page should return every generation made
        """
        generations = list()
        for _ in range(10):
            generation = new_generation()
            generations.append(generation)
        
        response = self.client.get(self.URL)
        response_generations = response.context["generation_list"]
        self.assertEqual(len(generations), len(response_generations))
        for gen in response_generations:
            self.assertTrue(gen in generations)
        for gen in generations:
            self.assertTrue(gen in response_generations)

class GenerationDetailsView(TestCase):
    def get_url(self, *args):
        return reverse("number_generator:generation_detail_page", args=args)

    def test_get_inexistent_generation(self):
        """
        its impossible to get an inexistent generation
        should return a 404 error
        """
        inexistent_puid = 999
        response = self.client.get(self.get_url(inexistent_puid))
        self.assertEqual(response.status_code, 404)

    def test_retrieve_formatted_puid(self):
        """
        page should contain the formatted puid for the generation
        """
        generation = new_generation()
        response = self.client.get(self.get_url(generation.public_unique_identifier))
        response_generation = response.context["generation"]
        formatted_puid = response_generation.get_formatted_puid()
        self.assertContains(response, formatted_puid)

    def test_retrieve_all_generated_numbers(self):
        """
        should return all the generated numbers for that generation
        """
        generation = new_generation()
        generation_numbers = generation.get_numbers_sorted()

        response = self.client.get(self.get_url(generation.public_unique_identifier))
        response_generation = response.context["generation"]
        response_generation_numbers = response_generation.get_numbers_sorted()

        self.assertEqual(len(generation_numbers), len(response_generation_numbers))
        for i in range(len(generation_numbers)):
            gen_number = generation_numbers[i]
            res_number = response_generation_numbers[i]

            self.assertEqual(gen_number.guid, res_number.guid)
            self.assertEqual(gen_number.generation, res_number.generation)
            self.assertEqual(gen_number.color, res_number.color)
            self.assertEqual(gen_number.number, res_number.number)
    
    def test_incrementing_formatted_puid(self):
        """
        formatted public unique identifier should be incremented every generation
        """
        GENERATION_QUANTITY = 11
        for i in range(GENERATION_QUANTITY):
            generation = new_generation()
            response = self.client.get(self.get_url(generation.public_unique_identifier))
            response_generation = response.context["generation"]
            self.assertEqual(generation, response_generation)
            got_formatted_puid = response_generation.get_formatted_puid()
            expected_formatted_puid = f"#{i + 1:06}"
            self.assertEqual(expected_formatted_puid, got_formatted_puid)
    
    def test_incrementing_puid(self):
        """
        public unique identifier should be incremented every generation
        """
        GENERATION_QUANTITY = 11
        for i in range(GENERATION_QUANTITY):
            generation = new_generation()
            response = self.client.get(self.get_url(generation.public_unique_identifier))
            response_generation = response.context["generation"]
            self.assertEqual(generation, response_generation)
            got_puid = response_generation.public_unique_identifier
            expected_puid = i + 1
            self.assertEqual(expected_puid, got_puid)

class GenerateRandomNumberViewBoundaryValueAnalysis(TestCase):
    URL = reverse("number_generator:home_page")

    def test_starting_range_below_zero(self):
        """
        starting range below 0 (zero) shouldn't be possible.
        should render the home page showing the error:
        "The starting range must be a positive integer."
        """
        data = {
            "range_from": -1,
            "range_to": 49,
            "quantity": 6,
        }
        response = self.client.post(self.URL, data)
        self.assertEqual(
            response.status_code,
            200,
            "Response Status Code should be 200 OK."
            + " (The operation wasn't successful but the page is rendered)"
        )
        ERROR_MESSAGE = "The starting range must be a positive integer."
        error_list = list(response.context["error_list"])
        self.assertTrue(ERROR_MESSAGE in error_list)
        self.assertContains(response, ERROR_MESSAGE)

    def test_starting_range_equal_zero(self):
        """
        starting range equal 0 (zero) should be ok.
        should generate the numbers and redirect to
        the generation details page
        """
        data = {
            "range_from": 0,
            "range_to": 49,
            "quantity": 6,
        }
        response = self.client.post(self.URL, data)
        self.assertEqual(
            response.status_code,
            302,
            "Response Status Code should be 302 FOUND."
        )
        self.assertEqual(
            response.get("Location"),
            reverse("number_generator:generation_detail_page", args=(1,)),
            "Should redirect to generation detail page with id 1",
        )

    def test_ending_range_equal_ninety_nine(self):
        """
        ending range equal 99 (ninety nine) should be ok.
        should generate the numbers and redirect to
        the generation details page
        """
        data = {
            "range_from": 50,
            "range_to": 99,
            "quantity": 6,
        }
        response = self.client.post(self.URL, data)
        self.assertEqual(
            response.status_code,
            302,
            "Response Status Code should be 302 FOUND."
        )
        self.assertEqual(
            response.get("Location"),
            reverse("number_generator:generation_detail_page", args=(1,)),
            "Should redirect to generation detail page with id 1",
        )

    def test_ending_range_above_ninety_nine(self):
        """
        ending range above 99 (ninety nine) shouldn't be possible.
        should render the home page showing the error:
        "The ending range must be equal or lower than 99."
        """
        data = {
            "range_from": 50,
            "range_to": 100,
            "quantity": 6,
        }
        response = self.client.post(self.URL, data)
        self.assertEqual(
            response.status_code,
            200,
            "Response Status Code should be 200 OK."
            + " (The operation wasn't successful but the page is rendered)"
        )
        ERROR_MESSAGE = "The ending range must be equal or lower than 99."
        error_list = list(response.context["error_list"])
        self.assertTrue(ERROR_MESSAGE in error_list)
        self.assertContains(response, ERROR_MESSAGE)

    def test_quantity_below_one(self):
        """
        quantity below 1 (one) shouldn't be possible.
        should render the home page showing the error:
        "Quantity must be a positive integer above zero."
        """
        data = {
            "range_from": 0,
            "range_to": 99,
            "quantity": 0,
        }
        response = self.client.post(self.URL, data)
        self.assertEqual(
            response.status_code,
            200,
            "Response Status Code should be 200 OK."
            + " (The operation wasn't successful but the page is rendered)"
        )
        ERROR_MESSAGE = "Quantity must be a positive integer above zero."
        error_list = list(response.context["error_list"])
        self.assertTrue(ERROR_MESSAGE in error_list)
        self.assertContains(response, ERROR_MESSAGE)

    def test_quantity_equal_one(self):
        """
        quantity equal 1 (one) should be ok.
        should generate the numbers and redirect to
        the generation details page
        """
        data = {
            "range_from": 0,
            "range_to": 99,
            "quantity": 1,
        }
        response = self.client.post(self.URL, data)
        self.assertEqual(
            response.status_code,
            302,
            "Response Status Code should be 302 FOUND."
        )
        self.assertEqual(
            response.get("Location"),
            reverse("number_generator:generation_detail_page", args=(1,)),
            "Should redirect to generation detail page with id 1",
        )

    def test_quantity_equal_one_hundred(self):
        """
        quantity equal 100 (one hundred) should be ok.
        should generate the numbers and redirect to
        the generation details page
        """
        data = {
            "range_from": 0,
            "range_to": 99,
            "quantity": 100,
        }
        response = self.client.post(self.URL, data)
        self.assertEqual(
            response.status_code,
            302,
            "Response Status Code should be 302 FOUND."
        )
        self.assertEqual(
            response.get("Location"),
            reverse("number_generator:generation_detail_page", args=(1,)),
            "Should redirect to generation detail page with id 1",
        )

    def test_quantity_above_one_hundred(self):
        """
        quantity above 100 (one hundred) shouldn't be possible.
        should render the home page showing the error:
        "Quantity must be equal or below 100."
        """
        data = {
            "range_from": 0,
            "range_to": 99,
            "quantity": 101,
        }
        response = self.client.post(self.URL, data)
        self.assertEqual(
            response.status_code,
            200,
            "Response Status Code should be 200 OK."
            + " (The operation wasn't successful but the page is rendered)"
        )
        ERROR_MESSAGE = "Quantity must be equal or below 100."
        error_list = list(response.context["error_list"])
        self.assertTrue(ERROR_MESSAGE in error_list)
        self.assertContains(response, ERROR_MESSAGE)

    def test_generate_all_numbers_within_range(self):
        """
        quantity equal the quantity of numbers within the range should be ok.
        should generate the numbers and redirect to
        the generation details page
        """
        data = {
            "range_from": 0,
            "range_to": 19,
            "quantity": 20,
        }
        response = self.client.post(self.URL, data)
        self.assertEqual(
            response.status_code,
            302,
            "Response Status Code should be 302 FOUND."
        )
        self.assertEqual(
            response.get("Location"),
            reverse("number_generator:generation_detail_page", args=(1,)),
            "Should redirect to generation detail page with id 1",
        )

    def test_generate_all_numbers_within_range_plus_one(self):
        """
        quantity equal the quantity of numbers within the range plus one shouldn't be possible.
        should render the home page showing the error:
        "Can't generate more numbers than exists within the specified range."
        """
        data = {
            "range_from": 0,
            "range_to": 19,
            "quantity": 21,
        }
        response = self.client.post(self.URL, data)
        self.assertEqual(
            response.status_code,
            200,
            "Response Status Code should be 200 OK."
            + " (The operation wasn't successful but the page is rendered)"
        )
        ERROR_MESSAGE = "Can not generate more numbers than exists within the specified range."
        error_list = list(response.context["error_list"])
        self.assertTrue(ERROR_MESSAGE in error_list)
        self.assertContains(response, ERROR_MESSAGE)

class GenerateRandomNumberView(TestCase):
    URL = reverse("number_generator:home_page")

    def test_request_multiple_generations(self):
        """
        the first generation identifier starts at number 1, the
        following identifers of future generations are auto incremented.
        the multiple generations should have an identifier in sequence
        that were generated
        """
        data = {
            "range_from": 0,
            "range_to": 99,
            "quantity": 6,
        }
        for i in range(10):
            n = i + 1
            response = self.client.post(self.URL, data)
            self.assertEqual(
                response.status_code,
                302,
                "Response Status Code should be 302 FOUND."
            )
            self.assertEqual(
                response.get("Location"),
                reverse("number_generator:generation_detail_page", args=(n,)),
                f"Should redirect to generation detail page with id {n}",
            )
    
    def test_non_numeric_data(self):
        """
        non numeric data should render the home page showing the error
        "Fields must be integer numbers."
        """
        data = {
            "range_from": "zero",
            "range_to": "ninety-nine",
            "quantity": "six",
        }
        response = self.client.post(self.URL, data)
        self.assertEqual(
            response.status_code,
            200,
            "Response Status Code should be 200 OK."
            + " (The operation wasn't successful but the page is rendered)"
        )
        ERROR_MESSAGE = "Fields must be integer numbers."
        error_list = list(response.context["error_list"])
        self.assertTrue(ERROR_MESSAGE in error_list)
        self.assertContains(response, ERROR_MESSAGE)

    def test_range_from_greater_than_range_to(self):
        """
        ranges input should be order independet and range from greater than range to should be ok.
        should generate the numbers and redirect to
        the generation details page
        """
        data = {
            "range_from": 99,
            "range_to": 0,
            "quantity": 6,
        }
        response = self.client.post(self.URL, data)
        self.assertEqual(
            response.status_code,
            302,
            "Response Status Code should be 302 FOUND."
        )
        self.assertEqual(
            response.get("Location"),
            reverse("number_generator:generation_detail_page", args=(1,)),
            "Should redirect to generation detail page with id 1",
        )

    def test_starting_range_equal_to_ending_range(self):
        """
        starting range equals to ending range means that only
        exists one number that can be generated and its valid
        should generate the number and redirect to
        the generation details page
        """
        data = {
            "range_from": 99,
            "range_to": 99,
            "quantity": 1,
        }
        response = self.client.post(self.URL, data)
        self.assertEqual(
            response.status_code,
            302,
            "Response Status Code should be 302 FOUND."
        )
        self.assertEqual(
            response.get("Location"),
            reverse("number_generator:generation_detail_page", args=(1,)),
            "Should redirect to generation detail page with id 1",
        )
