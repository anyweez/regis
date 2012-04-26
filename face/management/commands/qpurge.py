from django.core.management.base import BaseCommand, CommandError
import face.offline.QuestionSolver as qs
import face.models.models as regis

# TODO: This is out of date and no longer works.  Still seems potentially
# useful but will need to be revamped.
class Command(BaseCommand):
    args = 'none'
    help = 'Purges questions and question sets for users that no longer exist.'

    def handle(self, *args, **options):
        # Remove questions that don't have existing question sets.

        qsets = regis.QuestionSet.objects.all()
        sets_deleted = 0
        
        print 'Examining %d question sets...' % len(qsets)
        # Remove question sets whose owners no longer exist.
        for qset in qsets:
            try:
                u = qset.reserved_by
            except regis.User.DoesNotExist:
                qset.delete()
                sets_deleted += 1
        print '%d removed due to missing owner.' % sets_deleted
        
        questions = regis.Question.objects.all()
        questions_deleted = 0
        print 'Examining %d questions...' % len(questions)
        for question in questions:
            try:
                q = question.questionset.all()
                if len(q) == 0:
                    question.delete()
                    questions_deleted += 1
            except regis.QuestionSet.DoesNotExist:
                question.delete()
                questions_deleted += 1
        print '%d removed due to missing owner.' % questions_deleted