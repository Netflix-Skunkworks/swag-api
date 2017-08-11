import React, {Component} from 'react';
import {Card, CardActions, CardHeader, CardText} from 'material-ui/Card';
import FlatButton from 'material-ui/FlatButton';

class Error extends Component {
    constructor(props, context) {
        super(props, context);
        this.handleRetry = this.handleRetry.bind(this);
    }

    handleRetry = () => {
        this.setState({open: true});
    };

    render() {
        return (
            <Card>
                <CardHeader
                    title="Error"
                    subtitle="Something has gone terribly wrong"
                />
                <CardText>
                    SWAG isn't acting like itself at the moment, would you like to retry?
                </CardText>
                <CardActions>
                    <FlatButton label="Retry" onTouchTap={this.handleRetry}/>
                </CardActions>
            </Card>
        )
    }
}

export default Error;