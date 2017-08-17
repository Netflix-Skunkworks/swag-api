import React from 'react';
import Drawer from 'material-ui/Drawer';
import {List} from 'material-ui/List';
import ServiceDialog from './ServiceDialog';
import IconButton from 'material-ui/IconButton';
import Computer from 'material-ui/svg-icons/hardware/computer';

import Subheader from 'material-ui/Subheader';

class ServiceDrawer extends React.PureComponent {

    constructor(props, context) {
        super(props, context);
        this.handleToggle = this.handleToggle.bind(this);

        this.state = {
            open: false
        };
    }

    handleToggle() {
        this.setState({open: !this.state.open});
    }

    handleClose() {
        this.setState({open: false});
    }

    render() {
        return (
            <div>
                <IconButton tooltip="View Services" onClick={this.handleToggle}>
                    <Computer />
                </IconButton>
                <Drawer
                    docked={false}
                    width={400}
                    openSecondary={true}
                    open={this.state.open}
                    onRequestChange={(open) => this.setState({open})}
                >
                    <List>
                        <Subheader>Services</Subheader>
                        {this.props.services.map((service, index) => {
                            return (
                                <ServiceDialog key={index} data={service}/>
                            )
                        })}
                    </List>
                </Drawer>
            </div>
        );
    }
}

export default ServiceDrawer;