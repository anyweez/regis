import face.models.models as regis
import face.util.exceptions as exception
import face.util as util
import random

class Concierge(object):
    # Activates a prepared question set for a user.  It essentially
    # looks for a premade question set and transitions all of the
    # questions to their user ID.  Checks to make sure that the
    # assignment was done properly afterwards (although there is
    # likely still a TOCTOU bug here).
    #
    # Also activates the first question for the user.
    def activate_question_set(self, ruser):
        searching = True
        target_set = None
        # Search until you can grab a question set.
        while searching:
            open_sets = regis.PendingQuestionSet.objects.filter(reserved_by=None)
        
            if len(open_sets) > 0:
                target_set = random.choice(open_sets)
        
                target_set.reserved_by = ruser
                target_set.save()
        
                try:
                    regis.PendingQuestionSet.objects.get(reserved_by=ruser)
                    # Found a keeper
                    searching = False
                except regis.PendingQuestionSet.DoesNotExist:
                    pass
            # If there are no question sets available, throw an exception.  Nothin
            # we can do until more are generated.
            else:
                raise exception.NoQuestionSetReadyException(ruser)
            # The question set has been chosen.  Activate it for the user.
            questions = target_set.questions_set.all()
            for question in questions:
                question.uid = ruser
                question.save()
                
            qm = util.QuestionManager()
            qm.activate_next(ruser)