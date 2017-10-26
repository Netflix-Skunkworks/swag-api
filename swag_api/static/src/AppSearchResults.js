import React, {Component} from 'react';
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


export default class AppSearchResults extends Component {
    render() {
        const {data} = this.props;
        if (data.pending) {
            return <ResultLoader/>;
        } else if (data.rejected) {
            return <Error status={data.rejected}/>;
        } else if (data.fulfilled) {
            return <FilterResults
                items={data.value}
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
