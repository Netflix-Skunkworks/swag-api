import React, {Component} from 'react';



class AccountStatusStepper extends Component {
    constructor(props, context) {
        super(props, context);
        this.state = {
            stepIndex: this.getIndex(props.status)
        };
    }

    getIndex(status) {
        switch (status) {
            case 'created':
                return 0;
            case 'in-progress':
                return 1;
            case 'ready':
                return 2;
            case 'deprecated':
                return 3;
            case 'deleted':
                return 4;
            case 'in-active':
                return 5;
            default:
                return 6;
        }
    }

    render() {
        return (
            <div>
            </div>
        );
    }
}

export default AccountStatusStepper;