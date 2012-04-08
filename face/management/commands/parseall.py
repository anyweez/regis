import face.models.models as models
import face.offline.QuestionParser as qp

import json

from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    args = 'none'
    help = 'Parses all of the questions that havent been parsed for all users.'

    # The number of unassigned users that should be ready at any point.
    permutations = {
        'auto' : 100,
        'peer' : 1
    }

    def handle(self, *args, **options):
        parser = qp.QuestionParser()

        # Get all live templates.  Templates can be made live in the database.
        all_templates = models.QuestionTemplate.objects.filter(live=True, status='waiting')
#        all_tids = [t.id for t in all_templates]
    
        for template in all_templates:
            num_instances = models.QuestionInstance.objects.filter(template=template).count()
            try:
                req_instances = self.permutations[template.type]
            except KeyError:
                print 'Invalid template type for #%d: %s' % (template.id, template.type)
                continue
            
            print 'Parsing %d / %d instances of template #%d' % (req_instances - num_instances, req_instances, template.id)
            
            for i in xrange(req_instances - num_instances):
                instance = models.QuestionInstance(template=template, text='', variables='')
                instance.save()

                try:               
                    text, values = parser.parse(template, instance)
                
                    instance.text = text
                    instance.variables = json.dumps(values)
                    instance.save()
                # If there are any errors, let's delete them.
                except Exception as e:
                    instance.delete()
                    print e
                    
            template.status = 'pending'
            template.save()