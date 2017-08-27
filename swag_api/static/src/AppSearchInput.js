import React, {Component} from 'react';
import PropTypes from 'prop-types';
import debounce from 'debounce';
import Autosuggest from 'react-autosuggest';
import Paper from 'material-ui/Paper';
import {MenuItem} from 'material-ui/Menu';
import match from 'autosuggest-highlight/match';
import parse from 'autosuggest-highlight/parse';
import {withStyles} from 'material-ui/styles';


function renderSuggestion(suggestion, {query, isHighlighted}) {
    const matches = match(suggestion.name, query);
    const parts = parse(suggestion.name, matches);

    return (
        <MenuItem selected={isHighlighted} component="div">
            <div>
                {parts.map((part, index) => {
                    return part.highlight
                        ? <span key={index} style={{fontWeight: 300}}>
                {part.text}
              </span>
                        : <strong key={index} style={{fontWeight: 500}}>
                            {part.text}
                        </strong>;
                })}
            </div>
        </MenuItem>
    );
}

function renderSuggestionsContainer(options) {
    const {containerProps, children} = options;

    return (
        <Paper {...containerProps} square>
            {children}
        </Paper>
    );
}

function getSuggestionValue(suggestion) {
    return suggestion.name + ': ';
}

function getSuggestions(suggestions, value) {
    const inputValue = value.trim().toLowerCase();
    const inputLength = inputValue.length;
    let count = 0;

    return inputLength === 0
        ? []
        : suggestions.filter(suggestion => {
            const keep =
                count < 5 && suggestion.name.toLowerCase().slice(0, inputLength) === inputValue;

            if (keep) {
                count += 1;
            }

            return keep;
        });
}

const styles = theme => ({
    container: {
        flexGrow: 1,
        position: 'relative',
    },
    suggestionsContainerOpen: {
        position: 'absolute',
        marginTop: theme.spacing.unit,
        marginBottom: theme.spacing.unit * 3,
        left: 0,
        right: 0,
        zIndex: 9999,
    },
    suggestion: {
        display: 'block',
    },
    suggestionsList: {
        margin: 0,
        padding: 0,
        listStyleType: 'none',
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
    }
});

export default function appSearchFilterFactory(store) {
    function updateValue(value, callback) {
        const overrideValue = callback(value);
        if (typeof overrideValue === 'string') {
            value = overrideValue;
        }
        store.next(value);
    }

    class InputFilter extends Component {
        static displayName = 'InputFilter';

        static propTypes = {
            classPrefix: PropTypes.string.isRequired,
            initialSearch: PropTypes.string,
            inputProps: PropTypes.object,
            onChange: PropTypes.func,
            debounceTime: PropTypes.number
        };

        static defaultProps = {
            classPrefix: 'react-fuzzy-filter',
            inputProps: {},
            onChange: function () {
            },
            debounceTime: 0
        };

        state = {
            value: this.props.initialSearch || '',
            suggestions: this.props.keys
        };

        componentDidMount() {
            updateValue(this.props.initialSearch, this.props.onChange);
        }

        componentWillReceiveProps(nextProps) {
            this.updateValue = debounce(updateValue, nextProps.debounceTime);
            if (nextProps.initialSearch !== this.props.initialSearch) {
                updateValue(nextProps.initialSearch, this.props.onChange);
                this.setState({value: nextProps.initialSearch});
            }
        }

        handleSuggestionsFetchRequested = ({value}) => {
            this.setState({
                suggestions: getSuggestions(this.props.keys, value),
            });
        };

        handleSuggestionsClearRequested = () => {
            this.setState({
                suggestions: [],
            });
        };

        updateValue = debounce(updateValue, this.props.debounceTime);

        handleChange = (event, {newValue}) => {
            this.setState({
                value: newValue,
            });
            if (this.props.debounceTime > 0) {
                this.updateValue(newValue, this.props.onChange);
            } else {
                updateValue(newValue, this.props.onChange);
            }
        };

        render() {
            const {classes} = this.props;
            return (
                <Autosuggest
                    theme={{
                        container: classes.container,
                        suggestionsContainerOpen: classes.suggestionsContainerOpen,
                        suggestionsList: classes.suggestionsList,
                        suggestion: classes.suggestion,
                    }}
                    suggestions={this.state.suggestions}
                    onSuggestionsFetchRequested={this.handleSuggestionsFetchRequested}
                    onSuggestionsClearRequested={this.handleSuggestionsClearRequested}
                    renderSuggestionsContainer={renderSuggestionsContainer}
                    getSuggestionValue={getSuggestionValue}
                    renderSuggestion={renderSuggestion}
                    highlightFirstSuggestion={true}
                    inputProps={{
                        autoFocus: true,
                        className: classes.input,
                        value: this.state.value,
                        onChange: this.handleChange,
                    }}
                />
            );
        }
    }

    InputFilter.propTypes = {
        classes: PropTypes.object.isRequired,
    };

    return withStyles(styles)(InputFilter);
}