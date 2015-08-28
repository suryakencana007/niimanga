/**  @flow */

import React, {Component, PropTypes} from 'react/addons';
import Radium from 'radium';
import Colors from 'components/mixin/Colors';

@Radium.Enhancer
export default class LoadingUI extends Component {
    render(): any {
        if (this.props.hasOwnProperty('loading') && this.props.loading === false) return null;
        var text = <h4>{this.props.text}</h4> || '';
        return (
            <div className='icon-container' style={styles.base}>
            <i className='fa fa-5x fa-spinner fa-pulse'></i>
            {text}
            </div>
            );
    }
}

var styles = {
    base: {
        'textAlign': 'center',
        'marginTop': '30px'
    }
}