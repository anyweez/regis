
# Computes a bunch of statistics for the user provided in the constructor.
# It computes them lazily and stores the answer in case it's needed more
# than once.
class UserStats(object):
    def __init__(self, user):
        self.user = user