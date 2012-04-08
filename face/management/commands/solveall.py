from django.core.management.base import BaseCommand
import face.offline.QuestionSolver as qs
import face.models.models as models

class Command(BaseCommand):
    args = 'none'
    help = 'Solves all of the questions that havent been solved for all users.'

    def handle(self, *args, **options):
        solver = qs.QuestionSolver()
        questions = models.QuestionInstance.objects.all()
        
        missing_solvers = []
        solved_count = 0
        for question in questions:
            num_answers = models.Answer.objects.filter(question=question).count()

            if num_answers > 0:
                continue

            try:
                results = solver.solve(question)
            
                for val, msg in results['correct']:
                    ans = models.Answer(question=question, correct=True, value=val, message=msg)
                    ans.save()
                
                for val, msg in results['mistakes']:
                    ans = models.Answer(question=question, correct=False, value=val, message=msg)
                    ans.save()
            
                question.status = 'ready'
                question.save()
            
                solved_count += 1
            except ImportError:
                missing_solvers.append(question.template.id)
            except Exception as e:
                print 'Exception thrown while running solver %s:' % question.template.solver_name
                print e
                continue
            
        # All peer templates are ready.
        templates = models.QuestionTemplate.objects.filter(type='peer')
        for template in templates:
            template.status = 'ready'
            template.save()
        
        # Change the status of pending question templates if all of their 
        # instances have been solved.
        print 'Activating templates...'
        templates = models.QuestionTemplate.objects.filter(type='auto', status='pending')
        num_activated = 0
        for template in templates:
            instances = models.QuestionInstance.objects.filter(template=template)
            unsolved = [instance for instance in instances if models.Answer.objects.filter(question=instance).count() == 0]
            if len(unsolved) is 0:
                num_activated += 1
                template.status = 'ready'
                template.save()
        print 'Solved %d new problems.' % solved_count
        print 'Activated %d new templates.' % num_activated
        print 'Missing solvers for %d templates.' % len(list(set(missing_solvers)))