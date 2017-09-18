import React, {Component} from 'react';
import {withStyles} from 'material-ui/styles';

import Table, {TableBody, TableCell, TableHead, TableRow} from 'material-ui/Table';
import Typography from 'material-ui/Typography';


const styles = theme => ({});


class MetadataTable extends Component {
    getGeneral() {
        return Object.entries(this.props.data).filter(([key, value]) => {
            return !Array.isArray(value);
        });
    }

    render() {
        return (
            <div>
                <Typography type="subheading" gutterBottom>
                    Metadata
                </Typography>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell>Key</TableCell>
                            <TableCell>Value</TableCell>
                        </TableRow>
                    </TableHead>
                    {this.getGeneral().length ? (
                        <TableBody>
                            {this.getGeneral().map((item, index) => {
                                return (
                                    <TableRow key={index}>
                                        <TableCell>{item[0]}</TableCell>
                                        <TableCell>{item[1]}</TableCell>
                                    </TableRow>
                                )
                            })}
                        </TableBody>
                    ) : (
                        <TableBody>
                            <TableRow>
                                <TableCell>No Metadata</TableCell>
                            </TableRow>
                        </TableBody>
                    )}
                </Table>
            </div>
        )
    }
}

export default withStyles(styles)(MetadataTable);