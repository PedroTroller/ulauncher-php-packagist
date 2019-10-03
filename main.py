import json
import logging
import requests
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.client.Extension import Extension
from ulauncher.api.shared.action.OpenUrlAction import OpenUrlAction
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem

logger = logging.getLogger(__name__)

class PedroTrollerPackagistExtension(Extension):

    def __init__(self):
        super(PedroTrollerPackagistExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())

class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        query = event.get_argument()

        if not query:
            return;

        url = 'https://packagist.org/search.json?q={}'.format(query)

        logger.debug('Url sent to packagst: {}'.format(url))

        response = requests.get(url)
        data = response.json()

        items = []

        for package in data['results']:
            logger.debug('Found package: {}'.format(package['name']))

            items.append(ExtensionResultItem(
                    name=package['name'],
                    description=package['description'],
                    icon='images/PHP.png',
                    on_enter=OpenUrlAction(package['url'])
                )
            )

        return RenderResultListAction(items)

if __name__ == '__main__':
    PedroTrollerPackagistExtension().run()
