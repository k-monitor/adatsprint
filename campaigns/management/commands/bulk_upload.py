from glob import glob
import os
import re

from django.core.files import File
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand, CommandError

from campaigns.models import Campaign, MP


def get_MP_name_from_pdf(filename):
    filename = os.path.basename(filename)
    match = re.search(r'^(?P<name>[^_]+)_szlaössz_kihagyott\.pdf$', filename)
    assert match is not None
    return match.group('name')

class Command(BaseCommand):
    help = 'Import the PDFs from the given folder(s)'

    def add_arguments(self, parser):
        parser.add_argument('folders', nargs='+')

    def handle(self, *args, **options):
        for folder in options['folders']:
            self.handle_folder(folder)

    def handle_folder(self, folder):
        glob_pattern = os.path.join(folder, '*.pdf')
        self.stdout.write('processing %s...' % folder)
        for filename in glob(glob_pattern):
            self.handle_file(filename)

    def handle_file(self, filename):
        self.stdout.write('Found PDF file %s' % filename)
        campaign = Campaign.objects.first()  # TODO: fix
        basename = os.path.basename(filename)
        
        with open(filename, mode='rb') as pdf_in:
            pdf_file = default_storage.save(basename, File(pdf_in))

        return MP.objects.create(
            name=get_MP_name_from_pdf(filename),
            campaign=campaign,
            pdf_file=pdf_file,
        )
