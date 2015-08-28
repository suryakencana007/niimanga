import React, { Component, PropTypes } from 'react';
import Input from 'components/base/Input';

class LabelEdit extends Component {
  constructor(props, context) {
    super(props, context);
    this.state = {
      editing: false,
      text: this.props.text || ''
    };
  }  

  handleClick() {
    this.setState({ 
      editing: true,
      text: this.props.text || ''
    });
  }

  handleSave(text) {
    this.setState({ editing: false });
    this.props.saveText && this.props.saveText(text);
  }

  render() {
    let element;
    if (this.state.editing) {
      element = (
        <Input text={this.state.text}
        write={this.state.editing}
        onSave={(text) => this.handleSave(text)} />
      );
    } else {
      element = (
        <span onClick={this.handleClick.bind(this)}>
        {this.props.children}
        </span>
      );
    }

    return element;
  }
}

LabelEdit.propTypes = {
  text: PropTypes.string,
  saveText: PropTypes.func,
  children: PropTypes.object
};

export default LabelEdit;
