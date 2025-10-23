import os
import sys
import django

# ---------- Set project path ----------
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Climate_Agency'))
sys.path.insert(0, project_path)

# ---------- Set Django settings ----------
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Climate_Agency.settings')
django.setup()

# ---------- Import your function ----------

try:
	from Climate_Agency.climate_data.utils.fetch_open_meteo import fetch_open_meteo
except Exception:
	# Fallback: load the module directly from its file in case package imports fail
	import importlib.util
	module_path = os.path.join(project_path, 'Climate_Agency', 'climate_data', 'utils', 'fetch_open_meteo.py')
	spec = importlib.util.spec_from_file_location("fetch_open_meteo_module", module_path)
	if spec is None or spec.loader is None:
		raise ImportError(f"Could not load module from {module_path}")
	fetch_mod = importlib.util.module_from_spec(spec)
	spec.loader.exec_module(fetch_mod)
	fetch_open_meteo = getattr(fetch_mod, 'fetch_open_meteo')

# Karachi coordinates
dataset, data = fetch_open_meteo((24.8607, 67.0011))
print(data)
