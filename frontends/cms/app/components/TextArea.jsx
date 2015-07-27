var React = require('react'),
ENTER_KEY_CODE = 13;

module.exports = React.createClass({

  propTypes: {
    threadID: React.PropTypes.string.isRequired
  },

  getInitialState: function() {
    return {text: ''};
  },

  render: function() {
    var label = this.props.label,
    placeholder = this.props.placeholder || '';

    return (
      <div className="form-group">
      <label className="col-sm-2 control-label">
      {label}
      </label>
      <div className="col-sm-10">
      <textarea        
      className="form-control" 
      placeholder={placeholder} 
      value={this.state.text}
      onChange={this._onChange}
      onKeyDown={this._onKeyDown} />
      </div>
      </div>
      );
  },

  _onChange: function(event, value) {
    this.setState({text: event.target.value});
  },

  _onKeyDown: function(event) {
    if (event.keyCode === ENTER_KEY_CODE) {
      event.preventDefault();
      var text = this.state.text.trim();
      if (text) {
        // ChatMessageActionCreators.createMessage(text, this.props.threadID);
      }
      this.setState({text: ''});
    }
  }

});