from terroroftinytown.services.base import BaseService, html_unescape
import re
from terroroftinytown.services.status import URLStatus


class AdjixService(BaseService):
    def process_redirect(self, response):
        if '<title>Spammer</title>' in response.text or \
                '<title>Phisher</title>' in response.text:
            return (URLStatus.unavailable, None, None)

        groups = re.findall((
            r'CONTENT="0;URL=(.*)">|'
            '<frame src="(.*)">|'
            'rel="canonical" href="(.*)"/>'
            ),
            response.text
        )

        for group in groups:
            text = group[0] or group[1] or group[2]
            link = html_unescape(text)

            if 'ad.adjix.com' in link:
                continue

            return (URLStatus.ok, link, response.encoding)
