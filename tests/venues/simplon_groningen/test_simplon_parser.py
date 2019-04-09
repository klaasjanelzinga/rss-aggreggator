import dateparser
from hamcrest import equal_to, none, is_not
from hamcrest.core import assert_that

from venues.simplon_groningen.simplon_parser import SimplonParser


class TestSimplonParser:

    def test_parse_sample(self):
        parser = SimplonParser()
        with open('tests/samples/simplon-groningen/simplon.html') as f:
            results = parser.parse(''.join(f.readlines()))
            assert_that(len(results), equal_to(34))
            event = results[0]
            assert_that(event.title, equal_to('Foxlane + Car Pets - Simplon UP'))
            assert_that(event.description, equal_to(''))
            assert_that(event.url, equal_to('http://simplon.nl/?post_type=events&p=17602'))
            assert_that(event.image_url,
                        equal_to('https://simplon.nl/content/uploads/2019/03/FOXLANE-MAIN-PRESS-PHOTO-600x600.jpg'))
            assert_that(event.when, equal_to(dateparser.parse('2019-04-11T21:30:00+02:00')))
            assert_that(event.source, equal_to('https://www.simplon.nl'))
            assert_that(event.date_published, is_not(none()))
