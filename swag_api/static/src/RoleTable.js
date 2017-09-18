import React, {Component} from 'react';
import {withStyles} from 'material-ui/styles';
import Button from 'material-ui/Button';

import Table, {TableBody, TableCell, TableHead, TableRow} from 'material-ui/Table';
import Typography from 'material-ui/Typography';


const styles = theme => ({});

class RoleTable extends Component {
    render() {
        let roles = this.props.data ? this.props.data : [];
        return (
            <div>
                <Typography type="subheading" gutterBottom>
                    Roles
                </Typography>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell>Role Name</TableCell>
                            <TableCell>Approver</TableCell>
                            <TableCell>Google Group</TableCell>
                            <TableCell></TableCell>
                        </TableRow>
                    </TableHead>
                    {roles.length ? (
                        <TableBody>
                            {roles.map((item, index) => {
                                return (
                                    <TableRow key={index}>
                                        <TableCell>{item['roleName']}</TableCell>
                                        <TableCell>{item['secondaryApprover']}</TableCell>
                                        <TableCell>{item['googleGroup']}</TableCell>
                                        <TableCell>
                                            <Button href={item['policyUrl']}>
                                                Policy
                                            </Button>
                                        </TableCell>
                                    </TableRow>
                                )
                            })}
                        </TableBody>
                    ) : (
                        <TableBody>
                            <TableRow>
                                <TableCell>No Roles</TableCell>
                            </TableRow>
                        </TableBody>
                    )}
                </Table>
            </div>
        )
    }
}

export default withStyles(styles)(RoleTable);