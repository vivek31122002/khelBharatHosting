import json
from django.core.management.base import BaseCommand
from app.models import Rank, Rank2

class Command(BaseCommand):
    help = 'Load ranks from a JSON file'

    def handle(self, *args, **kwargs):
        with open('data/MOCK_DATA.json') as file:
            data = json.load(file)
            for item in data:
                Rank2.objects.create(
                    rank=0,
                    name=item['Name'],
                    points=item['Points'],
                    country=item['Country'],
                )
        # with open('data/MOCK_DATA_DVG.json') as file:
        #     data = json.load(file)
        #     for item in data:
        #         Rank.objects.create(
        #             rank=item['Rank'],
        #             name=item['Name'],
        #             points=item['Points'],
        #             district=item['District']
        #         )
        # with open('data/MOCK_DATA_HOS.json') as file:
        #     data = json.load(file)
        #     for item in data:
        #         Rank.objects.create(
        #             rank=item['Rank'],
        #             name=item['Name'],
        #             points=item['Points'],
        #             district=item['District']
        #         )
        self.stdout.write(self.style.SUCCESS('Successfully loaded ranks'))
