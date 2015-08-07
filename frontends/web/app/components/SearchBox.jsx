var React = require("react");
var Textbox = require('./TextBox');
var Button = require('./Button');
var {Component, PropTypes} = require('react/addons');

class SearchBox extends Component {
  static propTypes = {
    children: PropTypes.node.isRequired,
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
      <div className="search-nav">
        <div className="search-wrapper">
            <div className="search-parent">
                <input className="search-input"
                type="search"
                onChange={this._onQueryChange}
                onKeyDown={this._onQueryKeyDown}
                placeholder={this.props.placeholders}
                value={this.props.query}
                />
                <span className="btn-search-wrapper">
                    <button className="btn btn-search" 
                    onClick={this._onSearchClick}
                    type="submit">
                        <i className="fa fa-search fa-fw"></i>
                    </button>
                </span>
            </div>
        </div>
      </div>
    );
  }
}

module.exports = SearchBox;