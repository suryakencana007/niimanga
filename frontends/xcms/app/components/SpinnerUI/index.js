/** @flow */

import React, {Component, PropTypes} from 'react/addons';
import Radium from 'radium';
import Colors from 'components/mixin/Colors';
import Style from 'components/mixin/Style';

export default class SpinnerUI extends Component {
  render(): any {
    return (
      <div style={styles.root}>
        <div style={styles.inner} />
      </div>
    );
  }
}

var pulseKeyframes = Radium.keyframes({
  '0%': {width: '10%'},
  '50%': {width: '50%'},
  '100%': {width: '10%'}
});

var styles = {
  root: {
    left: 0,
    position: 'fixed',
    top: 0,
    width: '100%',
    zIndex: 10000
  },

  inner: {
    animation: pulseKeyframes + ' 3s ease 0s infinite',
    background: Colors.pink,
    height: '6px',
    margin: '0 auto'
  }
};