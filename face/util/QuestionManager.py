from django.db.models import Min, Max

import face.models.models as regis
import face.util.exceptions as exception
import datetime

class QuestionManager(object):
    # Activates the next question for the user.
    def activate_next(self, user):
        target_order = regis.Question.objects.filter(user=user, status='ready').aggregate(Min('order'))

        # If there is a question to be released, release it.
        try:
            q = regis.Question.objects.get(user=user, order=target_order['order__min'])
        
            q.time_released = datetime.datetime.now()
            q.status = 'released'
            q.save()
        except regis.Question.DoesNotExist:
            raise exception.NoQuestionReadyException(user)
        
    # Gets the most recently available question.  If multiple questions are available
    # then it displays the question with the lowest ORDER value.
    def get_current_question(self, user):
        try:
            target_order = regis.Question.objects.filter(user=user, status='released').aggregate(Max('order'))
            return regis.Question.objects.get(user=user, status='released', order=target_order['order__max'])
        except regis.Question.DoesNotExist:
            raise exception.NoQuestionReadyException(user)
    
    def time_until_next(self, user):
        nextq = self.get_current_question(user)
        time_expires = nextq.time_released + datetime.timedelta(days=2)

        return (time_expires - datetime.datetime.now())
    
    def current_expired(self):
        return (self.time_until_next().total_seconds() < 0)
    
    # Returns a tuple (bool, str) that states whether the answer
    # is correct and an accompanying message.
    def check_question(self, question, answer):
        answers = regis.Answer.objects.filter(question=question)
        
        correct = False
        msg = 'Sorry, try again.' # Default incorrect message.
        for ans in answers:
            # TODO: This should use the solver script's validate() method instead of a simple text comparison.
            if ans.value.strip() == answer.strip():
                msg = ans.message
                if ans.correct:
                    correct = True
                
        return (correct, msg)
