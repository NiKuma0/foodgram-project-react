import os
import csv
import json

from django.core.management.base import BaseCommand, CommandError
from recipes.models import IngredientModel

SUPP_EXTENSIONS = {
    '.csv': lambda *args, **kwargs: csv.DictReader(
        *args, **kwargs,
        fieldnames=('name', 'measurement_unit')
    ),
    '.json': json.load
}


class Command(BaseCommand):
    help = 'Write data from file to database (as IngredientModel objects)'

    def add_arguments(self, parser):
        parser.add_argument(
            'file', type=str,
            help='path to file'
        )
        parser.add_argument(
            '--delete', action='store_true',
            help='remove objects as in file'
        )

    def handle(self, delete: bool, file: str = None, *args, **kwargs):
        if not os.path.exists(file) or os.path.isdir(file):
            raise CommandError(
                f'File "{file}" not found or it is directory'
            )
        _, file_ext = os.path.splitext(file)
        if file_ext not in SUPP_EXTENSIONS:
            raise f'Not support extension {file_ext}'
        writer(IngredientModel, file, file_ext, delete)
        print('Done!\n')


def writer(model: IngredientModel, path: str, ext: str, delete=False) -> None:
    with open(path, newline='') as file:
        data = SUPP_EXTENSIONS[ext](file)
        if delete:
            count, _ = model.objects.filter(
                name__in=[fields['name'] for fields in data]
            ).delete()
            return print(f'Deleted {count} objects')
        count = model.objects.count()
        model.objects.bulk_create(
            [model(**fields) for fields in data],
            ignore_conflicts=True
        )
        print(f'Created {model.objects.count() - count} objects')
