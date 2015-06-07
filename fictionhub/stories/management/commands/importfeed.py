from django.core.management.base import NoArgsCommand, make_option
from stories.models import Story

class Command(NoArgsCommand):

    help = "Whatever you want to print here"

    option_list = NoArgsCommand.option_list + (
        make_option('--verbose', action='store_true'),
    )

    def handle_noargs(self, **options):
        print(Story.objects.all())
