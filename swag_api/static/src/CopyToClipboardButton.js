import React, {Component} from 'react';
import IconButton from 'material-ui/IconButton';
import Snackbar from 'material-ui/Snackbar';

import CopyToClipboard from 'react-copy-to-clipboard';



class CopyToClipboardButton extends Component {
    constructor(props) {
        super(props);
        this.state = {
            open: false,
            value: '',
            copied: false,
        };

        this.handleRequestClose = this.handleRequestClose.bind(this);
    }

    handleRequestClose() {
        this.setState({
            open: false,
        });
    }

    render() {
        return (
            <div>
                <CopyToClipboard text={this.props.text}
                                 onCopy={() => this.setState({copied: true, open: true})}>
                    <IconButton>
                        {this.props.button}
                    </IconButton>
                </CopyToClipboard>
                <Snackbar
                    open={this.state.open}
                    message="Copied to clipboard"
                    autoHideDuration={4000}
                    onRequestClose={this.handleRequestClose}
                />
            </div>
        );
    }
}

export default CopyToClipboardButton;