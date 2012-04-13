from django.core.management.base import BaseCommand
import face.offline.QuestionSolver as qs
import face.models.models as regis

class Command(BaseCommand):
    args = 'none'
    help = 'Parses all of the questions that havent been parsed for all users.'

    def handle(self, *args, **options):
        solver = qs.QuestionSolver()
        q = regis.QuestionInstance.objects.get(id=args[0])

        print '**********'
        print 'QUESTION:'
        print '**********'
        print q.text
        print ''
        print '**********'
        print 'SOLUTION:'
        print '**********'
        results = solver.solve(q)
        for i, result in enumerate(results['correct']):
            print '(%d) %s' % (i+1, result[0])
        print ''
        print 'Solved!'