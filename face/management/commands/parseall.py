import face.models.models as regis
import face.offline.QuestionParser as qp
import face.offline.ParserTools.ParserTools as ParserTools

import json, datetime

from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
  args = 'none'
  help = 'Parses all of the questions that havent been parsed for all users.'

  def handle(self, *args, **options):
    # The number of unassigned users that should be ready at any point.
    standby_threshold = 100

    parser = qp.QuestionParser()

    # Get all live templates.  Templates can be made live in the database.
    all_templates = regis.QuestionTemplate.objects.filter(live=True)
    all_tids = [t.id for t in all_templates]
    
    users = regis.RegisUser.objects.all()
    print 'Processing %d question templates...' % len(all_templates)
    print 'Scanning and updating records for %d user(s)...' % len(users)
    records_added = 0
    for user in users:
        ready_questions = regis.Question.objects.filter(uid__exact=user.id)
        ready_tids = [q.tid.id for q in ready_questions]
        
        parser.user = user
        
        # The default position of this question will be LAST until the
        # shuffler does its work.
        if len(ready_questions) > 0:
            next_order = max([rq.order for rq in ready_questions]) + 1
        else:
            next_order = 0
                              
        for t in ( set(all_tids) - set(ready_tids) ):
            template = regis.QuestionTemplate.objects.get(id=t)
            parser.template = template
            
            try:
                text, values = parser.parse(template.q_text)
            except Exception as e:
                print '[ERROR] Error parsing template #%d' % template.id
                print e
                continue
            
            # Save the information as a processed question.  The solver processor
            # will pick it up once it's been inserted.
            q = regis.Question(tid=template, uid=user, text=text, variables=json.dumps(values), time_released=datetime.datetime.now(), status='pending', order=next_order)
            q.save()
            
            records_added += 1
            # Increment the value of 'order' that will be stored on the next record.
            next_order += 1
            
    print '%d records added.' % records_added
