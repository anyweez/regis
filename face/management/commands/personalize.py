from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from operator import itemgetter
import face.models.models as regis

import random, math

class Command(BaseCommand):
    args = 'none'
    help = 'Analyze user performance and modify individual question orderings.'

    @transaction.commit_manually
    def handle(self, *args, **options):
        users = regis.User.objects.filter(is_active=True)
        print 'Examining %d user(s)...' % len(users)
        
        # TODO: None of these measures currently include adjustments using the so-called
        # confidence parameter (theta): (#correct / (#guesses + sqrt(#guesses - avg(#guesses))))  
        
        # This list contains a difficulty estimation for this question across
        # all users.  Indexed by question template ID.
        global_diffs = self.get_global_diffs()
        # The list containing global correctness rates for users.  Indexed by user ID.
        pqs = self.get_pqs()
        # This list contains a difficulty estimation for a class of questions.
        # Indexed by class.
        local_diff = self.get_local_diffs()
        # The list containing global correctness rates for users by class.  Indexed first
        # by class, then by users.
        pcs = self.get_pcs()
        
        # For each user, find the relevance scores for each question and
        # probabilistically order them.
        for user in users:
            relevance = {}
#            print 'User "%s"' % user.username
            for template in regis.QuestionTemplate.objects.all():
                global_score = abs(global_diffs[template.id] - pqs[user.id])
        
                local_score = 0
                for tag in template.categories.all():
                    local_score += abs(local_diff[tag.id] - pcs[tag.id][user.id])
                # Divide by the total number of categories.
                if len(template.categories.all()) > 0:
                    local_score /= len(template.categories.all())
                
                relevance[template.id] = 2 - (global_score + local_score)
                relevance[template.id] /= 2
#                print '  #%d %s: %.3f' % (template.id, template.title, relevance[template.id])        
    
            questions = [(key, relevance[key]) for key in relevance.keys()]
            questions = sorted(questions, key=itemgetter(1), reverse=True)
    
            order = []
            while len(questions) > 0:
                # Weigh the relevance so that higher values have a significantly higher probability
                # of being drawn.  Each value [0, 1] is currently being raise to the third power but
                # this parameter can be tweaked.  Higher values will make it more probable that
                # highly relevant questions will be drawn.  If the value gets too high then some of
                # the relevance numbers will approach zero, which is not good.  Don't do that.
                total = math.floor(sum([math.pow(question[1], 3) for question in questions]) * 1000)
                count = random.randint(0, total)
    
                current = 0
                while count > 0:
                    count -= questions[current][1] * questions[current][1] * 1000
                    current += 1
                order.append(questions[current-1][0])
                del questions[current-1]

            user_q = regis.Question.objects.exclude(status='retired').filter(user=user)
            for question in user_q:
                question.order = order.index(question.template.id)
                question.save()
            
            # Commit the new ordering to the database as a single transaction.
            transaction.commit()
    
        print 'Complete!'
    # For each user, compute their personal question score.  This score
    # represents the ratio of questions that they get correct vs. those that they
    # have unlocked.  Higher scores indicate a higher level of completion.
    #
    # Note that this score is normalized to [0, 1] across all active users.
    def get_pqs(self):
        diffs = {}
        for user in regis.User.objects.filter(is_active=True):
            solved = regis.Question.objects.filter(user=user, status='solved')
            unsolved = regis.Question.objects.filter(user=user, status='released')
            
            
            diffs[user.id] = (len(solved) * 1.0) / (len(solved) + len(unsolved))
        
        peak_pgs = max(diffs.values())
        for key in diffs.keys():
            diffs[key] /= peak_pgs

        return diffs
    
    # For each class (tag) AND user, compute the personal class score.  This
    # represents the ratio of questions that the user has answered correctly,
    # similarly to the PQS score, but this is on a per-class basis.
    #
    # This score is also normalized to [0, 1] across all active users.
    def get_pcs(self):
        users = regis.User.objects.filter(is_active=True)
        diffs = {}
        for tag in regis.QuestionTag.objects.all():
            diffs[tag.id] = {}
            for user in users:
                solved = regis.Question.objects.filter(status='solved')
                unsolved = regis.Question.objects.filter(status='released')
                diffs[tag.id][user.id] = (len(solved) * 1.0) / (len(solved) + len(unsolved))
                
            peak_pcs = max(diffs[tag.id])
            for uid in diffs[tag.id].keys():
                diffs[tag.id][uid] /= peak_pcs
    
        return diffs

    # For each class, compute the global difficulty score.  Similar to
    # the global difficulty scores but are per-class (tag) instead of
    # per-template.
    def get_local_diffs(self):
        tags = regis.QuestionTag.objects.all()
        templates = regis.QuestionTemplate.objects.all()
        solved = regis.Question.objects.filter(status='solved')
        unsolved = regis.Question.objects.filter(status='released')
        
        correct = {}
        available = {}
        
        for tag in tags:
            correct[tag.id] = 0
            available[tag.id] = 0
        
        # Tally everything up.
        for tag in tags:
            for template in templates:
                for question in solved:
                    # If the question is solved and pulled from the correct
                    # template then count it.
                    if question.template.id == template.id:
                        correct[tag.id] += 1
                        available[tag.id] += 1
                for question in unsolved:
                    if question.template.id == template.id:
                        available[tag.id] += 1
                        
        diffs = []
        for tag in tags:
            if available[tag.id] > 0:
                diffs.append(1 - (correct[tag.id] * 1.0 / available[tag.id]))
            else:
                diffs.append(0)
        return diffs
    
    # For each question, compute the global difficulty score.  The difficulty
    # score is a number in the range [0, 1] and is based on how many user have
    # unlocked the question vs. how many have solved it.  The score increases
    # as the # of users to successfully solve the question decreases (they have
    # an inverse relationship).
    def get_global_diffs(self):
        unanswered = regis.Question.objects.exclude(user=None).filter(status='released')
        answered = regis.Question.objects.exclude(user=None).filter(status='solved')
        correct = {}
        available = {}
        
        templates = regis.QuestionTemplate.objects.all()
        for template in templates:
            correct[template.id] = 0
            available[template.id] = 0
            
        # Count all of the questions that are available but unanswered.
        for question in unanswered:
            available[question.template.id] += 1
                    
        # Count all of the questions that are answered.
        for question in answered:
            correct[question.template.id] += 1
            available[question.template.id] += 1
   
        diffs = {} 
        for template in templates:
            if available[template.id] == 0:
                perc = 0
            else:
                perc = 1 - (correct[template.id] * 1.0 / available[template.id])
            diffs[template.id] = perc
            
        return diffs