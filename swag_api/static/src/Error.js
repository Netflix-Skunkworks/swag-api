import React, {Component} from 'react';
import Card, {CardActions, CardHeader, CardContent} from 'material-ui/Card';
import Button from 'material-ui/Button';


class Error extends Component {
    constructor(props, context) {
        super(props, context);
        this.handleRetry = this.handleRetry.bind(this);
    }

    handleRetry() {
        this.setState({open: true});
    }

    render() {
        return (
            <Card>
                <CardHeader
                    title="Error"
                    subtitle="Something has gone terribly wrong"
                />
                <CardContent>
                    SWAG isn't acting like itself at the moment, would you like to retry?
                </CardContent>
                <CardActions>
                    <Button label="Retry" onClick={this.handleRetry}/>
                </CardActions>
            </Card>
        )
    }
}

export default Error;