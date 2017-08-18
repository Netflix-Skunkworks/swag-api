import React, {Component} from 'react';
import PropTypes from 'prop-types';

import {withStyles} from 'material-ui/styles';
import classnames from 'classnames';
import Card, {CardHeader, CardContent, CardActions} from 'material-ui/Card';
import Collapse from 'material-ui/transitions/Collapse';
import Avatar from 'material-ui/Avatar';
import IconButton from 'material-ui/IconButton';
import red from 'material-ui/colors/red';
import ExpandMoreIcon from 'material-ui-icons/ExpandMore';

import List, {ListItem, ListItemText} from 'material-ui/List';
import Table, {TableBody, TableCell, TableHead, TableRow} from 'material-ui/Table';

import PermIdentity from 'material-ui-icons/PermIdentity';
import Fingerprint from 'material-ui-icons/Fingerprint';
import Computer from 'material-ui-icons/Computer';
import BeachAccess from 'material-ui-icons/BeachAccess';
import Warning from 'material-ui-icons/Warning';
import Email from 'material-ui-icons/Email';
import Contacts from 'material-ui-icons/Contacts';
import Layers from 'material-ui-icons/Layers';
import SupervisorAccount from 'material-ui-icons/SupervisorAccount';

import CopyToClipboardButton from './CopyToClipboardButton';
import ServiceDialog from './ServiceDialog';
import JSONDialog from './JSONDialog';
import Tabs, {Tab} from 'material-ui/Tabs';


function TabContainer(props) {
    return (
        <div style={{padding: 20}}>
            {props.children}
        </div>
    );
}

TabContainer.propTypes = {
    children: PropTypes.node.isRequired,
};


const styles = theme => ({
    card: {
        margin: 10,
    },
    media: {
        height: 194,
    },
    expand: {
        transform: 'rotate(0deg)',
        transition: theme.transitions.create('transform', {
            duration: theme.transitions.duration.shortest,
        }),
    },
    expandOpen: {
        transform: 'rotate(180deg)',
    },
    avatar: {
        backgroundColor: red[500],
    },
    flexGrow: {
        flex: '1 1 auto',
    },
    generalItem: {
        width: '25%'
    }
});


class AccountCard extends Component {
    constructor(props, context) {
        super(props, context);
        this.state = {
            expanded: true,
            value: 0
        };

        this.handleExpandClick = this.handleExpandClick.bind(this);
    }

    handleExpandClick() {
        this.setState({expanded: !this.state.expanded});
    }

    handleChange = (event, value) => {
        this.setState({value});
    };


