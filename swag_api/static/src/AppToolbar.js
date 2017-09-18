import React, {Component} from 'react';
import {withStyles} from 'material-ui/styles';
import AppBar from 'material-ui/AppBar';
import Toolbar from 'material-ui/Toolbar';
import Typography from 'material-ui/Typography';

import Download from './Download';
import AppSearch from './AppSearch';
import AppSearchResults from './AppSearchResults';


const styles = theme => ({
    root: {
        width: '100%',
    },
    flex: {
        flex: 1,
    },
});

class AppToolbar extends Component {
    render() {
        const classes = this.props.classes;

        return (
            <div className={classes.root}>
                <AppBar position="static">
                    <Toolbar>
                        <Typography type="title" color="inherit" className={classes.flex}>
                            SWAG
                        </Typography>
                        <AppSearch/>
                        <Download/>
                    </Toolbar>
                </AppBar>
                <AppSearchResults/>
            </div>
        );
    }
}


export default withStyles(styles)(AppToolbar);