import React from 'react';
import {MuiThemeProvider, createMuiTheme} from 'material-ui/styles';
import blue from 'material-ui/colors/blue';
import pink from 'material-ui/colors/pink';
import red from 'material-ui/colors/red';

import { connect } from 'react-refetch';

import AppToolbar from './AppToolbar';
import AppSearchResults from './AppSearchResults';

//import 'typeface-roboto';


const theme = createMuiTheme({
    palette: {
        primary: blue,
        accent: {
            ...pink,
            A400: '#00e677',
        },
        error: red,
    },
});


class Main extends React.Component {
    constructor(props, context) {
        super(props, context);
        this.state = {
            search: '',
            namespace: 'accounts',
        };
    }

    render() {
        const {dataFetch} = this.props
        return (
            <div>
                <MuiThemeProvider theme={theme}>
                    <div style={{width: '100%'}}>
                        <AppToolbar search={this.state.search} data={dataFetch} namespace={this.state.namespace}/>
                        <AppSearchResults search={this.state.search} data={dataFetch}/>
                    </div>
                </MuiThemeProvider>
            </div>
        );
    }
}

export default connect(props => {
    return {
        dataFetch: `/api/1/accounts`
    }
})(Main);
