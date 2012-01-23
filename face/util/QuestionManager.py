from django.db.models import Min, Max

import face.models.models as regis
import face.util.exceptions as exception
import datetime

class QuestionManager(object):
    # Activates the next question for the user.
    def activate_next(self, user):
        target_order = regis.Question.objects.filter(uid=user, status='ready').aggregate(Min('order'))

        # If there is a question to be released, release it.
        try:
            q = regis.Question.objects.get(uid=user, order=target_order['order__min'])
        
            q.time_released = datetime.datetime.now()
            q.status = 'released'
            q.save()
        except regis.Question.DoesNotExist:
            raise exception.NoQuestionReadyException(user)
        
    # Gets the most recently available question.  If multiple questions are available
    # then it displays the question with the lowest ORDER value.
    def get_current_question(self, user):
        target_order = regis.Question.objects.filter(uid=user, status='released').aggregate(Max('order'))
        q = regis.Question.objects.filter(uid=user, order=target_order['order__max'])

        try:
            return q[0]
        except:
            raise exception.NoQuestionReadyException(user)
    
    def time_until_next(self, user):
        nextq = self.get_current_question(user)
        time_expires = nextq.time_released + datetime.timedelta(days=1)
        
        return (time_expires - datetime.datetime.now())
        
    # Returns a tuple (bool, str) that states whether the answer
    # is correct and an accompanying message.
    def check_question(self, question, answer):
        answers = regis.Answer.objects.filter(qid=question)
        
        correct = False
        msg = 'Sorry, try again.' # Default incorrect message.
        for ans in answers:
            if ans.value.strip() == answer.strip():
                msg = ans.message
                if ans.correct:
                    correct = True
                
        return (correct, msg)
