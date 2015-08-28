/**  @flow */

import React, {Component, PropTypes, findDOMNode} from 'react/addons';

export default class AlertUI extends Component {
    static propTypes = {
        msg: PropTypes.string,
        cssClass: PropTypes.string,
        dismissible: PropTypes.bool
    }

    static defaultProps = {
        msg: '',
        cssClass: '',
        dismissible: false
    }

    render(): any {
        if (!this.props.msg) {
            return (<span></span>);
        }

        if (this.props.hasOwnProperty('cssClass')) {
            var cssClass = this.props.cssClass;
        } else {
            var cssClass = 'danger';
        }

        var className = "alert alert-" + cssClass;

        if (this.props.hasOwnProperty('dismissible') &&
            this.props.dismissible) {
            return (
                <div className={className + ' alert-dismissible'} role="alert">
                    <button type="button" className="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>
                    {this.props.msg}
                </div>
            );
        }

        return (
            <div className={className} role="alert">{this.props.msg}</div>
        );
    }
});