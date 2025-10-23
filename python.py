# import os
# import django
# file_name = 'Climate_Agency'
# file_path = os.path.join('python_django', file_name)
# while not os.path.isfile(file_path):
#     file_name = input("Whoops! No such file! Please enter the name of the file you'd like to use: ")
#     file_path = os.path.join('python_django', file_name)

#     os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Climate_Agency.settings')
#     django.setup()

# import sys
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'python_django')))

# # ✅ Import your function
# # Update the import path below to match your actual project structure
# # For example, if 'fetch_open_meteo.py' is directly inside 'Climate_Agency', use:
# from Climate_Agency.fetch_open_meteo import fetch_open_meteo

# # If 'fetch_open_meteo.py' is inside 'Climate_Agency/utils', use:
# from Climate_Agency.utils.fetch_open_meteo import fetch_open_meteo

# # If 'fetch_open_meteo.py' is inside 'Climate_Agency/climate_data/utils', use:
# from Climate_Agency.climate_data.utils.fetch_open_meteo import fetch_open_meteo

# # ✅ Run it
# dataset, data = fetch_open_meteo((24.8607, 67.0011))  # Karachi coordinates
# print(data)