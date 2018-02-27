import React, {Component} from 'react';
import {fuseConfig, FilterResults} from './AppSearch';

import AccountCard from './AccountCard';
import Error from './Error';
import ResultLoader from './ResultLoader';

import {withStyles} from 'material-ui/styles';
import Dialog from 'material-ui/Dialog';
import AppBar from 'material-ui/AppBar';
import Toolbar from 'material-ui/Toolbar';
import ArrowBack from 'material-ui-icons/ArrowBack';
import Slide from 'material-ui/transitions/Slide';
import ServiceCard from './ServiceCard';
import IconButton from 'material-ui/IconButton';
import Typography from 'material-ui/Typography';
import ReactJson from 'react-json-view';

const styles = {
    appBar: {
        position: 'relative',
    },
    flex: {
        flex: 1,
    },
    container: {
        padding: '16px',
        fontWeight: '500',
        boxSizing: 'border-box',
        position: 'relative',
        whiteSpace: 'nowrap',
        overflow: 'auto'
    },
    content: {
        display: 'flex',
        flexDirection: 'column',
        flexWrap: 'no-wrap',
        minHeight: '100vh'
    }
}
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
    state = { open: false, jsonOpen: false, account: { services: []} }
    onOpenCard = account => event => {
      this.setState({
        open: true,
        account
      })
    }

    onOpenJSON = account => event => {
      this.setState({
        jsonOpen: true,
        account,
      })
    }

    handleClose = event => {
      this.setState({
        open: false,
        jsonOpen: false,
        account: { services: [] },
      })
    }

    render() {
        const {data, classes} = this.props;

        if (data.pending) {
            return <ResultLoader/>;
        } else if (data.rejected) {
            return <Error status={data.rejected}/>;
        } else if (data.fulfilled) {
            return <div>
              <Dialog
                  fullScreen
                  open={this.state.open}
                  onRequestClose={this.handleClose}
                  transition={<Slide direction="right"/>}
              >
                  <AppBar position="static">
                      <Toolbar>
                          <IconButton color="contrast" onClick={this.handleClose} aria-label="Close">
                              <ArrowBack/>
                          </IconButton>
                          <Typography type="title" color="inherit" className={classes.flex}>
                              Services
                          </Typography></Toolbar>
                  </AppBar>
                  <div className={classes.container}>
                      <div className={classes.content}>
                          {this.state.account.services.map((item, index) => <ServiceCard key={index} service={item}/>)}
                      </div>
                  </div>
              </Dialog>
              <Dialog
                  fullScreen
                  open={this.state.jsonOpen}
                  onRequestClose={this.handleClose}
                  transition={<Slide direction="right"/>}
              >
                  <AppBar position="static">
                      <Toolbar>
                          <IconButton color="contrast" onClick={this.handleClose} aria-label="Close">
                              <ArrowBack/>
                          </IconButton>
                          <Typography type="title" color="inherit" className={classes.flex}>
                              Raw JSON
                          </Typography></Toolbar>
                  </AppBar>
                  <div className={classes.container}>
                      <div className={classes.content}>
                          <ReactJson enableClipBoard={false} displayDataTypes={false} displayObjectSize={false} onEdit={true} src={this.state.account}/>
                      </div>
                  </div>
              </Dialog>
              <FilterResults
                  items={data.value}
                  fuseConfig={fuseConfig}
                  prefilters={prefilters}
              >
                  {filteredItems => {
                      return (
                          <div>
                              {filteredItems.map((item, idx) => idx > -1 ? <AccountCard openJSON={this.onOpenJSON} openDialog={this.onOpenCard} key={item.id} account={item}/> : null)}
                          </div>
                      )
                  }}
            </FilterResults>
          </div>
        }
    }
}

export default withStyles(styles)(AppSearchResults)
