import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cse_archive.settings.dev")

import django
django.setup()

from browse_courses import BrowseCourses
from browse_sessions import BrowseSessions
from browse_teachers import BrowseTeachers
from browse_resources import BrowseResources
from browse_references import BrowseReferences
