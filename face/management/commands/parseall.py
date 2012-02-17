import face.models.models as regis
import face.offline.QuestionParser as qp
import face.offline.ParserTools.ParserTools as ParserTools

import json, datetime

from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    args = 'none'
    help = 'Parses all of the questions that havent been parsed for all users.'

    # The number of unassigned users that should be ready at any point.
    SETS_AVAILABLE = 10

    def handle(self, *args, **options):
        parser = qp.QuestionParser()

        # Get all live templates.  Templates can be made live in the database.
        all_templates = regis.QuestionTemplate.objects.filter(live=True)
        all_tids = [t.id for t in all_templates]
    
        users = regis.RegisUser.objects.all()
        avail_qsets = regis.QuestionSet.objects.filter(reserved_by=None)
        print '%d users are registered in the system.' % len(users)
        print '%d question sets are available of the requested %d' % (len(avail_qsets), self.SETS_AVAILABLE)
        print '  Processing %d question templates for each set.' % len(all_templates)
        records_added = 0
    
        # Add new question sets
        for i in xrange(self.SETS_AVAILABLE - len(avail_qsets)):
            qset = regis.QuestionSet(reserved_by=None)
            qset.save()
    
        all_qsets = regis.QuestionSet.objects.all()
        # Process all question sets and add missing questions.
        for qset in all_qsets:
            questions = qset.questions.exclude(status='retired')
        
            target_tids = list(set(all_tids) - set([q.template.id for q in questions]))
            parser.qset = qset
        
            # The default position of this question will be LAST until the
            # shuffler does its work.
            if len(questions) > 0:
                next_order = max([rq.order for rq in questions]) + 1
            else:
                next_order = 0
                              
            for t in target_tids:
                template = regis.QuestionTemplate.objects.get(id=t)
                parser.template = template
            
                try:
                    text, values = parser.parse(template.text)
                except Exception as e:
                    print '[ERROR] Error parsing template #%d' % template.id
                    print e
                    continue
            
                # Save the information as a processed question.  The solver processor
                # will pick it up once it's been inserted.
                try:
                    q = regis.Question(template=template, user=qset.reserved_by, text=text, variables=json.dumps(values), status='pending', order=next_order)
                    q.save()
                    
                # If we get this exception then we're got some cruft that needs to be cleared away.
                # TODO: Catch exception for when qset.reserved_by doesn't exist.  Delete the question set and all corresponding questions in this case.
                except regis.RegisUser.DoesNotExist:
                    pass
                    # Delete the questions owned by the user.
                    # Delete the answers.
                    # Delete the question set.
                
                # Add this question to the question set.
                qset.questions.add(q)
            
                records_added += 1
                # Increment the value of 'order' that will be stored on the next record.
                next_order += 1
                # Save the question set.
            qset.save()
            
        print '%d records added.' % records_added
