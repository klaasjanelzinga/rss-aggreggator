from datetime import datetime
import logging
from typing import List

from bs4 import BeautifulSoup

from core.event import Event


class SimplonParser:

# <a data-type="concert" href="http://simplon.nl/?post_type=events&p=17412" title="Idaly" class="isotope item concert">
#     <div class="item-image" style="background-image: url(https://simplon.nl/content/uploads/2019/03/IDALY_ONTHEROAD_FINALARTWORK_CLEAN-600x600.jpg)">
#         <div class="overlay bg-color-concert"></div>
#                     </div>
#     <div class="item-details">
#         <div class="title"><h2><span>Idaly</span></h2></div>
#         <div class="subtitle">On The Road Tour</div>        <div class="date color-concert">Za 13 April 2019</div>
#         <div class="details">
#             <span class="mouseover">
#                 <br>Waar: <b>Kleine zaal</b> Open: <b>20:00 - 23:00 uur</b>
#                 <br>VVK: <b>&euro; 11,-</b> DVK: <b>&euro; 11,-</b>                <br>
#                 Aanvang: <b>21:00 uur</b><br>
#             </span>
#             Genre: <b>Hiphop / Trap</b>
#         </div>
#     </div>
#     <div class="item-hitarea">
#             <div data-ticket="https://simplon.stager.nl/web/tickets/282459" data-type="concert" class="buy-ticket color-black border-concert bg-color-concert">Koop tickets</div>
#     </div>
# </a>
    def __init__(self):
        pass

    def parse(self, content: str) -> List[Event]:
        soup = BeautifulSoup(content, features='html.parser')
        events = soup.find_all('a', {'class': 'item'})

        logging.info(f'found {len(events)} event in {self}')
        return [self._transform(tag) for tag in events]

    def _transform(self, tag) -> Event:
        return Event(url='',
                     title='',
                     description='',
                     venue_id='',
                     source='',
                     date_published=datetime.now(),
                     when=datetime.now(),
                     image_url=''
                     )
