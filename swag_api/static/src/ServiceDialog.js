import React, {Component} from 'react';
import {ListItem} from 'material-ui/List';
import Dialog from 'material-ui/Dialog';
import FlatButton from 'material-ui/FlatButton';
import ActionGrade from 'material-ui/svg-icons/action/grade';
import {
    blue300,
} from 'material-ui/styles/colors';

import MetadataTable from './MetadataTable';


class ServiceDialog extends Component {
    constructor(props, context) {
        super(props, context);
        this.handleOpen = this.handleOpen.bind(this);
        this.handleClose = this.handleClose.bind(this);

        this.state = {
            open: false,
        };
    }

    handleOpen = () => {
        this.setState({open: true});
    };

    handleClose = () => {
        this.setState({open: false});
    };

    render() {
        const actions = [
            <FlatButton
                label="Close"
                primary={true}
                onTouchTap={this.handleClose}
            />,
        ];

        let metadata = this.props.data.metadata ? this.props.data.metadata : {};

        return (
            <div>
                <ListItem
                    onTouchTap={this.handleOpen}
                    primaryText={this.props.data.name}
                    leftIcon={<ActionGrade color={blue300}/>}
                />
                <Dialog
                    title="Details"
                    actions={actions}
                    modal={false}
                    open={this.state.open}
                    onRequestClose={this.handleClose}
                >
                    <MetadataTable data={metadata}/>
                </Dialog>
            </div>
        );
    }
}

export default ServiceDialog;