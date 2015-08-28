import React, { Component, PropTypes } from 'react';
import classnames from 'classnames';
import Radium from 'radium';
import Colors from 'components/mixin/Colors';
import PureRender from 'components/mixin/PureRender';

@PureRender
@Radium.Enhancer
class Input extends Component {
  constructor(props, context) {
    super(props, context);
    this.state = {
      text: this.props.text || ''
    };
  }

  handleSubmit(e) {
    const text = e.target.value.trim();
    if (e.which === 13) {
      this.props.onSave && this.props.onSave(text);
    }
  }

  handleChange(e) {
    this.setState({ text: e.target.value });
  }

  handleBlur(e) {
    this.props.onSave && this.props.onSave(e.target.value);
  }

  render() {
    return (
      <input 
      style={[
        styles.base,
        this.props.write === true && styles.write
        ]}
             type='text'
             placeholder={this.props.placeholder}
             autoFocus='true'
             value={this.state.text}
             onBlur={this.handleBlur.bind(this)}
             onChange={this.handleChange.bind(this)}
             onKeyDown={this.handleSubmit.bind(this)} />
    );
  }
}

Input.propTypes = {
  onSave: PropTypes.func.isRequired,
  text: PropTypes.string,
  placeholder: PropTypes.string,
  write: PropTypes.bool
};


let styles = {
  base: {
    border: 'none',
    margin: 0,
    padding: '4px',
    width: '100%',
    fontFamily: 'inherit',
    fontWeight: 'inherit',
    lineHeight: '0.9em',
    color: 'inherit',
    background: 'rgba(0, 0, 0, 0.003)'
  },
  write: {
    border: '1px solid',
    borderColor: Colors.pink.lighten(17)
  },
  label: {

  }
}
export default Input;
