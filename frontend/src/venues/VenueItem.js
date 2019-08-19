import { Typography } from '@material-ui/core';
import GridListTile from '@material-ui/core/GridListTile';
import { withStyles } from '@material-ui/core/styles';
import PropTypes from 'prop-types';
import React from 'react';
import { withRouter } from 'react-router-dom';


const styles = theme => ({

    gridListTile: {
        width: '100%',
        marginBottom: '2px',
        borderStyle: 'none',
        border: '1px',
        backgroundColor: 'lightgrey',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'left',
    },
    tileText: {
        paddingLeft: '5px',
        display: 'flex',
        textAlign: 'left',
    },
});


class VenueItem extends React.Component {

    render() {
        const { classes } = this.props;
        const venue = this.props.item;
        return (
            <GridListTile className={classes.gridListTile} key={venue.venue_id} >
                <Typography className={classes.tileText} color="textSecondary">
                    {venue.name}
                </Typography>
                <Typography className={classes.tileText} variant="subtitle1" color="textSecondary">
                    <a href={venue.url}>{venue.url}</a>
                </Typography>
                <Typography className={classes.tileText} variant="subtitle1" color="textSecondary">
                    <a href={`mailto:{venue.email}`}>{venue.email}</a>
                </Typography>
                <Typography className={classes.tileText} variant="subtitle1" color="textSecondary">
                    {venue.city} {venue.country}
                </Typography>
                <Typography className={classes.tileText} variant="subtitle1" color="textSecondary">
                    Date last checked: {venue.lastFetchedDate}
                </Typography>
            </GridListTile>
        );
    }
}

VenueItem.propTypes = {
    classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(withRouter(VenueItem));

