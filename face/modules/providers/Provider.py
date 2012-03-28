import LocalQuestionProvider, CourseSharingQuestionProvider
import LocalUserProvider


class ProviderException(object):
    pass

## This should be made more dynamic and flexible.  Essentially it just
## needs to pull the QuestionProvider out of persistent storage (DB?)
## and return the appropriate provider type.
## TODO: Make {Question|User}Providers dynamic.
def getQuestionProvider():
    return CourseSharingQuestionProvider
#    return LocalQuestionProvider

def getUserProvider():
    return LocalUserProvider