// @flow

import React from 'react';
import compose from 'recompose/compose';
import pure from 'recompose/pure';
import PropTypes from 'prop-types';
import withWidth, {isWidthUp} from 'material-ui/utils/withWidth';
import Search from 'material-ui-icons/Search';
import {fade} from 'material-ui/styles/colorManipulator';
import {withStyles} from 'material-ui/styles';
import fuzzyFilterFactory from './FuzzyFilterFactory';

export const {AppSearchInputFilter, FilterResults} = fuzzyFilterFactory();

const styles = theme => ({
    '@global': {
        '.algolia-autocomplete': {
            fontFamily: theme.typography.fontFamily,
            '& .algolia-docsearch-suggestion--title': {
                ...theme.typography.title,
            },
            '& .algolia-docsearch-suggestion--text': {
                ...theme.typography.body1,
            },
            '& .ds-dropdown-menu': {
                boxShadow: theme.shadows[1],
                borderRadius: 2,
                '&::before': {
                    display: 'none',
                },
                '& [class^=ds-dataset-]': {
                    border: 0,
                    borderRadius: 2,
                },
            },
        },
    },
    wrapper: {
        fontFamily: theme.typography.fontFamily,
        position: 'relative',
        borderRadius: 2,
        background: fade(theme.palette.common.white, 0.15),
        '&:hover': {
            background: fade(theme.palette.common.white, 0.25),
        },
        width: '90%'
    },
    search: {
        width: theme.spacing.unit * 8,
        height: '100%',
        position: 'absolute',
        pointerEvents: 'none',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
    },
    input: {
        font: 'inherit',
        padding: `${theme.spacing.unit}px ${theme.spacing.unit}px ${theme.spacing.unit}px ${theme
            .spacing.unit * 9}px`,
        border: 0,
        display: 'block',
        verticalAlign: 'middle',
        whiteSpace: 'normal',
        background: 'none',
        margin: 0, // Reset for Safari
        color: 'inherit',
        width: '100%',
        '&:focus': {
            outline: 0,
        },
    },
});

export const fuseConfig = {
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

function AppSearch(props) {
    const {classes, width} = props;

    if (!isWidthUp('sm', width)) {
        return null;
    }

    return (
        <div className={classes.wrapper}>
            <div className={classes.search}>
                <Search/>
            </div>
            <AppSearchInputFilter keys={fuseConfig.keys} debounceTime={200}/>
        </div>
    );
}

AppSearch.propTypes = {
    classes: PropTypes.object.isRequired,
    width: PropTypes.string.isRequired,
};

export default compose(
    withStyles(styles, {
        name: 'AppSearch',
    }),
    withWidth(),
    pure,
)(AppSearch);