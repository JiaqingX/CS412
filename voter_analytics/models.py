from django.db import models
from django.utils.dateparse import parse_date

class Voter(models.Model):
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    street_number = models.CharField(max_length=10)
    street_name = models.CharField(max_length=100)
    apartment_number = models.CharField(max_length=10, blank=True, null=True)
    zip_code = models.CharField(max_length=10, default='00000')  
    date_of_birth = models.DateField()
    date_of_registration = models.DateField()
    party_affiliation = models.CharField(max_length=50)
    precinct_number = models.CharField(max_length=10)
    v20state = models.BooleanField(default=False)
    v21town = models.BooleanField(default=False)
    v21primary = models.BooleanField(default=False)
    v22general = models.BooleanField(default=False)
    v23town = models.BooleanField(default=False)
    voter_score = models.IntegerField()

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.street_name}"

    @staticmethod
    def load_data(file_path):
        import csv

        # Helper function to convert 'TRUE'/'FALSE' to boolean
        def parse_boolean(value):
            return value.strip().upper() == 'TRUE'

        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                Voter.objects.create(
                    last_name=row['Last Name'],
                    first_name=row['First Name'],
                    street_number=row['Residential Address - Street Number'],
                    street_name=row['Residential Address - Street Name'],
                    apartment_number=row.get('Residential Address - Apartment Number', None),
                    zip_code=row.get('Residential Address - Zip Code', '00000'),  
                    date_of_birth=parse_date(row['Date of Birth']),
                    date_of_registration=parse_date(row['Date of Registration']),
                    party_affiliation=row['Party Affiliation'],
                    precinct_number=row['Precinct Number'],
                    v20state=parse_boolean(row['v20state']),
                    v21town=parse_boolean(row['v21town']),
                    v21primary=parse_boolean(row['v21primary']),
                    v22general=parse_boolean(row['v22general']),
                    v23town=parse_boolean(row['v23town']),
                    voter_score=int(row['voter_score']),
                )
