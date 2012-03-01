from django.core.management.base import BaseCommand, CommandError
import face.offline.QuestionSolver as qs
import face.models.models as regis

class Command(BaseCommand):
    args = 'none'
    help = 'Parses all of the questions that havent been parsed for all users.'

    def handle(self, *args, **options):
        solver = qs.QuestionSolver()
        q = regis.Question.objects.get(id=args[0])

        print '**********'
        print 'QUESTION:'
        print '**********'
        print q.text
        print ''
        print '**********'
        print 'SOLUTION:'
        print '**********'
        results = solver.solve(q)
        if results is None:
            print 'Question was provided by community and has no solver.'
            
        for i, result in enumerate(results['correct']):
            print '(%d) %s' % (i+1, result[0])
        print ''
        print 'Solved!'

# Get all questions that are inactive.

# For each question, run the solver with the parameters list from the
# database.

# Store the output in the database and flip the READY flag for the
# question to true.
