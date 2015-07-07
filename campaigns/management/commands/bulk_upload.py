from glob import glob
import os
import re

from django.core.files import File
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand, CommandError

from campaigns.models import Campaign, MP

FILENAME_REGEXPS = [
    r'^(?P<name>.+)_szlaössz_kihagyott\.pdf$',
    r'^(?P<name>.+) kampány elszámolás 2014_kihagyott\.pdf$',
    r'^(?P<name>.+) számlaösszesítő\.pdf$',
    r'^(?P<name>.+) számlaösszesítő_kihagyott\.pdf$',
    r'^(?P<name>.+) szlaössz\.pdf$',
    r'^(?P<name>.+)_számlaösszesítő\.pdf$',
    r'^(?P<name>.+) szlö\.pdf$',
    r'^(?P<name>.+)_szlao\.pdf$',
    r'^(?P<name>.+)_számlaösszesítő_kihagyott\.pdf$',
    r'^(?P<name>.+) szlaö\.pdf$',
    r'^(?P<name>.+) szllö\.pdf$',
    r'^(?P<name>.+) szlaösszesítő\.pdf$',
    r'^(?P<name>.+)_szlao_kihagyott\.pdf$',
    r'^(?P<name>.+) szlö.\.pdf$',
    r'^(?P<name>.+) számlaösszesítők\.pdf$',
    r'^(?P<name>.+) szlao\.pdf$',
    r'^(?P<name>.+) választási elszámolás 2014_kihagyott\.pdf$',
    r'^(?P<name>.+)_számlaösszesítő_hp_kihagyott\.pdf$',
    r'^(?P<name>.+) választási elszámolás 2014\.pdf$',
    r'^(?P<name>.+) választási elszámolás 2014.pdf_2\.pdf$',
    r'^(?P<name>.+) választási elszámolás szamlaosszesito 2014 jav pdf\.pdf$',
    r'^(?P<name>.+) választási elszámolás számlaösszesítő 2014_kihagyott\.pdf$',
    r'^(?P<name>.+) választási elszámolás elszámolás számlaösszesítő 2014_kihagyott\.pdf$',
    r'^(?P<name>.+)_számlaösszesítő_hiánypótlás\.pdf$',
    r'^(?P<name>.+) Sz\.pdf$',
    r'^(?P<name>.+)_kihagyott\.pdf$',
    r'^(?P<name>.+) számlaöszesítő\.pdf$',
    

    # Last resort: assume anything before '.pdf' is the name
    r'^(?P<name>.+)\.pdf$',
]


FOLDER_REGEXPS = [
    r'^Kampanyscan_szamlaosszesito-(?P<name>.+)$',
    r'^(?P<name>.+) Kampány elszámolás 2014 - számlaösszesítők$',
]


def get_MP_name_from_pdf(filename):
    filename = os.path.basename(filename)
    for regexp in FILENAME_REGEXPS:
        match = re.search(regexp, filename, flags=re.I)
        if match is None:
            continue
        return match.group('name')
    assert False, "MP name not found"


def get_campaign_name_from_folder(folder):
    folder = os.path.basename(folder)
    for regexp in FOLDER_REGEXPS:
        match = re.search(regexp, folder, flags=re.I)
        if match is None:
            continue
        return match.group('name')
    assert False, "Campaign name not found"

class Command(BaseCommand):
    help = 'Import the PDFs from the given folder(s)'

    def add_arguments(self, parser):
        parser.add_argument('folders', nargs='+')

    def skip_campaign(self):
        return None

    def handle(self, *args, **options):
        count = 0
        for folder in options['folders']:
            count += self.handle_folder(folder)

        print("%d MP objects inserted" % count)

    def handle_folder(self, folder):
        self.stdout.write('Processing %s...' % folder)
        campaign_name = get_campaign_name_from_folder(folder)
        self.stdout.write('Creating campaign %r' % campaign_name)
        campaign = Campaign.objects.create(name=campaign_name)

        glob_pattern = os.path.join(folder, '*.pdf')
        glob_pattern_upper = os.path.join(folder, '*.PDF')

        count = 0
        for filename in glob(glob_pattern) + glob(glob_pattern_upper):
            self.handle_file(filename, campaign)
            count += 1
        return count

    def handle_file(self, filename, campaign):
        self.stdout.write('Processing PDF file %s' % filename)
        basename = os.path.basename(filename)

        with open(filename, mode='rb') as pdf_in:
            pdf_file = default_storage.save(basename, File(pdf_in))

        return MP.objects.create(
            name=get_MP_name_from_pdf(filename),
            campaign=campaign,
            pdf_file=pdf_file,
        )
