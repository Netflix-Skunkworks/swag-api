import React, {Component} from 'react';
import CircularProgress from 'material-ui/CircularProgress';
import fuzzyFilterFactory from './FuzzyFilterFactory';

import AccountCard from './AccountCard';

const {InputFilter, FilterResults} = fuzzyFilterFactory();


const styles = {
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
};

const fuseConfig = {
    keys: ['environment', 'id', 'sensitive', 'owner', 'provider', 'tags', 'aliases', 'contacts'],
    threshold: 0.6,
    distance: 100,
    shouldSort: true
};

const prefilters = [
    {
        regex: /\S+:\S+/g,
        handler: (match, items, Fuse) => {
            const [key, value] = match.split(':');
            const preConfig = fuseConfig;
            preConfig.keys = [key];
            const fuse = new Fuse(items, preConfig);
            return fuse.search(value);
        }
    }
];

class Search extends Component {
    render() {
        return (
            <div style={styles.container}>
                <InputFilter style={styles.search} debounceTime={200}/>
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
                    <div style={styles.loadingProgress}><CircularProgress size={80} thickness={5}/></div> : null}
            </div>
        );
    }
}

export default Search;
