import React from 'react';
import PropTypes from 'prop-types';
import {withStyles} from 'material-ui/styles';
import IconButton from 'material-ui/IconButton';
import Computer from 'material-ui-icons/Computer';
import Typography from 'material-ui/Typography';

import Dialog from 'material-ui/Dialog';
import AppBar from 'material-ui/AppBar';
import Toolbar from 'material-ui/Toolbar';
import ArrowBack from 'material-ui-icons/ArrowBack';
import Slide from 'material-ui/transitions/Slide';
import Tooltip from 'material-ui/Tooltip';
import ServiceCard from './ServiceCard';


const styles = theme => ({
    appBar: {
        position: 'relative',
    },
    flex: {
        flex: 1,
    },
    container: {
        padding: '16px',
        fontWeight: '500',
        boxSizing: 'border-box',
        position: 'relative',
        whiteSpace: 'nowrap',
        overflow: 'auto'
    },
    content: {
        display: 'flex',
        flexDirection: 'column',
        flexWrap: 'no-wrap',
        minHeight: '100vh'
    }
});


class ServiceDialog extends React.PureComponent {
    constructor(props, context) {
        super(props, context);
        this.handleOpen = this.handleOpen.bind(this);
        this.handleClose = this.handleClose.bind(this);

        this.state = {
            open: false,
        };
    }

    handleOpen() {
        this.setState({open: true});
    }

    handleClose() {
        this.setState({open: false});
    }

    render() {
        const {classes} = this.props;
        return (
            <div>
                <Tooltip title="Services">
                    <IconButton onClick={this.handleOpen}>
                        <Computer/>
                    </IconButton>
                </Tooltip>
                <Dialog
                    fullScreen
                    open={this.state.open}
                    onRequestClose={this.handleClose}
                    transition={<Slide direction="right"/>}
                >
                    <AppBar position="static">
                        <Toolbar>
                            <IconButton color="contrast" onClick={this.handleClose} aria-label="Close">
                                <ArrowBack/>
                            </IconButton>
                            <Typography type="title" color="inherit" className={classes.flex}>
                                Services
                            </Typography></Toolbar>
                    </AppBar>
                    <div className={classes.container}>
                        <div className={classes.content}>
                            {this.props.services.map((item, index) => <ServiceCard key={index} service={item}/>)}
                        </div>
                    </div>
                </Dialog>
            </div>
        );
    }
}

ServiceDialog.propTypes = {
    classes: PropTypes.object.isRequired
};

export default withStyles(styles)(ServiceDialog);