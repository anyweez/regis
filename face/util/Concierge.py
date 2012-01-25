import face.models.models as regis
import face.util.exceptions as exception
import random

import face.util.QuestionManager as qm

class Concierge(object):
    # Activates a prepared question set for a user.  It essentially
    # looks for a premade question set and transitions all of the
    # questions to their user ID.  Checks to make sure that the
    # assignment was done properly afterwards (although there is
    # likely still a TOCTOU bug here).
    #
    # Also activates the first question for the user.
    def activate_question_set(self, user):
        searching = True
        target_set = None
        print 'Diving into while loop.'
        # Search until you can grab a question set.
        while searching:
            open_sets = regis.QuestionSet.objects.filter(reserved_by=None)
        
            if len(open_sets) > 0:
                print 'Choosing a set...'
                target_set = random.choice(open_sets)
        
                target_set.reserved_by = user
                target_set.save()
        
                try:
                    regis.QuestionSet.objects.get(reserved_by=user)
                    # Found a keeper
                    searching = False
                except regis.QuestionSet.DoesNotExist:
                    pass
            # If there are no question sets available, throw an exception.  Nothing
            # we can do until more are generated.
            else:
                raise exception.NoQuestionSetReadyException(user)
            
            print 'Question set #%d' % target_set.id
            # The question set has been chosen.  Activate it for the user.
            questions = target_set.questions.all()
            for question in questions:
                question.user = user
                question.save()
                
            question_m = qm.QuestionManager()
            question_m.activate_next(user)