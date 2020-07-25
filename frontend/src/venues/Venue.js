import GridList from '@material-ui/core/GridList';
import { withStyles } from '@material-ui/core/styles';
import PropTypes from 'prop-types';
import React from 'react';
import VenueItem from './VenueItem.js';

const styles = ({
    progressbar: {
        flexGrow: 1,
        marginTop: '10px',
    }
});


class Venue extends React.Component {

    render() {
        const { classes } = this.props
        // if (this.props.venuesFetched) {
            let nothingFound;

            if (this.props.venues.length === 0) {
                nothingFound = <p>Nothing found !</p>
            }

            return (
                <div>
                    {nothingFound}
                    <GridList cols={1} className={classes.gridList}>
                        {this.props.venues.map(venue => (
                            <VenueItem item={venue} key={venue.venue_id} />
                        ))}
                    </GridList>
                </div>
            );
    }
}

Venue.propTypes = {
    classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(Venue);

