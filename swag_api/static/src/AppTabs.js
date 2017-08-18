import React, {Component} from 'react';
import PropTypes from 'prop-types';
import {withStyles} from 'material-ui/styles';
import Tabs, {Tab} from 'material-ui/Tabs';
import AppBar from 'material-ui/AppBar';
import Button from 'material-ui/Button';
import Snackbar,{ SnackbarContent } from 'material-ui/Snackbar';

import AccountBox from 'material-ui-icons/AccountBox';

import Search from './Search';

const styles = theme => ({});

function TabContainer(props) {
    return (
        <div style={{padding: 20}}>
            {props.children}
        </div>
    );
}

TabContainer.propTypes = {
    children: PropTypes.node.isRequired
}


const action = (
  <Button color="accent" dense>
    Retry
  </Button>
);


class AppTabs extends Component {
    constructor(props, context) {
        super(props, context);

        this.state = {
            accounts: [],
            loading: true,
            error: false,
            value: 0
        };
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

    handleChange(event, value) {
        this.setState({value});
    }

    render() {
        const {value} = this.state;

        return (
            <div>
                <Snackbar
                    open={this.state.error}
                >
                    <SnackbarContent
                        message="Error fetching account data. "
                        action={action}
                    />
                </Snackbar>
                <AppBar position="static">
                    <Tabs
                        value={value}
                        onChange={this.handleChange}
                        centered
                    >
                        <Tab
                            icon={<AccountBox/>}
                            label="Accounts">
                        </Tab>
                    </Tabs>
                </AppBar>
                    {value === 0 &&
                        <TabContainer>
                            <Search data={this.state.accounts} loading={this.state.loading}/>
                        </TabContainer>
                    }
            </div>
        );
    }
}


export default withStyles(styles)(AppTabs);