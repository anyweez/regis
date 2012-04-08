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
        
    return db_questions

## Get a single question as specified by the question_id.
##
## Note: this method should always return a single JSON object
## or raise an exception.
#def get_question(question_id):
#    try:
#        question = models.Question.objects.get(id=question_id)
#        return json.dumps(question)
#    except models.Question.DoesNotExist:
#        raise provider.ProviderException('A question with an ID of %s does not exist.' % question_id)

## Submits an attempt for the provided question.  Should return
## JSON object describing attempt.  This is also a good place to
## store the attempt if desired. 
##
## Response: {
##   correct : true / false
## }
def submit_attempt(question_id, user_id, attempt):
    question = get_question(question_id)
    user = provider.getUserProvider().getUser(user_id)
    
    dj_question = models.Question.objects.get(id=question['id'])
    dj_user = models.User.objects.get(id=user['id'])
    
    manager = qm.QuestionManager()
    correct, reason = manager.check_question(question, attempt)
    
    guess = models.Guess(
        user = dj_user,
        question = dj_question,
        value = attempt,
        correct = correct,
        time_guessed=datetime.datetime.now()
    )
    guess.save()

    return {'correct' : correct}
