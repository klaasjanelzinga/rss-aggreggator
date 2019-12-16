from typing import Dict

from opencensus.common.transports.async_ import AsyncTransport
from opencensus.ext.stackdriver import stats_exporter as stackdriver_stats_exporter
from opencensus.ext.stackdriver import trace_exporter as stackdriver_exporter
from opencensus.ext.zipkin.trace_exporter import ZipkinExporter
from opencensus.stats import measure, view
from opencensus.stats.aggregation import LastValueAggregation
from opencensus.stats.measure import BaseMeasure
from opencensus.stats.stats import stats
from opencensus.tags import tag_key, tag_map, tag_value
from opencensus.trace.base_exporter import Exporter
from opencensus.trace.samplers import AlwaysOnSampler
from opencensus.trace.tracer import Tracer

from app.core.app_config import AppConfig
from app.core.venue.venue import Venue
from app.opencensus.ext.prometheus import Options, new_stats_exporter


class OpenCensusHelper:
    def __init__(self) -> None:
        self.venue_total_metric: Dict[str, BaseMeasure] = {}

    def register_venue(self, venue: Venue) -> None:
        if venue.venue_id in self.venue_total_metric:
            return
        requested_measure = measure.MeasureInt(
            f"number_of_items/{venue.venue_id}", f"Number of items uploaded for venue {venue.venue_id}", "By"
        )
        created_view = view.View(
            f"number_of_events/{venue.venue_id}_last_value",
            f"The number of events that were received for {venue.venue_id}",
            [tag_key.TagKey("venue_id")],
            requested_measure,
            LastValueAggregation(),
        )
        stats.view_manager.register_view(created_view)
        self.venue_total_metric[venue.venue_id] = requested_measure

    def count_venue_total(self, venue: Venue, total_events: int) -> None:
        self.register_venue(venue)
        metric = self.venue_total_metric[venue.venue_id]
        mmap = stats.stats_recorder.new_measurement_map()
        mmap.measure_int_put(metric, total_events)
        tmap = tag_map.TagMap()
        tmap.insert(tag_key.TagKey("venue_id"), tag_value.TagValue(venue.venue_id))
        mmap.record(tmap)


def initialize_tracer() -> Tracer:
    if AppConfig.is_running_in_gae():
        exporter = stackdriver_exporter.StackdriverExporter(transport=AsyncTransport)
    else:
        exporter = ZipkinExporter(service_name="local-rss", host_name="zipkin", port=9411, endpoint="/api/v2/spans")
    return Tracer(exporter=exporter, sampler=AlwaysOnSampler())


def initialize_stats_exporter() -> Exporter:
    if AppConfig.is_running_in_gae():
        return stackdriver_stats_exporter.new_stats_exporter()
    return new_stats_exporter(Options(address="", port=8081, namespace="rss-local"))


# Set op opencensus (OC) trace and metrics with exporter.
OC_TRACER = initialize_tracer()
stats.view_manager.register_exporter(initialize_stats_exporter())
