import { Fab } from "@material-ui/core";
import { withStyles } from '@material-ui/core/styles';
import { CalendarToday } from "@material-ui/icons";
import PropTypes from 'prop-types';
import React from 'react';
import { icsFormatter } from './ics';

const styles = theme => ({
    icalButton: {
        float: 'right',
        marginBottom: '10px',
        marginTop: '10px',
        marginRight: '10px',
    }
});


class ICSButton extends React.Component {
    constructor(props) {
        super(props);
        this.openICSFile = this.openICSFile.bind(this);
    }

    openICSFile() {
        console.log('creating ical', this.props.event);
        var cal = icsFormatter();
        cal.addEvent(
            this.props.event.url, 
            this.props.event.title, 
            this.props.event.description, 
            this.props.event.venue.name + ' ' + this.props.event.venue.city, 
            this.props.event.when,
            this.props.event.when);
        cal.download(`${this.props.event.title}.ics`)
    }

    render() {
        const { classes } = this.props;

        return <Fab color="secondary" aria-label="Download ical" className={classes.icalButton}
            onClick={this.openICSFile}>
            <CalendarToday></CalendarToday>
        </Fab>

    }
}

ICSButton.propTypes = {
    classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(ICSButton);

