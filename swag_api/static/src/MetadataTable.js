import React, {Component} from 'react';
import Subheader from 'material-ui/Subheader';
import {Table, TableBody, TableHeader, TableHeaderColumn, TableRow, TableRowColumn} from 'material-ui/Table';


class MetadataTable extends Component {
    render() {
        return (
            <div>
                <Subheader>Service Metadata</Subheader>
                <Table>
                    <TableHeader displaySelectAll={false} adjustForCheckbox={false}>

                        <TableRow>
                            <TableHeaderColumn>Key</TableHeaderColumn>
                            <TableHeaderColumn>Value</TableHeaderColumn>
                        </TableRow>
                    </TableHeader>
                    <TableBody displayRowCheckbox={false}>
                        {Object.entries(this.props.data).map(([key, value]) => {
                            return (
                                <TableRow>
                                    <TableRowColumn>{key}</TableRowColumn>
                                    <TableRowColumn>{value}</TableRowColumn>
                                </TableRow>
                            )
                        })}
                    </TableBody>
                </Table>
            </div>
        )
    }
}

export default MetadataTable;