import React, {Component} from 'react';

import {connect} from 'react-refetch';

import {fuseConfig, FilterResults} from './AppSearch';

import AccountCard from './AccountCard';
import Error from './Error';
import ResultLoader from './ResultLoader';


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


class AppSearchResults extends Component {
    render() {
        const {resultFetch} = this.props;
        if (resultFetch.pending) {
            return <ResultLoader/>;
        } else if (resultFetch.rejected) {
            return <Error status={resultFetch.rejected}/>;
        } else if (resultFetch.fulfilled) {
            return <FilterResults
                items={resultFetch.value}
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
        }
    }
}

export default connect(props => {
    const url = '/api/1/accounts';
    return {
        resultFetch: url,
        refreshFetch: () => ({
            resultFetch: {
                url,
                force: true,
                refreshing: true
            }
        })
    }})(AppSearchResults);
