from django.core.management.base import BaseCommand, CommandError
import face.offline.QuestionSolver as qs
import face.models.models as regis

import os

class Command(BaseCommand):
    args = 'none'
    help = 'Lists all of the solvers that aren\'t readily available but are listed for templates.'

    def handle(self, *args, **options):
        templates = regis.QuestionTemplate.objects.all()
        needed_names = list(set([template.solver_name for template in templates]))
        
        have_names = [f.split('Solver')[0] for f in os.listdir('offline/Solvers') if f.endswith('.py')]
        
        for solver in (set(needed_names) - set(have_names)):
            print '  %s' % solver
        

# Get all questions that are inactive.

# For each question, run the solver with the parameters list from the
# database.

# Store the output in the database and flip the READY flag for the
# question to true.
