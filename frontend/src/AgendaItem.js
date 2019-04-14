import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import GridListTile from '@material-ui/core/GridListTile';
import GridListTileBar from '@material-ui/core/GridListTileBar';


const styles = theme => ({
    gridListTile: {
        width: '100%',
        marginBottom: '10px',
    },
    agenda_image: {
        position: 'left',
        display: 'block',
        height: '250px',
        width: '250px',
    },
    details: {
        position: 'absolute',
        top: '0px',
        fontWeight: 'bold',
        left: '300px',
        color: 'black',
        textAlign: 'left',
        marginLeft: '5px'
    },
    details_title: {
        fontSize: '48px',
    },
    details_description: {
        fontSize: '32px',
    }
});


function AgendaItem(props) {
    const { classes } = props;
    const event = props.item;
    return (
        <GridListTile className={classes.gridListTile} key={event.id}>
            <a href={event.url}>
                <img className={classes.agenda_image} src={event.image_url} alt={event.title} />
                <div className={classes.details}>
                    <div className={classes.details_title}>{event.title}</div>
                    <div className={classes.description}>{event.description}</div>
                </div>
                <GridListTileBar
                    title={event.venue.name}
                    subtitle={<span>{event.when}</span>}
                >
                </GridListTileBar>
            </a>
        </GridListTile>
    );
}

AgendaItem.propTypes = {
    classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(AgendaItem);

