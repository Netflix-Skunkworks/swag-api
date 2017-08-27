import React from 'react';
import {CircularProgress} from 'material-ui/Progress';
import {withStyles} from 'material-ui/styles';

import {fuseConfig, FilterResults} from './AppSearch';

import AccountCard from './AccountCard';


const styles = theme => ({
    container: {
        padding: '16px',
        fontWeight: '500',
        boxSizing: 'border-box',
        position: 'relative',
        whiteSpace: 'nowrap'
    },
    loadingProgress: {
        height: '100%',
        padding: '0',
        margin: '0',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center'
    }
});


const prefilters = [
    {
        regex: /.*:.*/g,
        handler: (match, items, Fuse) => {
            const [key, value] = match.split(':');
            const fuse = new Fuse(items, {keys: [key], threshold: 0.6, shouldSort: true, distance: 100});
            return fuse.search(value.trim());
        }
    }
];

class AppSearchResults extends React.Component {
    render() {
        const classes = this.props.classes;

        return (
            <div className={classes.container}>
                <FilterResults
                    items={this.props.data}
                    fuseConfig={fuseConfig}
                    prefilters={prefilters}
                >
                    {filteredItems => {
                        return (
                            <div>
                                {filteredItems.map((item) => <AccountCard key={item.id} account={item}/>)}
                            </div>
                        )
                    }}
                </FilterResults>
                {this.props.loading ?
                    <div className={classes.loadingProgress}><CircularProgress size={80}/></div> : null}
            </div>
        );
    }
}

export default withStyles(styles)(AppSearchResults);
