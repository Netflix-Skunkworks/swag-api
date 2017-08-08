import React, {Component} from 'react';
import AppBar from 'material-ui/AppBar';
import fuzzyFilterFactory from './FuzzyFilterFactory';

import getMuiTheme from 'material-ui/styles/getMuiTheme';
import {Card, CardActions, CardHeader, CardMedia, CardText} from 'material-ui/Card';
import {Table, TableBody, TableHeader, TableHeaderColumn, TableRow, TableRowColumn} from 'material-ui/Table';
import Subheader from 'material-ui/Subheader';
import Avatar from 'material-ui/Avatar';
import Dialog from 'material-ui/Dialog';
import FlatButton from 'material-ui/FlatButton';
import {List, ListItem} from 'material-ui/List';
import CircularProgress from 'material-ui/CircularProgress';

import ActionGrade from 'material-ui/svg-icons/action/grade';
import PermIdentity from 'material-ui/svg-icons/action/perm-identity';
import Fingerprint from 'material-ui/svg-icons/action/fingerprint';
import Computer from 'material-ui/svg-icons/hardware/computer';
import BeachAccess from 'material-ui/svg-icons/places/beach-access';
import Warning from 'material-ui/svg-icons/alert/warning';
import Email from 'material-ui/svg-icons/communication/email';
import Contacts from 'material-ui/svg-icons/communication/contacts';

import injectTapEventPlugin from 'react-tap-event-plugin';

import {
    blue300,
    red500,
    yellow500,
    green500,
    gray500,
    white
} from 'material-ui/styles/colors';

import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';

// Needed for onTouchTap
// http://stackoverflow.com/a/34015469/988941
injectTapEventPlugin();

const {InputFilter, FilterResults} = fuzzyFilterFactory();

const muiTheme = getMuiTheme({
    palette: {
        accent1Color: blue300,
    },
});

const styles = {
    container: {
        padding: '16px',
        fontWeight: '500',
        boxSizing: 'border-box',
        position: 'relative',
        whiteSpace: 'nowrap'
    },
    search: {
        display: 'flex',
        flexDirection: 'row',
        justifyContent: 'flex-end'
    },
    dualList: {
        display: 'flex',
        justifyContent: 'space-evenly'
    },
    listItem: {
        flexGroup: 0
    },
    loadingProgress: {
        height: '100%',
        padding: '0',
        margin: '0',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center'
    },
    uppercase: {
        textTransform: 'uppercase'
    }
};

const fuseConfig = {
        keys: ['environment', 'id', 'sensitive', 'owner', 'provider', 'tags'],
        threshold: 0.2,
        distance: 100
    };

const prefilters = [
    {
        regex: /\S+:\S+/g,
        handler: (match, items, Fuse) => {
            const [key, value] = match.split(':');
            const preConfig = fuseConfig;
            preConfig.keys = [key];
            const fuse = new Fuse(items, preConfig);
            return fuse.search(value);
        }
    }
];


class Search extends Component {
    render() {
        return (
            <div style={styles.container}>
                <InputFilter style={styles.search} debounceTime={200}/>
                <FilterResults
                    items={this.props.data}
                    fuseConfig={fuseConfig}
                    prefilters={prefilters}
                >
                    {filteredItems => {
                        return (
                            <div>
                                {filteredItems.map((item) => <AccountCard key={item.id} data={item}/>) }
                            </div>
                        )
                    }}
                </FilterResults>
                {this.props.loading ? <div style={styles.loadingProgress}><CircularProgress size={80} thickness={5} /></div> : null }
            </div>
        );
    }
}

class Error extends Component {
    constructor(props, context) {
        super(props, context);
        this.handleRetry = this.handleRetry.bind(this);
    }

    handleRetry = () => {
        this.setState({open: true});
    };

    render() {
        return (
            <Card>
                <CardHeader
                    title="Error"
                    subtitle="Something has gone terribly wrong"
                />
                <CardMedia>
                </CardMedia>
                <CardText>
                    SWAG isn't acting like itself at the moment, would you like to retry?
                </CardText>
                <CardActions>
                    <FlatButton label="Retry" onTouchTap={this.handleRetry}/>
                </CardActions>
            </Card>
        )
    }
}