    render() {
        const classes = this.props.classes;
        const {value} = this.state;

        return (
            <div>
                <Card className={classes.card}>
                    <CardHeader
                        avatar={
                            <Avatar aria-label="Status" className={classes.avatar}>
                                {this.props.account.name.charAt(0).toUpperCase()}
                            </Avatar>
                        }
                        title={this.props.account.name}
                        subheader={this.props.account.description}
                    />
                    <Collapse in={this.state.expanded} transitionDuration="auto" unmountOnExit>
                        <CardContent>
                            <Tabs
                                value={this.state.value}
                                onChange={this.handleChange}
                                indicatorColor="primary"
                                textColor="primary"
                                centered
                            >
                                <Tab label="General"/>
                                <Tab label="Aliases"/>
                                <Tab label="Regions"/>
                            </Tabs>
                            {value === 0 &&
                            <TabContainer>
                                <List dense={true} style={{display: 'flex', flexWrap: 'wrap'}}>
                                    <ListItem className={classes.generalItem}>
                                        <CopyToClipboardButton button={<Fingerprint/>} text={this.props.account.id}/>
                                        <ListItemText primary={this.props.account.id} secondary="Id"/>
                                    </ListItem>
                                    <ListItem className={classes.generalItem}>
                                        <CopyToClipboardButton button={<Computer/>} text={this.props.account.provider}/>
                                        <ListItemText primary={this.props.account.provider} secondary="Provider"/>
                                    </ListItem>
                                    <ListItem className={classes.generalItem}>
                                        <CopyToClipboardButton button={<PermIdentity/>}
                                                               text={this.props.account.owner}/>
                                        <ListItemText primary={this.props.account.owner} secondary="Owner"/>
                                    </ListItem>
                                    <ListItem className={classes.generalItem}>
                                        <CopyToClipboardButton button={<BeachAccess/>}
                                                               text={this.props.account.environment}/>
                                        <ListItemText primary={this.props.account.environment}
                                                      secondary="Environment"/>
                                    </ListItem>
                                    <ListItem className={classes.generalItem}>
                                        <CopyToClipboardButton button={<Warning/>} text={this.props.account.sensitive}/>
                                        <ListItemText primary={this.props.account.sensitive ? 'Yes' : 'No'}
                                                      secondary="Sensitive"/>
                                    </ListItem>
                                    <ListItem className={classes.generalItem}>
                                        <CopyToClipboardButton button={<Email/>} text={this.props.account.email}/>
                                        <ListItemText primary={this.props.account.email} secondary="Email"/>
                                    </ListItem>
                                    <ListItem className={classes.generalItem}>
                                        <CopyToClipboardButton button={<Contacts/>} text={this.props.account.contacts}/>
                                        <ListItemText primary={this.props.account.contacts} secondary="Contacts"/>
                                    </ListItem>
                                    <ListItem className={classes.generalItem}>
                                        <CopyToClipboardButton button={<Layers/>} text={this.props.account.type}/>
                                        <ListItemText
                                            primary={this.props.account.type ? this.props.account.type : 'Unknown'}
                                            secondary="Type"/>
                                    </ListItem>
                                </List>
                            </TabContainer>}
                            {value === 1 &&
                            <TabContainer>
                                <List dense={true} style={{display: 'flex', flexWrap: 'wrap'}}>
                                    {this.props.account.aliases.map((alias, index) => {
                                        return (
                                            <ListItem key={index} className={classes.generalItem}>
                                                <CopyToClipboardButton button={<SupervisorAccount/>} text={alias}/>
                                                <ListItemText primary={alias}/>
                                            </ListItem>
                                        )
                                    })}
                                </List>
                            </TabContainer>
                            }
                            {value === 2 &&
                            <TabContainer>
                                <Table>
                                    <TableHead displaySelectAll={false} adjustForCheckbox={false}>
                                        <TableRow>
                                            <TableCell>Region</TableCell>
                                            <TableCell>Status</TableCell>
                                        </TableRow>
                                    </TableHead>
                                    <TableBody displayRowCheckbox={false}>
                                        <TableRow>
                                            <TableCell>us-east-1</TableCell>
                                            <TableCell>Created</TableCell>
                                        </TableRow>
                                        <TableRow>
                                            <TableCell>us-west-2</TableCell>
                                            <TableCell>Created</TableCell>
                                        </TableRow>
                                        <TableRow>
                                            <TableCell>eu-west-1</TableCell>
                                            <TableCell>Created</TableCell>
                                        </TableRow>
                                    </TableBody>
                                </Table>
                            </TabContainer>
                            }
                        </CardContent>
                    </Collapse>
                    <CardActions disableActionSpacing>
                        <ServiceDialog services={this.props.account.services}/>
                        <JSONDialog data={this.props.account}/>
                        <div className={classes.flexGrow}/>
                        <IconButton
                            className={classnames(classes.expand, {
                                [classes.expandOpen]: this.state.expanded,
                            })}
                            onClick={this.handleExpandClick}
                            aria-expanded={this.state.expanded}
                            aria-label="Show more"
                        >
                            <ExpandMoreIcon/>
                        </IconButton>
                    </CardActions>
                </Card>
            </div>
        );
    }
}

AccountCard.propTypes = {
    classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(AccountCard);