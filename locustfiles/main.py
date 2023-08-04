import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")

import django
django.setup()

from browse_courses import BrowseCourses
from browse_professors import BrowseProfessors
from browse_resources import BrowseResources
from browse_classrooms import BrowseClassrooms
from browse_references import BrowseReferences
from browse_recorded_classrooms import BrowseRecordedClassroom
