from django.core.management.base import BaseCommand, CommandError
import face.offline.QuestionSolver as qs
import face.models.models as regis

class Command(BaseCommand):
    args = 'none'
    help = 'Solves all of the questions that havent been solved for all users.'

    # Checks to see if there are any retired questions for this template
    # We want to copy some of their state if so.
    def find_ancestor(self, question):
        try:
            ancestors = regis.Question.objects.filter(
                    status='retired',
                    template=question.template,
                    user=question.user).order_by('-id')
            return ancestors[0]
        except regis.Question.DoesNotExist:
            return None

    def handle(self, *args, **options):
        solver = qs.QuestionSolver()
        qlist = self.get_question_list()

        missing_solvers = []
        solved_count = 0
        for q in qlist:
            try:
                results = solver.solve(q)
                # If the problem is community-based it does not have to be solved.
                if results is None:
                    continue
            
                for val, msg in results['correct']:
                    ans = regis.Answer(question=q, correct=True, value=val, message=msg)
                    ans.save()
                
                for val, msg in results['mistakes']:
                    ans = regis.Answer(question=q, correct=False, value=val, message=msg)
                    ans.save()
            
                ancestor = self.find_ancestor(q)
                if ancestor is not None:
                    q.order = ancestor.order
                    if ancestor.time_released is not None:
                        q.status = 'released'
                        q.time_released = ancestor.time_released
                    else:
                        q.status = 'ready'
                    q.save()
                else:
                    q.status = 'ready'
                    q.save()
            
                solved_count += 1
            except ImportError:
                missing_solvers.append(q.template.id)
            except Exception as e:
                print 'Exception thrown while running solver %s:' % q.template.solver_name
                print e
                continue
        
        print 'Solved %d new problems.' % solved_count
        print 'Missing solvers for %d templates.' % len(list(set(missing_solvers)))

    def get_question_list(self):
        all_q = regis.Question.objects.exclude(status='retired')
        keepers = []
      
        for q in all_q:
            num_ans = regis.Answer.objects.filter(question=q)

            if len(num_ans) == 0:
                keepers.append(q)
              
        return keepers
