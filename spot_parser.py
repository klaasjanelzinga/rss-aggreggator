from bs4 import BeautifulSoup

#          <article class="program__item" data-datetime="1554285600" data-description="klassiek-lunchconcert-in-het-cafe-van-de-oosterpoort" data-filters="" data-genres="" data-title="lunchconcert-carlos-marin-rayo-piano">
#           <a class="program__link" href="https://www.spotgroningen.nl/programma/lunchconcert-3-april-2019/">
#            <time class="program__date" datetime="2019-04-03T12:00:00+02:00">
#             <span>
#              wo
#             </span>
#             <strong>
#              3
#             </strong>
#             <span>
#              apr
#             </span>
#            </time>
#            <figure class="program__figure" style="background-color: #1f1118;">
#             <img alt="" class="program__image b-lazy" data-src="/wp-content/uploads/2017/09/lunchconcerten-nieuw-150x150.jpg" src="data:image/gif;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs="/>
#            </figure>
#            <div class="program__content">
#             <h1>
#              Lunchconcert: Carlos Marín Rayo (piano)
#             </h1>
#             <p>
#              Klassiek lunchconcert in Het Café van De Oosterpoort
#             </p>
#            </div>
#           </a>
#          </article>

base_url = 'https://www.spotgroningen.nl'
scrape_url = 'https://www.spotgroningen.nl/programma'
with open('samples/spot/Programma - Spot Groningen.html') as f:
    content = ''.join(f.readlines())
    soup = BeautifulSoup(content, 'html.parser')

    program_items = soup.find_all('article')
    item = program_items[0]
    url = item.a.get('href')
    image_url = item.a.figure.img.get('data-src')
    title = item.a.div.h1.text
    description = item.a.div.p.text
