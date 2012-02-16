import face.models.models as regis
import math

# Computes a bunch of statistics for the user provided in the constructor.
# It computes them lazily and stores the answer in case it's needed more
# than once.
class UserStats(object):
    def __init__(self, user):
        self.user = user
        # Used for caching some info to reduce query volume.
        self.data = {}
        
    def questions_answered(self):
        questions = regis.Question.objects.filter(user=self.user)
        
        num_available = 0
        num_answered = 0
        
        for question in questions:
            if question.status == 'ready':
                num_available += 1
            if question.status == 'released':
                num_available += 1
            if question.status == 'solved':
                num_available += 1
                num_answered += 1
        
        return (num_answered, num_available)
    
    def percent_answered(self):
        num_answered, num_available = self.questions_answered()
        
        if num_available > 0:
            return int(round(((num_answered * 1.0) / num_available) * 100))
        else:
            return 0
    
    def guesses_per_question(self):
        guesses = regis.Guess.objects.filter(user=self.user)
        question_dict = {}

        if len(guesses) is 0:
            return 'N / A'
        
        # Add all of the keys to a dict.
        for guess in guesses:
            if question_dict.has_key(guess.question.id):
                question_dict[guess.question.id].append(guess.id)
            else:
                question_dict[guess.question.id] = [guess.id,]
        
        guess_cnt = [len(question_dict[key]) for key in question_dict.keys()]

        return (sum(guess_cnt) * 1.0) / len(guess_cnt)
    
    def fastest_answer(self):
        guesses = regis.Guess.objects.filter(user=self.user, correct=True)
        shortest = None
        
        if len(guesses) is 0:
            return 'N / A'
        
        for guess in guesses:
            guess_time = guess.time_guessed
            avail_time = guess.question.time_released
            
            delta = (guess_time - avail_time)
            if shortest is None or delta < shortest:
                shortest = delta

        seconds = float(shortest.seconds)
        days = int(math.floor(seconds / 86400))
        seconds -= (days * 86400)
        hours = int(math.floor(seconds / 3600))
        seconds -= (hours * 3600)
        minutes = int(math.floor(seconds / 60))
        seconds -= (minutes * 60)

        if days > 0:
            return '%d days, %d hours, %d minutes and %d seconds' % (days, hours, minutes, seconds)
        elif hours > 0:
            return '%d hours, %d minutes and %d seconds' % (hours, minutes, seconds)
        elif minutes > 0:
            return '%d minutes and %d seconds' % (minutes, seconds)
        else:
            return '%d seconds!'
        
    def hardest_question_answered(self):
        # Get all questions that have been answered by the user.
        questions = regis.Question.objects.filter(user=self.user, status='solved')
        
        hardest_q = None
        hardest_percentage = 1.1
        # Check to determine the number of released vs solved.
        for question in questions:
            other_qs = regis.Question.objects.filter(template=question.template)
            other_available = 0
            other_solved = 0
            
            for other_q in other_qs:
                if other_q.status == 'solved':
                    other_solved += 1
                    other_available += 1
                elif other_q.status == 'released':
                    other_available += 1

            if other_available > 0:
                percentage = (other_solved * 1.0) / other_available
            
                if percentage < hardest_percentage:
                    hardest_q = question
                    hardest_percentage = percentage
                    
        # If the percentage hasn't changed it means the user hasn't solved
        # any questions yet.
        if hardest_percentage > 1.0:
            return (hardest_q, None)
        else:
            return (hardest_q, hardest_percentage * 100)