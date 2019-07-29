import AppBar from '@material-ui/core/AppBar';
import { withStyles } from '@material-ui/core/styles';
import Toolbar from '@material-ui/core/Toolbar';
import PropTypes from 'prop-types';
import React from 'react';
import HeaderMenu from './HeaderMenu';
import SearchBox from './SearchBox';
import Title from './Title';


const styles = theme => ({
  headerbar: {
    width: '100%',
    height: '84px',
  },
  grow: {
    flexGrow: 1,
  },
  sectionDesktop: {
    display: 'none',
    [theme.breakpoints.up('md')]: {
      display: 'flex',
    },
  },
  sectionMobile: {
    display: 'flex',
    [theme.breakpoints.up('md')]: {
      display: 'none',
    },
  },
});


class HeaderBar extends React.Component {

  renderSearchBox() {
    if (this.props.searchEvents === undefined) {
      return <div></div>
    } else {
      return <SearchBox searchEvents={this.props.searchEvents} />;
    }
  }

  render() {
    const { classes } = this.props;
    return (
      <div className={classes.headerbar}>
        <AppBar position="static">
          <Toolbar>
            <Title />
            <div className={classes.grow} />
            {this.renderSearchBox()}
            <HeaderMenu />
          </Toolbar>
        </AppBar>

      </div>
    );
  }
}

HeaderBar.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(HeaderBar);