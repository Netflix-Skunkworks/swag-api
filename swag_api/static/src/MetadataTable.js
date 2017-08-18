import React, {Component} from 'react';
import { withStyles } from 'material-ui/styles';

import Table, {TableBody, TableCell, TableHead, TableRow} from 'material-ui/Table';

import CopyToClipboardButton from './CopyToClipboardButton';


const styles = theme => ({});

class MetadataTable extends Component {
    render() {
        return (
            <div>
                <Table>
                    <TableHead displaySelectAll={false} adjustForCheckbox={false}>
                        <TableRow>
                            <TableCell>Key</TableCell>
                            <TableCell>Value</TableCell>
                            <TableCell/>
                        </TableRow>
                    </TableHead>
                    <TableBody displayRowCheckbox={false}>
                        {Object.entries(this.props.data).map(([key, value]) => {
                            return (
                                <TableRow key={key}>
                                    <TableCell>{key}</TableCell>
                                    <TableCell>{value}</TableCell>
                                    <TableCell>
                                        <CopyToClipboardButton text={value}/>
                                    </TableCell>
                                </TableRow>
                            )
                        })}
                    </TableBody>
                </Table>
            </div>
        )
    }
}

export default withStyles(styles)(MetadataTable);