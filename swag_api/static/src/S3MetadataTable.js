import React, {Component} from 'react';
import {withStyles} from 'material-ui/styles';

import Typography from 'material-ui/Typography';


const styles = theme => ({});


class S3MetadataTable extends Component {

    render() {
        return (
            <div>
                <Typography type="subheading" gutterBottom>
                    Metadata
                </Typography>
            </div>
        )
    }
}

export default withStyles(styles)(S3MetadataTable);