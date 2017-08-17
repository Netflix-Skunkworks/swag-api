import React from 'react';
import Dialog from 'material-ui/Dialog';
import FlatButton from 'material-ui/FlatButton';
import ReactJson from 'react-json-view';
import IconButton from 'material-ui/IconButton';

import Search from 'material-ui/svg-icons/action/search';


class JSONDialog extends React.PureComponent {
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
    };

    handleClose() {
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

        return (
            <div>
                <IconButton tooltip="View JSON" onTouchTap={this.handleOpen}>
                    <Search/>
                </IconButton>
                <Dialog
                    title="Raw JSON"
                    actions={actions}
                    modal={false}
                    open={this.state.open}
                    onRequestClose={this.handleClose}
                >
                    <div style={{overflow: 'auto', height: '500px', width: 'auto'}}>
                        <ReactJson src={this.props.data}/>
                    </div>
                </Dialog>
            </div>
        );
    }
}

export default JSONDialog;