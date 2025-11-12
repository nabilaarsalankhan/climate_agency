#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import types, sys
from django.core.management import execute_from_command_line
if 'cgi' not in sys.modules:
        sys.modules['cgi'] = types.SimpleNamespace(
        parse_header=lambda x: (x, {}),
        escape=lambda s, quote=True: s
)
def main():
    """Run administrative tasks."""
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Climate_Agency.settings')
    sys.path.append(os.path.join(os.path.dirname(__file__), 'Climate_Agency'))
   
    try:
        execute_from_command_line(sys.argv)
    except Exception as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        )
    raise exc
        
execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
