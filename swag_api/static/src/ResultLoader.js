import React, {Component} from 'react';
import {withStyles} from 'material-ui/styles';

import CircularProgress from 'material-ui/Progress/CircularProgress';

const styles = theme => ({
    loadingProgress: {
        height: '100%',
        padding: '0',
        margin: '0',
        marginTop: '10px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center'
    }
});


class ResultLoader extends Component {
    render() {
        const classes = this.props.classes;
        return (
            <div className={classes.loadingProgress}>
                <CircularProgress size={80}/>
            </div>
        )
    }
}

export default withStyles(styles)(ResultLoader);


