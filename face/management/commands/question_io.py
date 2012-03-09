from django.core.management.base import BaseCommand, CommandError
from django.core import serializers

import face.offline.QuestionSolver as qs
import face.models.models as regis
import sys

class Command(BaseCommand):
    args = '[import|export]'
    help = 'Import or export the question templates.'

    def handle(self, *args, **options):
        if len(args) != 1:
            print 'Please specify either "import" or "export."'
            sys.exit(1)
    
        ## Import all questions and update the body text
        ## based on the title.
        if args[0] == 'import':
            infile = open('templates.xml')
            templates = serializers.deserialize('xml', infile)
            
            for template in [template for template in templates]:
                try:
                    qt = regis.QuestionTemplate.objects.get(title=template.object.title)
                    qt.text = template.object.text
                    qt.save()
                    print 'Updated %s' % qt.title
                except regis.QuestionTemplate.DoesNotExist:
                    print 'Template %s doesn\'t exist.' % template.object.title
                    
            infile.close()
    
        ## Export all question templates to an XML file.
        elif args[0] == 'export':
            outfile = open('templates.xml', 'w')
            serializers.serialize('xml', regis.QuestionTemplate.objects.all(), stream=outfile)
            outfile.close()
            print 'Templates written to templates.xml'