class MetadataTable extends Component {
    render() {
        return (
            <div>
                <Subheader>Metadata</Subheader>
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

class ServiceDialog extends Component {
    constructor(props, context) {
        super(props, context);
        this.handleOpen = this.handleOpen.bind(this);
        this.handleClose = this.handleClose.bind(this);

        this.state = {
            open: false,
        };

    }

    handleOpen = () => {
        this.setState({open: true});
    };

    handleClose = () => {
        this.setState({open: false});
    };

    render() {
        const actions = [
            <FlatButton
                label="Close"
                primary={true}
                onTouchTap={this.handleClose}
            />,
        ];

        let metadata = this.props.data.metadata ? this.props.data.metadata : {};

        return (
            <div>
                <ListItem
                    onTouchTap={this.handleOpen}
                    primaryText={this.props.data.name}
                    leftIcon={<ActionGrade />}
                />
                <Dialog
                    title="Details"
                    actions={actions}
                    modal={false}
                    open={this.state.open}
                    onRequestClose={this.handleClose}
                >
                <MetadataTable data={metadata}/>
                </Dialog>
            </div>
        );
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
            expanded: false,
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

    avatarColor(status) {
        if (status === "not ready") {
            return red500
        } else if (status === "in progress") {
            return yellow500
        } else if (status === "ready") {
            return green500
        } else {
            return gray500
        }
    }

    render() {
        return (
            <div>
                <Card expanded={this.state.expanded} onExpandChange={this.handleExpandChange}>
                    <CardHeader
                        title={this.account.name}
                        subtitle={this.account.description}
                        avatar={
                            <Avatar
                                color={white}
                                backgroundColor={this.avatarColor(this.status)}
                            />
                        }
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
                                    leftIcon={<Fingerprint />}
                                    disabled={true}
                                />
                                <ListItem
                                    primaryText={this.account.provider}
                                    secondaryText="Account Provider"
                                    leftIcon={<Computer />}
                                    disabled={true}
                                />
                                <ListItem
                                    primaryText={this.account.owner}
                                    secondaryText="Account Owner"
                                    leftIcon={<PermIdentity />}
                                    disabled={true}
                                />
                                <ListItem
                                    primaryText={this.account.environment}
                                    secondaryText="Environment"
                                    leftIcon={<BeachAccess />}
                                    disabled={true}
                                />
                                <ListItem
                                    primaryText={this.account.sensitive ? 'Yes': 'No'}
                                    secondaryText="Sensitive"
                                    leftIcon={<Warning />}
                                    disabled={true}
                                />
                                <ListItem
                                    primaryText={this.account.email}
                                    secondaryText="Email"
                                    leftIcon={<Email />}
                                    disabled={true}
                                />
                                <ListItem
                                    primaryText={this.account.contacts}
                                    secondaryText="Contacts"
                                    leftIcon={<Contacts />}
                                    disabled={true}

                                />
                            </List>
                            <List style={styles.listItem}>
                                <Subheader>Services</Subheader>
                                {this.account.services.map((service, index) => {
                                    return (
                                        <ServiceDialog key={index} data={service} />
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
                </Card>
            </div>
        );
    }
}

const SWAGAppBar = () => (
    <AppBar
        title="SWAG"
    />
);

export default class Main extends Component {
    constructor(props, context) {
        super(props, context);

        this.handleRequestClose = this.handleRequestClose.bind(this);
        this.handleTouchTap = this.handleTouchTap.bind(this);

        this.state = {
            open: false,
            accounts: [],
            loading: true,
            error: false
        };
    }

    handleRequestClose() {
        this.setState({
            open: false,
        });
    }

    componentDidMount() {
        let myRequest = new Request('/api/1/accounts');
        fetch(myRequest).then((response) => {
            this.setState({loading: false});
            if (response.ok) {
                response.json().then((json) => {
                    this.setState({accounts: json});
                });
            } else {
                this.setState({error: true})
            }
        });
    }

    handleTouchTap() {
        this.setState({
            open: true,
        });
    }

    render() {
        return (
            <MuiThemeProvider muiTheme={muiTheme}>
                <div>
                    <SWAGAppBar />
                    {this.state.error ? <Error/> : <Search data={this.state.accounts} loading={this.state.loading}/>}
                </div>
            </MuiThemeProvider>
        );
    }
}
