import React, {Component} from 'react';
import {withStyles} from 'material-ui/styles';

import Table, {TableBody, TableCell, TableHead, TableRow} from 'material-ui/Table';
import Typography from 'material-ui/Typography';


import CopyToClipboardButton from './CopyToClipboardButton';


const styles = theme => ({});

class MetadataTable extends Component {
    getGeneral() {
        return Object.entries(this.props.data).filter(([key, value]) => {
            return !Array.isArray(value);
        });
    }

    getSubTables() {
        return Object.entries(this.props.data).filter(([key, value]) => {
            return Array.isArray(value);
        });
    }

    render() {
        return (
            <div>
                <Typography type="subheading" gutterBottom>
                    General
                </Typography>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell>Key</TableCell>
                            <TableCell>Value</TableCell>
                            <TableCell/>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {this.getGeneral().map((item, index) => {
                            return (
                                <TableRow key={index}>
                                    <TableCell>{item[0]}</TableCell>
                                    <TableCell>{item[1]}</TableCell>
                                    <TableCell>
                                        <CopyToClipboardButton text={item[1]}/>
                                    </TableCell>
                                </TableRow>
                            )
                        })}
                    </TableBody>
                </Table>
                {this.getSubTables().map((item) => {
                    return item[1].map((value, index) => {
                        return (
                            <Table key={index}>
                                <TableHead>
                                    <TableRow>
                                        <TableCell>Key</TableCell>
                                        <TableCell>Value</TableCell>
                                        <TableCell/>
                                    </TableRow>
                                </TableHead>
                                <TableBody>
                                    {Object.entries(value).map(([key, value], index) => {
                                        return (
                                            <TableRow key={index}>
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
                        )
                    })
                })}
            </div>
        )
    }
}

export default withStyles(styles)(MetadataTable);