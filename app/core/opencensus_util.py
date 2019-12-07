from opencensus.stats import measure, view
from opencensus.stats.aggregation import SumAggregation
from opencensus.stats.measure import BaseMeasure
from opencensus.stats.stats import stats
from opencensus.tags import tag_key

from app.core.venue.venue import Venue


def create_count_measurement_for_venue(venue: Venue) -> BaseMeasure:
    requested_measure = measure.MeasureInt(
        f"number_of_items/{venue.venue_id}", f"Number of items uploaded for venue {venue.venue_id}", "By"
    )
    created_view = view.View(
        f"number_of_events/{venue.venue_id}",
        f"The number of events that were received for {venue.venue_id}",
        [tag_key.TagKey("venue_id")],
        requested_measure,
        SumAggregation(),
    )
    stats.view_manager.register_view(created_view)
    return requested_measure
