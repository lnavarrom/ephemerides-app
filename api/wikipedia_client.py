import requests
from datetime import datetime
from typing import Dict, List, Optional
import random

class WikipediaClient:
    """Client per obtenir efemèrides de Wikipedia"""

    def __init__(self, base_url_template: str):
        self.base_url_template = base_url_template
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'EphemeridesApp/1.0 (Educational Project)'
        })

    def get_events(self, month: int, day: int, language: str = 'ca') -> List[Dict]:
        """
        Obté tots els events del dia especificat

        Returns:
            List de diccionaris amb: year, text, pages (links relacionats)
        """
        url = self.base_url_template.format(
            lang=language,
            type='events',
            month=month,
            day=day
        )

        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            return data.get('events', [])
        except requests.RequestException as e:
            raise Exception(f"Error fetching events from Wikipedia: {str(e)}")

    def get_random_event(self, month: int, day: int, language: str = 'ca') -> Optional[Dict]:
        """Retorna un event aleatori del dia especificat"""
        events = self.get_events(month, day, language)
        return random.choice(events) if events else None

    def get_event_details(self, event: Dict, language: str = 'ca') -> Dict:
        """
        Enriqueix un event amb més informació dels seus links relacionats

        Returns:
            Dict amb: year, text, description (extret de pages), links
        """
        result = {
            'year': event.get('year', 'Unknown'),
            'text': event.get('text', ''),
            'links': []
        }

        # Extreure informació de les pàgines relacionades
        pages = event.get('pages', [])
        if pages:
            main_page = pages[0]
            result['description'] = main_page.get('extract', '')
            result['thumbnail'] = self._extract_thumbnail(main_page)
            result['links'] = self._extract_links(pages)

        return result

    def _extract_thumbnail(self, page: Dict) -> str:
        """Extreu la URL del thumbnail d'una pàgina"""
        thumbnail = page.get('thumbnail', {})
        return thumbnail.get('source', '') if thumbnail else ''

    def _extract_links(self, pages: List[Dict]) -> List[Dict]:
        """Extreu els links de Wikipedia de les pàgines relacionades"""
        links = []
        for page in pages:
            page_url = page.get('content_urls', {}).get('desktop', {}).get('page', '')
            if page_url:
                links.append({
                    'title': page.get('title', ''),
                    'url': page_url
                })
        return links
