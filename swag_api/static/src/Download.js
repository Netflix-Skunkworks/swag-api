import React, {Component} from 'react';
import IconButton from 'material-ui/IconButton';
import FileDownload from 'material-ui-icons/FileDownload';
import {CSVLink} from 'react-csv';

import {connect} from 'react-refetch';


class Download extends Component {
    getCSVData(accounts) {
        let columns = ['id', 'contacts', 'aliases', 'email', 'name', 'sensitive', 'owner', 'provider', 'descriptions', 'tags', 'environment'];
        accounts.forEach((value) => {
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

    render() {
        const {accountFetch} = this.props;

        if (accountFetch.fulfilled) {
            return (
                <IconButton color="contrast" aria-label="Download">
                    <CSVLink filename={"accounts.csv"} data={this.getCSVData(accountFetch.value)}><FileDownload
                        style={{fill: 'white'}}/></CSVLink>
                </IconButton>
            )
        }
        return <div></div>
    }
}


export default connect(props => {
    return {
        accountFetch: `/api/1/accounts`
    }
})(Download)