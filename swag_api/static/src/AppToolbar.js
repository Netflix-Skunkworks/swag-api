import React, {Component} from 'react';
import {withStyles} from 'material-ui/styles';
import AppBar from 'material-ui/AppBar';
import Button from 'material-ui/Button';
import Snackbar, {SnackbarContent} from 'material-ui/Snackbar';
import Toolbar from 'material-ui/Toolbar';
import Typography from 'material-ui/Typography';
import IconButton from 'material-ui/IconButton';
import FileDownload from 'material-ui-icons/FileDownload';
import {CSVLink} from 'react-csv';


import AppSearch from './AppSearch';
import AppSearchResults from './AppSearchResults';


const styles = theme => ({
    root: {
        width: '100%',
    },
    flex: {
        flex: 1,
    },
});

const action = (
    <Button color="accent" dense>
        Retry
    </Button>
);


class AppToolbar extends Component {
    constructor(props, context) {
        super(props, context);

        this.state = {
            accounts: [],
            loading: true,
            error: false,
            value: 0
        };
    }

    getCSVData() {
        let columns = ['id', 'contacts', 'aliases', 'email', 'name', 'sensitive', 'owner', 'provider', 'descriptions', 'tags', 'environment'];
        let accounts = [];
        this.state.accounts.forEach((value) => {
            let account = {};
            Object.entries(value).forEach(([key, value]) => {
                if (columns.includes(key)) {
                    account[key] = value;
                }
            });
            accounts.push(account);
        });
        return accounts;
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
                this.setState({error: true});
            }
        });
    }

    render() {
        const classes = this.props.classes;

        return (
            <div className={classes.root}>
                <Snackbar
                    open={this.state.error}
                >
                    <SnackbarContent
                        message="Error fetching account data. "
                        action={action}
                    />
                </Snackbar>
                <AppBar position="static">
                    <Toolbar>
                        <Typography type="title" color="inherit" className={classes.flex}>
                            SWAG
                        </Typography>
                        <AppSearch/>
                        <IconButton color="contrast" aria-label="Download">
                            <CSVLink filename={"accounts.csv"} data={this.getCSVData()}><FileDownload
                                style={{fill: 'white'}}/></CSVLink>
                        </IconButton>
                    </Toolbar>
                </AppBar>
                <AppSearchResults data={this.state.accounts} loading={this.state.loading}/>
            </div>
        );
    }
}


export default withStyles(styles)(AppToolbar);