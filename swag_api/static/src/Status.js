import React, {Component} from 'react';

import {
    Step,
    Stepper,
    StepLabel,
    StepContent
} from 'material-ui/Stepper';


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
            <div style={{maxHeight: 400, maxWidth: 380, margin: 'auto'}}>
                <Stepper linear={false} orientation="vertical" activeStep={this.state.stepIndex}>
                    <Step>
                        <StepLabel>
                            Created
                        </StepLabel>
                        <StepContent>
                            <p style={{wordWrap: "break-word"}}>
                                Account has been created but infrastructure
                                has not yet been established.
                            </p>
                        </StepContent>
                    </Step>
                    <Step>
                        <StepLabel>
                            In-progress
                        </StepLabel>
                        <StepContent>
                            <p>
                                Account infrastructure is currently being deployed.
                            </p>
                        </StepContent>
                    </Step>
                    <Step completed={false}>
                        <StepLabel>
                            Ready
                        </StepLabel>
                        <StepContent>
                            <p>
                                Account is ready for deployment.
                            </p>
                        </StepContent>
                    </Step>
                     <Step completed={false}>
                        <StepLabel>
                            Deprecated
                        </StepLabel>
                        <StepContent>
                            <p>
                                Account has been marked as deprecated,
                                no new services should be deployed into this account.
                            </p>
                        </StepContent>
                    </Step>
                    <Step completed={false}>
                        <StepLabel>
                            In-active
                        </StepLabel>
                        <StepContent>
                            <p>
                                Account has been evacuated of all services.
                            </p>
                        </StepContent>
                    </Step>
                    <Step completed={false}>
                        <StepLabel>
                            Deleted
                        </StepLabel>
                        <StepContent>
                            <p>
                                Account has been marked as deleted.
                                No services still exist in this account.
                            </p>
                        </StepContent>
                    </Step>
                </Stepper>
            </div>
        );
    }
}

export default AccountStatusStepper;