#!/usr/bin/env python
import os
import sys
"""Django's command-line utility for administrative tasks."""

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Climate_Agency.settings')

    # ✅ Add both folders to sys.path so Python can locate climate_data
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'Climate_Agency')))
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'climate_data')))

    try:
        import django
        django.setup()
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # ✅ Now import fetch_open_meteo safely (after Django setup)
    try:
        from climate_data.fetch_open_meteo import fetch_open_meteo
        dataset, data = fetch_open_meteo((24.8607, 67.0011))  # Karachi coords
        print("Weather data fetched successfully ✅")
    except Exception as e:
        print(f"⚠️ fetch_open_meteo import failed: {e}")

    execute_from_command_line(sys.argv)
if __name__ == '__main__':
    main()
