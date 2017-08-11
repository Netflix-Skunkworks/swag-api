import React, {Component} from 'react';

import Avatar from 'material-ui/Avatar';
import {List, ListItem} from 'material-ui/List';
import {Card, CardActions, CardHeader, CardText} from 'material-ui/Card';
import Subheader from 'material-ui/Subheader';

import PermIdentity from 'material-ui/svg-icons/action/perm-identity';
import Fingerprint from 'material-ui/svg-icons/action/fingerprint';
import Computer from 'material-ui/svg-icons/hardware/computer';
import BeachAccess from 'material-ui/svg-icons/places/beach-access';
import Warning from 'material-ui/svg-icons/alert/warning';
import Email from 'material-ui/svg-icons/communication/email';
import Contacts from 'material-ui/svg-icons/communication/contacts';

import {
    red500,
    yellow500,
    green500,
    lightBlue500,
    brown500,
    blueGrey500,
    white
} from 'material-ui/styles/colors';

import CopyToClipboardButton from './CopyToClipboardButton';
import ServiceDialog from './ServiceDialog';


const styles = {
    dualList: {
        display: 'flex',
        justifyContent: 'space-evenly'
    },
    listItem: {
        flexGroup: 0
    }
};

class StatusAvatar extends Component {
    avatarColor(status) {
        if (status === "created") {
            return lightBlue500;
        } else if (status === "in-progress") {
            return yellow500;
        } else if (status === "ready") {
            return green500;
        } else if (status === "deprecated") {
            return brown500;
        } else if (status === "deleted") {
            return red500;
        } else if (status === "in-active") {
            return blueGrey500;
        } else {
            return lightBlue500;
        }
    }

    render() {
        return (
            <Avatar
                color={white}
                backgroundColor={this.avatarColor(this.status)}
                style={{marginRight: '10px'}}
            />
        )
    }
}

class AccountCard extends Component {
    constructor(props, context) {
        super(props, context);

        this.account = props.data;

        this.handleExpandChange = this.handleExpandChange.bind(this);
        this.handleToggle = this.handleToggle.bind(this);
        this.handleExpand = this.handleExpand.bind(this);
        this.handleReduce = this.handleReduce.bind(this);

        this.state = {
            expanded: false
        };
    }

    handleExpandChange(expanded) {
        this.setState({expanded: expanded});
    };

    handleToggle(toggle) {
        this.setState({expanded: toggle});
    };

    handleExpand() {
        this.setState({expanded: true});
    };

    handleReduce() {
        this.setState({expanded: false});
    };

    render() {
        return (
            <div>
                <Card expanded={this.state.expanded} onExpandChange={this.handleExpandChange}>
                    <CardHeader
                        title={this.account.name}
                        subtitle={this.account.description}
                        avatar={<StatusAvatar/>}
                        actAsExpander={true}
                        showExpandableButton={true}
                    />
                    <CardText expandable={true}>
                        <div style={styles.dualList}>
                            <List style={styles.listItem}>
                                <Subheader>General</Subheader>
                                <ListItem
                                    primaryText={this.account.id}
                                    secondaryText="Account Id"
                                    leftIcon={<Fingerprint/>}
                                    disabled={true}
                                />
                                <ListItem
                                    primaryText={this.account.provider}
                                    secondaryText="Account Provider"
                                    leftIcon={<Computer/>}
                                    disabled={true}
                                />
                                <ListItem
                                    primaryText={this.account.owner}
                                    secondaryText="Account Owner"
                                    leftIcon={<PermIdentity/>}
                                    disabled={true}
                                />
                                <ListItem
                                    primaryText={this.account.environment}
                                    secondaryText="Environment"
                                    leftIcon={<BeachAccess/>}
                                    disabled={true}
                                />
                                <ListItem
                                    primaryText={this.account.sensitive ? 'Yes' : 'No'}
                                    secondaryText="Sensitive"
                                    leftIcon={<Warning/>}
                                    disabled={true}
                                />
                                <ListItem
                                    primaryText={this.account.email}
                                    secondaryText="Email"
                                    leftIcon={<Email/>}
                                    disabled={true}
                                />
                                <ListItem
                                    primaryText={this.account.contacts}
                                    secondaryText="Contacts"
                                    leftIcon={<Contacts/>}
                                    disabled={true}

                                />
                            </List>
                            <List style={styles.listItem}>
                                <Subheader>Services</Subheader>
                                {this.account.services.map((service, index) => {
                                    return (
                                        <ServiceDialog key={index} data={service}/>
                                    )
                                })}
                            </List>
                            <List style={styles.listItem}>
                                <Subheader>Aliases</Subheader>
                                {this.account.aliases.map((alias, index) => {
                                    return (
                                        <ListItem
                                            key={index}
                                            primaryText={alias}
                                            disabled={true}
                                        />
                                    )
                                })}
                            </List>
                            <List style={styles.listItem}>
                                <Subheader>Status</Subheader>
                            </List>
                        </div>
                    </CardText>
                    <CardActions>
                        <CopyToClipboardButton tooltip="Copy AccountId" text={this.account.id}/>
                    </CardActions>
                </Card>
            </div>
        );
    }
}

export default AccountCard;