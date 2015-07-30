var React = require("react");
var Textbox = require('./Textbox');
var Button = require('./Button');
var {Component, PropTypes} = require('react/addons');

class SearchBox extends Component {
  static propTypes = {
    onQueryChange: PropTypes.func.isRequired,
    onQuerySubmit: PropTypes.func.isRequired,
    query: PropTypes.string.isRequired
  };

  _onQueryKeyDown = (e: Object) => {
    if (e.key === 'Enter') {
      this.props.onQuerySubmit(this.props.query);
    }
  };

  _onQueryChange = (e: Object) => {
    this.props.onQueryChange(e.target.value);
  };

  _onSearchClick = () => {
    this.props.onQuerySubmit(this.props.query);
  };

  render(): any {
    return (
      <span >
        <Textbox
          onChange={this._onQueryChange}
          onKeyDown={this._onQueryKeyDown}
          type="search"
          value={this.props.query}
        />
        <Button
          onClick={this._onSearchClick}
          use="special">
          Search
        </Button>
      </span>
    );
  }
}