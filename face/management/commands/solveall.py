from django.core.management.base import BaseCommand, CommandError
import face.offline.QuestionSolver as qs
import face.models.models as regis

class Command(BaseCommand):
    args = 'none'
    help = 'Parses all of the questions that havent been parsed for all users.'

    def handle(self, *args, **options):
        solver = qs.QuestionSolver()
        qlist = self.get_question_list()

        solved_count = 0
        for q in qlist:
            try:
                results = solver.solve(q)
            
                for val, msg in results['correct']:
                    ans = regis.Answer(qid=q, correct=True, value=val, message=msg)
                    ans.save()
                
                for val, msg in results['mistakes']:
                    ans = regis.Answer(qid=q, correct=False, value=val, message=msg)
                    ans.save()
            
                q.status = 'ready'
                q.save()
            
                solved_count += 1
            except Exception as e:
                print '[ERROR] Error solving problem #%d for user #%d.' % (q.id, q.uid.id)
                print e
            
        print 'Solved %d new problems.' % solved_count
      
    def get_question_list(self):
        all_q = regis.Question.objects.all()
        keepers = []
      
        for q in all_q:
            num_ans = regis.Answer.objects.filter(qid__exact=q.id)

            if len(num_ans) == 0:
                keepers.append(q)
              
        return keepers

# Get all questions that are inactive.

# For each question, run the solver with the parameters list from the
# database.

# Store the output in the database and flip the READY flag for the
# question to true.
