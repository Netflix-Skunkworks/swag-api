import React, {Component} from 'react';
import AppBar from 'material-ui/AppBar';

import getMuiTheme from 'material-ui/styles/getMuiTheme';

import injectTapEventPlugin from 'react-tap-event-plugin';

import Search from './Search';
import Error from './Error';

import {
    blue300,
} from 'material-ui/styles/colors';

import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';

// Needed for onTouchTap
// http://stackoverflow.com/a/34015469/988941
injectTapEventPlugin();

const muiTheme = getMuiTheme({
    palette: {
        accent1Color: blue300,
    },
});

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
                    <SWAGAppBar/>
                    {this.state.error ? <Error/> : <Search data={this.state.accounts} loading={this.state.loading}/>}
                </div>
            </MuiThemeProvider>
        );
    }
}
