import React from 'react';
import {MuiThemeProvider, createMuiTheme} from 'material-ui/styles';
import createPalette from 'material-ui/styles/palette';
import blue from 'material-ui/colors/blue';
import pink from 'material-ui/colors/pink';
import red from 'material-ui/colors/red';

import AppTabs from './AppTabs';


const theme = createMuiTheme({
    palette: createPalette({
        primary: blue,
        accent: {
            ...pink,
            A400: '#00e677',
        },
        error: red,
    }),
});

function Palette() {
    return (
        <MuiThemeProvider theme={theme}>
            <AppTabs/>
        </MuiThemeProvider>
    );
}

export default Palette;