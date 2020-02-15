import React, { Component } from 'react';
import HeaderBar from '../headerbar/HeaderBar';
import Venue from './Venue.js'
import { withRouter } from 'react-router-dom';
import config from '../Config'

class VenueApp extends Component {

    constructor() {
        super()
        this.state = {
            venues: [],
            venuesFetched: false
        }
        this.endpoint = `${config.apihost}/api/venues`;
    }

    fetchInitialLoad() {
        fetch(this.endpoint)
            .then(results => results.json())
            .then(results => {
                this.setState({
                    venues: results.venues,
                    venuesFetched: true
                })
            })
    }

    componentDidMount() {
        this.fetchInitialLoad()
    }

    render() {
        return (
            <div className="App">
                <HeaderBar />
                <Venue
                    venues={this.state.venues}
                    venuesFetched={this.state.venuesFetched}
                />
            </div>
        );
    }
}

export default withRouter(VenueApp);
