import requests
from django.conf import settings

def fetch_adzuna_jobs(search_query="software intern", country="in"):
    """
    Fetches real-time jobs from Adzuna API.
    Defaults to India ('in') and 'software intern'.
    """
    app_id = settings.ADZUNA_APP_ID
    app_key = settings.ADZUNA_APP_KEY
    
    url = f"https://api.adzuna.com/v1/api/jobs/{country}/search/1"
    
    params = {
        'app_id': app_id,
        'app_key': app_key,
        'results_per_page': 5,
        'what': search_query,
        'content-type': 'application/json'
    }
    
    try:
        response = requests.get(url, params=params, timeout=5)
        if response.status_code == 200:
            data = response.json()
            results = data.get('results', [])
            
            # Formating to match our local Job model structure for frontend consistency
            formatted_jobs = []
            for item in results:
                formatted_jobs.append({
                    'id': f"adz-{item.get('id')}",
                    'employer': item.get('company', {}).get('display_name', 'External Hirer'),
                    'title': item.get('title'),
                    'description': item.get('description', ''),
                    'job_type': 'external',
                    'location': item.get('location', {}).get('display_name', 'Diverse'),
                    'link': item.get('redirect_url'),
                    'is_external': True
                })
            return formatted_jobs
    except Exception as e:
        print(f"Adzuna API Error: {e}")
    
    return []
