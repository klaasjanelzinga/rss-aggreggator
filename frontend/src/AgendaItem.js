import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import GridListTile from '@material-ui/core/GridListTile';
import GridListTileBar from '@material-ui/core/GridListTileBar';
import ICSButton from './ICSButton';


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
    icalButton: {
        float: 'right',
        marginBottom: '10px',
        marginTop: '10px',
        marginRight: '10px',
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


class AgendaItem extends React.Component {

    render() {
        const { classes } = this.props;
        const event = this.props.item;
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
                <ICSButton event={event}></ICSButton>
            </GridListTile>
        );
    }
}

AgendaItem.propTypes = {
    classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(AgendaItem);

