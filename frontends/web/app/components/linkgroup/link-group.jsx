/** @flow */

import React from 'react';
var {Component, PropTypes} = require('react/addons');
// ---- Styles ----
const styles = {
  marginBottom: 16
};

// ---- React Class ----
class SidebarLinkGroup extends Component {

  render() {
    return (
      <ul style={ styles }>
        { this.props.children }
      </ul>
    )
  }
}

module.exports = SidebarLinkGroup;
