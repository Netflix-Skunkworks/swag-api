import {BehaviorSubject} from 'rxjs/BehaviorSubject';
import filterResultsFactory from './FilterResults';
import appSearchFilterFactory from './AppSearchInput';


export default function fuzzyFilterFactory() {
    const store = new BehaviorSubject();
    return {
        FilterResults: filterResultsFactory(store),
        AppSearchInputFilter: appSearchFilterFactory(store)
    };
}