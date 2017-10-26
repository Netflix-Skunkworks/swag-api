import React, {Component} from 'react';
import IconButton from 'material-ui/IconButton';
import FileDownload from 'material-ui-icons/FileDownload';
import {CSVLink} from 'react-csv';
import PropTypes from 'prop-types';
import Tooltip from 'material-ui/Tooltip';


function filterData(data) {
    let columns = ['id', 'contacts', 'aliases', 'email', 'name', 'sensitive', 'owner', 'provider', 'descriptions', 'tags', 'environment'];
    let arrCopy = JSON.parse(JSON.stringify(data));
    arrCopy.forEach((value) => {
        let account = {};
        Object.entries(value).forEach(([key, value]) => {
            if (columns.includes(key)) {
                account[key] = value;
            }
        });
        arrCopy.push(account);
    });
    return arrCopy;
}


class Download extends Component {
    render() {
        const {data} = this.props;

        if (data.fulfilled) {
            return (
                <Tooltip title="Download CSV">
                    <IconButton color="contrast" aria-label="Download">
                        <CSVLink filename={"data.csv"} data={filterData(data.value)}>
                            <FileDownload style={{fill: 'white'}}/>
                        </CSVLink>
                    </IconButton>
                </Tooltip>
            )
        }

        return (
            <IconButton color="contrast" aria-label="Download">
                <FileDownload style={{fill: 'white'}}/>
            </IconButton>
        )
    }
}

Download.propTypes = {
    data: PropTypes.object.isRequired,
};

export default Download;
