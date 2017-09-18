import React from 'react';
import {MuiThemeProvider, createMuiTheme} from 'material-ui/styles';
import blue from 'material-ui/colors/blue';
import pink from 'material-ui/colors/pink';
import red from 'material-ui/colors/red';

import AppToolbar from './AppToolbar';


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


function Palette() {
    return (
        <MuiThemeProvider theme={theme}>
            <AppToolbar/>
        </MuiThemeProvider>
    );
}

export default Palette;