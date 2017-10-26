import React, {Component} from 'react';
import AppBar from 'material-ui/AppBar';
import Toolbar from 'material-ui/Toolbar';
import Typography from 'material-ui/Typography';
import {withStyles} from 'material-ui/styles';
import PropTypes from 'prop-types';

import Download from './Download';
import AppSearch from './AppSearch';

const styles = theme => ({
    flex: {
        flex: 1,
    },
});


class AppToolbar extends Component {
    render() {
        const {classes, search, data} = this.props;
        return (
            <AppBar position="static">
                <Toolbar>
                    <Typography type="title" color="inherit" className={classes.flex}>
                        SWAG
                    </Typography>
                    <AppSearch search={search}/>
                    <Download data={data}/>
                </Toolbar>
            </AppBar>
    );
    }
}

AppToolbar.propTypes = {
    data: PropTypes.object.isRequired,
    search: PropTypes.string.isRequired
};

export default withStyles(styles)(AppToolbar);