import React, { Component } from 'react';
import Agenda from './agenda/Agenda';
import './App.css';
import HeaderBar from './headerbar/HeaderBar';
import config from './Config'

class App extends Component {

  constructor() {
    super()
    this.state = {
      eventsFetched: false,
      fetch_offset: '',
      events: [],
      is_fetching_done: false,
      currentView: "TODAY",
    }
    this.is_searching = false
    this.searchTerms = ''
    this.endpoint = `${config.apihost}/api`
    this.eventEndpoint = `${this.endpoint}/events`
    this.todayEventEndpoint = `${this.endpoint}/events/today`
    this.tomorrowEventEndpoint = `${this.endpoint}/events/tomorrow`
    this.searchEndpoint = `${this.endpoint}/search`

    this.searchEvents = this.searchEvents.bind(this);
    this.switchView = this.switchView.bind(this);
  }

  is_fetching_done(base64EncodedDone) {
    var base64 = require('base-64');
    var decoded = base64.decode(base64EncodedDone)
    return decoded === 'DONE'
  }

  fetchMoreEvents() {
    this.setState({ eventsFetched: false })
    if (this.is_searching) {
      this.concatFetchedEvents(`${this.searchEndpoint}?fetch_offset=${this.state.fetch_offset}&term=${this.searchTerms}`)
    } else {
      this.concatFetchedEvents(`${this.eventEndpoint}?fetch_offset=${this.state.fetch_offset}`)
    }
  }

  concatFetchedEvents(endpoint) {
    fetch(endpoint)
      .then(results => results.json())
      .then(results => {
        this.setState({
          events: this.state.events.concat(results.events),
          fetch_offset: results.fetch_offset,
          eventsFetched: true,
          is_fetching_done: this.is_fetching_done(results.fetch_offset),
        })
      })
  }

  searchEvents(searchTerms) {
    if (searchTerms === '') {
      this.fetchTodayEvents()
      return;
    }
    this.is_searching = true
    this.searchTerms = searchTerms
    this.setState({
      eventsFetched: false,
      fetch_offset: '',
      events: [],
      currentView: "SEARCH_RESULTS",
    })
    this.fetchEvents(`${this.searchEndpoint}?term=${searchTerms}`)
  }

  fetchEvents(endpoint) {
    this.setState({
      events: [],
      eventsFetched: false,
    })
    fetch(endpoint)
      .then(results => results.json())
      .then(results => {
        this.setState({
          events: results.events,
          fetch_offset: results.fetch_offset,
          eventsFetched: true,
          is_fetching_done: this.is_fetching_done(results.fetch_offset),
        })
      })
  }

  fetchTodayEvents() {
    this.is_searching = false
    this.search_terms = ''
    this.fetchEvents(this.todayEventEndpoint);
  }

  fetchTomorrowEvents() {
    this.is_searching = false
    this.search_terms = ''
    this.fetchEvents(this.tomorrowEventEndpoint);
  }

  fetchAllEvents() {
    this.is_searching = false
    this.search_terms = ''
    this.fetchEvents(this.eventEndpoint);
  }

  componentDidMount() {
    this.fetchTodayEvents();
  }

  switchView(newView) {
    this.setState({ currentView: newView })
    if (newView === "ALL") {
      this.fetchAllEvents();
    }
    if (newView === "TOMORROW") {
      this.fetchTomorrowEvents();
    }
    if (newView === "TODAY") {
      this.fetchTodayEvents();
    }
  }

  render() {
    return (
      <div className="App">
        <HeaderBar
          selected={this.state.currentView}
          switchView={(newView) => this.switchView(newView)}
          searchEvents={(searchTerms) => this.searchEvents(searchTerms)}
        />

        <Agenda
          events={this.state.events}
          currentView={this.state.currentView}
          eventsFetched={this.state.eventsFetched}
          isFetchingDone={this.state.is_fetching_done}
          fetchMoreEvents={() => this.fetchMoreEvents()}
        />
      </div>

    );
  }
}

export default App;
