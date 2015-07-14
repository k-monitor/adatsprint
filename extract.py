"""
Extract the campaign data to two CSV files.
"""
import csv
import time

import django
django.setup()
from django.utils import translation

from campaigns.models import MP, MPEvent, Expense

if __name__ == '__main__':
    translation.activate('en-us')
    time_suffix = time.strftime('%Y%m%d-%H%M%S')

    for basename, model, queryset in [
        ('MPs', MP, MP.objects.select_related('campaign')),
        ('events', MPEvent, MPEvent.objects.select_related('MP', 'user')),
        ('expenses', Expense, Expense.objects.select_related('MP')),
    ]:
        filename = '%s-%s.csv' % (basename, time_suffix)
        print('Writing %s...' % filename)

        with open(filename, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(model.as_csv_tuple.header)
            for row in queryset:
                writer.writerow(row.as_csv_tuple())

        print("Done.")
