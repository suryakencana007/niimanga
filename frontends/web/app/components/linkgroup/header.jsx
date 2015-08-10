import React from 'react';
import {Component, PropTypes} from 'react/addons';
import Colors from 'components/mixin/Colors';

const styles = {
  base: {
    display: 'flex',
    alignItems: 'center',
    marginBottom: 8
  },
  text: {
    marginRight: 8,
    fontSize: 11,
    fontWeight: 400,
    lineHeight: '16px',
    color: Colors.white.darken(15),
    textTransform: 'uppercase'
  },
  border: {
    flex: '1 0 auto',
    height: 1,
    backgroundColor: Colors.white
  }
};


class SidebarHeader extends Component {

  render() {
    return (
      <h6 style={ styles.base }>
        <span style={ styles.text }>{ this.props.children }</span>
        <span style={ styles.border }></span>
      </h6>
    )
  }
}

module.exports = SidebarHeader;
