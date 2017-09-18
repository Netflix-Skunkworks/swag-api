import React, {Component} from 'react';
import Button from 'material-ui/Button';
import Snackbar, {SnackbarContent} from 'material-ui/Snackbar';


const action = (
    <Button color="accent" dense>
        Retry
    </Button>
);


class Error extends Component {
    render() {
        const open = this.props.status;
        return (
            <Snackbar open={open}>
                <SnackbarContent
                    message="Error fetching account data. "
                    action={action}
                />
            </Snackbar>
        )
    }
}

export default Error
