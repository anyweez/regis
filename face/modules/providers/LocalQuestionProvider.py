import face.models.models as models
import face.util.QuestionManager as qm
import Provider as provider

import datetime

## Get all questions that are stored in the system.  This does
## not include any user permission filtering, which should be
## done outside of the data provider.
##
## Note: this method should always return a list of JSON objects.
def get_questions(user_id):
    # Get all of questions for the specified user.
    try:
        user = models.User.objects.get(id=user_id)
    except models.User.DoesNotExist:
        raise provider.ProviderException('The specified user does not exist.')
    
    db_questions = models.UserQuestion.objects.filter(user=user, status__in=['released', 'solved'])
    
    for i, db_question in enumerate(db_questions):
        db_questions[i].time_released = db_question.released.isoformat()
        
    return [d.jsonify() for d in db_questions]

## Get a single question as specified by the question_id.
##
## Note: this method should always return a single JSON object
## or raise an exception.
def get_question(question_id):
    try:
        question = models.QuestionInstance.objects.get(id=question_id)
        return question
    except models.QuestionInstance.DoesNotExist:
        raise provider.ProviderException('A question with an ID of %s does not exist.' % question_id)


def create_new_question(user_id, question_text, correct_answer):
    try:
        owner = models.User.objects.get(id=user_id)
    except models.User.DoesNotExist:
        raise provider.ProviderException('The specified user does not exist.')
    type = 'peer'
    text = question_text 
    
    live = True 
    status = 'waiting'
    
    template = models.QuestionTemplate(owner=owner, type=type, text=text, live=live, status=status)
#    #TODO(cartland): Bug with template saving
#    #Field 'community' doesn't have a default value
    template.save()
#    qm.process_template(template, owner)
#    question = models.UserQuestion.objects.get(template=template, user=owner)
#    answer = models.Answer(question__template=template, correct=True, value=correct_answer, message=None)
#    answer.save()

    #TODO(cartland): What should we return? I think we need to return
    # a template. It makes sense for the owner of a question to get
    # a tempalte of that question, not the question itself.
    # For an MVP it is fine to return a question (UserQuestion in the backend).
    return "Template created (process incomplete)"




## Submits an attempt for the provided question.  Should return
## JSON object describing attempt.  This is also a good place to
## store the attempt if desired. 
##
## Response: {
##   correct : true / false
## }
def submit_attempt(question_id, user_id, attempt):
    # Get question
    # Get user
    # Get userquestion.instance
    # check question against answers to instance
    
    question = get_question(question_id)
    user = provider.getUserProvider().get_user(user_id)
    
    user_q = models.UserQuestion.objects.exclude(status='retired').get(instance=question, user=user)
    
    manager = qm.QuestionManager()
    correct, reason = manager.check_question(question, attempt)
    
    guess = models.Guess(
        user = user,
        question = user_q,
        value = attempt,
        correct = correct,
        time_guessed=datetime.datetime.now()
    )
    guess.save()

    if correct:
        user_q.gradable = True
        user_q.save()

    return guess

# question_id is a template id.
def submit_grade_for_attempt(author_id, attempt_id, score, messages=None):
    try:
        author = models.User.objects.get(id=author_id)
    except models.User.DoesNotExist:
        raise provider.ProviderException('The specified user does not exist.')

    try:
        attempt = models.Guess.objects.get(id=attempt_id)
    except models.User.DoesNotExist:
        raise provider.ProviderException('The specified user does not exist.')

    try:
        evaluation = models.GuessEvaluation.objects.get(attempt=attempt, author=author, guesser=attempt.user)
        evaluation.score = score
    except models.GuessEvaluation.DoesNotExist:
        evaluation = models.GuessEvaluation(attempt=attempt, author=author, guesser=attempt.user, score=score)
    except models.GuessEvaluation.MultipleObjectsReturned:
        models.GuessEvaluation.objects.delete(attempt=attempt, author=author, guesser=attempt.user)
        evaluation = models.GuessEvaluation(attempt=attempt, author=author, guesser=attempt.user, score=score)
        
    evaluation.save()
    return evaluation.jsonify()

# question_id is a template id. TODO (cartland) make this real
def __get_attempts_to_grade(user_id, question_id, limit=None, include_graded=None):
    if include_graded is None:
        include_graded = False
    fields = [
            'attempt_id',
            'question_id',
            'text']
    attempts = models.Guess.objects.filter(question__id=question_id).order_by('value')
    jattempts = [a.jsonify() for a in attempts]
    output = []
    for j in jattempts:
        if limit is not None and len(output) == limit:
            return output
        values = {}
        for k, v in j.items():
            if k in fields:
                values[k] = v
        try:
          evaluation = models.GuessEvaluation.objects.get(author__id=user_id, attempt__id=j['attempt_id'])
          values['evaluation'] = evaluation.jsonify()
        except models.GuessEvaluation.DoesNotExist:
          values['evaluation'] = None
        if values['evaluation'] is None or include_graded:
          output.append(values)
    return output


# question_id is a template id
def __get_given_answers(user_id, question_id, correct=None):
    user_q = models.UserQuestion.objects.get(user=user_id, template__id=question_id)

    if correct is None:
        answers = models.Answer.objects.filter(question__template__id=question_id, question__id=user_q.instance.id)
    else:
        answers = models.Answer.objects.filter(question__template__id=question_id, question__id=user_q.instance.id, correct=correct)
    return [a.jsonify() for a in answers]

def get_grading_package(user_id, question_id, correct=None, limit=None, include_graded=None):
    package = {}
    package['user_id'] = user_id
    package['question_id'] = question_id
    package['score_options'] = [[0, "Incorrect"], [1, "On topic"], [2, "Demonstrates some understanding"], [3, "Good answer"], [4, "Best answer"]]
    package['given_answers'] = __get_given_answers(user_id, question_id, correct=correct)
    package['peer_attempts'] = __get_attempts_to_grade(user_id, question_id, limit=limit, include_graded=include_graded)
    return package



def submit_hint(user_id, question_id, hint_text):
    question_template = models.QuestionTemplate.objects.get(id=question_id)
    user = provider.getUserProvider().get_user(user_id)
    
    hint = models.Hint(template=question_template, author=user, text=hint_text)
    hint.save()
    return hint.jsonify()


def get_hints(user_id, question_id):
    hints = models.Hint.objects.filter(template__id=question_id)
    return [h.jsonify() for h in hints]
