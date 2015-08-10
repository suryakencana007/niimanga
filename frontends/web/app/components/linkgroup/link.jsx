/** @flow */

import React from 'react';
import Radium from 'radium';
import Colors from 'components/mixin/Colors';
import {Component, PropTypes} from 'react/addons';
import { projectStyles } from './project-vars.js';
import { Link }  from 'react-router';

const styles = {
  base: {
    display: 'flex',
    alignItems: 'center',
    padding: '12px 0',
    cursor: 'pointer',
    transition: `background-color ${ projectStyles.timings.color } ${ projectStyles.easings.color }`,
    ':hover': {
      backgroundColor: Colors.white
    }
  },
  link: {
    position: 'relative',
    display: 'block',
    fontSize: '12px',
    textDecoration: 'none',
    lineHeight: '20px'
  },
  icon: {
    color: Colors.white,
    width: 16,
    height: 16,
    marginLeft: 16
  },
  text: {
    flex: '1 0 auto',
    padding: '0 16px',
    fontSize: 14,
    color: Colors.white,
    whiteSpace: 'nowrap',
    overflow: 'hidden',
    textOverflow: 'ellipsis',
    transition: `color ${ projectStyles.timings.color } ${ projectStyles.easings.color }`
  },
  textHover: {
    color: Colors.primary
  },
  button: {
    padding: '4px 10px',
    marginRight: 8,
    borderRadius: 0,
    fontSize: 11,
    color: Colors.gray2.darken(27),
    backgroundColor: Colors.white
  },
  external: {
    width: 12,
    height: 12,
    marginLeft: 0,
    marginRight: 12
  }
};

@Radium.Enhancer
class SidebarLink extends Component {

  render() {
    return (
      <li key="base" style={ styles.base }>      
      <Link style={[ styles.text,
        Radium.getState(this.state, 'base', ':hover') && styles.textHover,
       styles.link ]} to={this.props.linkto}>
        { this.props.children }
        </Link>    
        { ( this.props.external ) ?
          <i
            className={this.props.iconClass}
            style={ [ styles.icon, styles.external,
            Radium.getState(this.state, 'base', ':hover') && styles.textHover ] }
            >
          </i>
          : null
        }
      </li>
    )
  }
}

module.exports = SidebarLink;
