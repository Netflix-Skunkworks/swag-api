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
import Layers from 'material-ui/svg-icons/maps/layers';

import {
    red500,
    yellow500,
    green500,
    blue300,
    brown500,
    blueGrey500,
    white
} from 'material-ui/styles/colors';

import CopyToClipboardButton from './CopyToClipboardButton';
import ServiceDialog from './ServiceDialog';
import AccountStatusStepper from './Status';


const styles = {
    dualList: {
        display: 'flex',
        justifyContent: 'flex-start',
        flexWrap: 'wrap'
    },
    listItem: {
        flexGroup: 0
    }
};

class StatusAvatar extends Component {
    avatarColor(status) {
        switch (status) {
            case 'created':
                return blue300;
            case 'in-progress':
                return yellow500;
            case 'ready':
                return green500;
            case 'deprecated':
                return brown500;
            case 'deleted':
                return red500;
            case 'in-active':
                return blueGrey500;
            default:
                return blue300;
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
                        title={this.props.account.name}
                        subtitle={this.props.account.description}
                        avatar={<StatusAvatar/>}
                        actAsExpander={true}
                        showExpandableButton={true}
                    />
                    <CardText expandable={true}>
                        <div style={styles.dualList}>
                            <List style={styles.listItem}>
                                <Subheader>General</Subheader>
                                <ListItem
                                    primaryText={this.props.account.id}
                                    secondaryText="Account Id"
                                    leftIcon={<Fingerprint/>}
                                    disabled={true}
                                />
                                <ListItem
                                    primaryText={this.props.account.provider}
                                    secondaryText="Account Provider"
                                    leftIcon={<Computer/>}
                                    disabled={true}
                                />
                                <ListItem
                                    primaryText={this.props.account.owner}
                                    secondaryText="Account Owner"
                                    leftIcon={<PermIdentity/>}
                                    disabled={true}
                                />
                                <ListItem
                                    primaryText={this.props.account.environment}
                                    secondaryText="Environment"
                                    leftIcon={<BeachAccess/>}
                                    disabled={true}
                                />
                                <ListItem
                                    primaryText={this.props.account.sensitive ? 'Yes' : 'No'}
                                    secondaryText="Sensitive"
                                    leftIcon={<Warning/>}
                                    disabled={true}
                                />
                                <ListItem
                                    primaryText={this.props.account.email}
                                    secondaryText="Email"
                                    leftIcon={<Email/>}
                                    disabled={true}
                                />
                                <ListItem
                                    primaryText={this.props.account.contacts}
                                    secondaryText="Contacts"
                                    leftIcon={<Contacts/>}
                                    disabled={true}

                                />
                                <ListItem
                                    primaryText={this.props.account.type}
                                    secondaryText="Type"
                                    leftIcon={<Layers/>}
                                    disabled={true}

                                />
                            </List>
                            <List style={styles.listItem}>
                                <Subheader>Status</Subheader>
                                <AccountStatusStepper status='created'/>
                            </List>
                            <List style={styles.listItem}>
                                <Subheader>Aliases</Subheader>
                                {this.props.account.aliases.map((alias, index) => {
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
                                <Subheader>Services</Subheader>
                                {this.props.account.services.map((service, index) => {
                                    return (
                                        <ServiceDialog key={index} data={service}/>
                                    )
                                })}
                            </List>
                        </div>
                    </CardText>
                    <CardActions>
                        <CopyToClipboardButton tooltip="Copy Account Id" text={this.props.account.id}/>
                    </CardActions>
                </Card>
            </div>
        );
    }
}

export default AccountCard;