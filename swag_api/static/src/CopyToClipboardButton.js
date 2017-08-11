import React, {Component} from 'react';
import IconButton from 'material-ui/IconButton';
import Snackbar from 'material-ui/Snackbar';

import ContentCopy from 'material-ui/svg-icons/content/content-copy';

import CopyToClipboard from 'react-copy-to-clipboard';


class CopyToClipboardButton extends Component {
    constructor(props) {
        super(props);
        this.state = {
            open: false,
            value: '',
            copied: false
        };
    }

    handleTouchTap = () => {
        this.setState({
            open: true,
        });
    };

    handleRequestClose = () => {
        this.setState({
            open: false,
        });
    };

    render() {
        return (
            <div>
                <CopyToClipboard text={this.props.text}
                                 onCopy={() => this.setState({copied: true, open: true})}>
                    <IconButton tooltip={this.props.tooltip}>
                        <ContentCopy/>
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