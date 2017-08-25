import React from 'react';
import {CircularProgress} from 'material-ui/Progress';
import {withStyles} from 'material-ui/styles';
import fuzzyFilterFactory from './FuzzyFilterFactory';

import AccountCard from './AccountCard';

const {InputFilter, FilterResults} = fuzzyFilterFactory();


const styles = theme => ({
    search: {
        display: 'flex',
        flexDirection: 'row',
        justifyContent: 'flex-end'
    },
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

const fuseConfig = {
    keys: [
        {
            name: 'name',
            weight: 0.8
        },
        {
            name: 'environment',
            weight: 0.3

        }, {
            name: 'id',
            weight: 0.8

        }, {
            name: 'sensitive',
            weight: 0.4

        }, {
            name: 'owner',
            weight: 0.7

        }, {
            name: 'provider',
            weight: 0.2

        }, {
            name: 'tags',
            weight: 0.5

        }, {
            name: 'aliases',
            weight: 0.6

        }, {
            name: 'contacts',
            weight: 0.3

        }, {
            name: 'email',
            weight: 0.7

        }],
    threshold: 0.6,
    distance: 100,
    tokenize: true,
    shouldSort: true,
    matchAllTokens: true
};

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

class Search extends React.Component {
    render() {
        const classes = this.props.classes;

        return (
            <div className={classes.container}>
                <InputFilter className={classes.search} keys={fuseConfig.keys} debounceTime={200}/>
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

export default withStyles(styles)(Search);
