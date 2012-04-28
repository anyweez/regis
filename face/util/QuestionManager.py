from django.db.models import Max
from django.template import Context
from django.template.loader import get_template

import face.models.models as models
import face.util.exceptions as exception
import face.modules.providers as providers
import datetime, random

class QuestionManager(object):
    # Makes sure that the user has bindings to all ready templates. This
    # method will create a UserQuestion linking the provided user with
    # each template marked as 'ready.'
    def bind_questions(self, user):
        all_t = models.QuestionTemplate.objects.filter(status='ready')

        # If there are no templates then our work here is done.  This is a
        # fairly useless situation to be in but shouldn't crash.
        if len(all_t) is 0:
            return False
        
        # Put the template at the end of the queue for each user by default.
        # The personalization process can update this later.        
        starting_order = models.UserQuestion.objects.filter(user=user).aggregate(Max('order'))
        if starting_order['order__max'] is None:
            next_order = 0
        else:
            next_order = starting_order['order__max']
        
        for template in all_t:
            if models.UserQuestion.objects.filter(template=template).count() is 0:
                inst = models.QuestionInstance.objects.filter(template=template)
                models.UserQuestion(user=user, 
                    template=template, 
                    order=next_order,
                    status='ready',
                    instance=random.choice(inst)).save()
                next_order += 1
        
    # Internal use only.  This is a predicate that determines whether a new  
    # question should be released for the specifed user.
    #
    # This function can be modularized later if we want to.
    def _check_release(self, user):
        questions = models.UserQuestion.objects.filter(user=user, status='released').order_by('-released')
        if len(questions) > 0:
            return (datetime.datetime.now() - questions[0].released) > datetime.timedelta(days=2)
        # If no questions have been unlocked, unlock one.
        else:
            return True
    
    # Activates the next question for the user.  If check_release == True
    # then the system will check to see whether a question should be unlocked
    # before doing it.
    def activate_next(self, user, check_release=True):
        # Release a question if either (a) _check_release says we should or
        # (b) check_release specifies that we shouldn't care.
        if not check_release or (check_release and self._check_release(user)):
            # Raises a NoQuestionReadyException if there are no questions 
            # left to unlock.
            try:
                target_order = models.UserQuestion.objects.filter(user=user, status='ready').order_by('order')
            except models.UserQuestion.DoesNotExist:
                raise exception.NoQuestionReadyException(user)

            # If there are no questions to unlock then return false.
            if len(target_order):
                question = target_order[0]
            else:
                return False
            
            # If there is a question to be released, release it.
            question.released = datetime.datetime.now()
            question.visible = True
            question.answerable = True
            question.status = 'released'
            question.save()

            return True
        else:
            return False
    
    # Get all of the questions for the specified user that are either 'released'
    # or 'solved.'  Those are the only two status's that should ever be visible.  
    def get_questions(self, user, json=True, include_hints=True):
        provider = providers.LocalQuestionProvider
        questions = provider.get_questions(user.id)
        output = []
        # Render the HTML template for the question before returning it.
        for question in questions:
            question['html'] = get_template('question.tpl').render(Context({'question': question}))
            if include_hints:
                hints = provider.get_hints(user.id, question['question_id'])
                question['html'] += get_template('hints-scrap.tpl').render(Context({'question': question}))
            if question['gradable']:
                grading_package = provider.get_grading_package(user.id, question['question_id'], correct=True, limit=None, include_graded=False)
                score_options = grading_package['score_options']
                given_answers = grading_package['given_answers']
                peer_attempts = grading_package['peer_attempts']
                grading_html = get_template('grading.tpl').render(Context({
                    'question': question, 
                    'peer_attempts' : peer_attempts, 
                    'given_answers' : given_answers,
                    'score_options' : score_options,
                }))

                question['html'] +=  grading_html
        return questions
    
    # Returns a tuple (bool, str) that states whether the answer
    # is correct and an accompanying message.
    def check_question(self, question, answer):
        answers = models.Answer.objects.filter(question=question)
        
        correct = False
        msg = "Sorry, that's not correct.  Keep trying!" # Default incorrect message.
        for ans in answers:
            # TODO: This should use the solver script's validate() method instead of a simple text comparison.
            if ans.value.strip() == answer.strip():
                msg = ans.message
                if ans.correct:
                    correct = True
                
        return (correct, msg)

    def format_hints_html(self, hints):
        return get_template('hints.tpl').render(Context({'hints': hints}))
