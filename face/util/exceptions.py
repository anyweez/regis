
# Thrown when a user doesn't have an available question.
class NoQuestionReadyException(Exception):
    def __init__(self, user):
        self.user = user
        
    def __str__(self):
        return 'No question ready for user %s' % self.user.username
    
class UnauthorizedAttemptException(Exception):
    def __init__(self, user, qid):
        self.user = user
        self.qid = qid
        
    def __str__(self):
        return '%s made an authorized guess attempt on question ID #%d' % (self.user.username, self.qid)
    
