/** @flow */

import React, {Component, PropTypes} from 'react/addons';

export default class SearchBox extends Component {
  static propTypes = {
    onQueryChange: PropTypes.func.isRequired,
    onQuerySubmit: PropTypes.func.isRequired,
    query: PropTypes.string.isRequired
  };

  constructor() {
    super();
    this._onQueryChange = this._onQueryChange.bind(this);
    this._onSearchClick = this._onSearchClick.bind(this);
    this._onQueryKeyDown = this._onQueryKeyDown.bind(this);
  }

  _onQueryKeyDown(e: Object) {
    if (e.key === 'Enter') {
      this.props.onQuerySubmit(this.props.query);
    }
  }

  _onQueryChange(e: Object) {
    this.props.onQueryChange(e.target.value);
  }

  _onSearchClick() {
    this.props.onQuerySubmit(this.props.query);
  }

  render(): any {
    return (
      <div className="search-nav">
        <div className="search-wrapper">
            <div className="search-parent">
                <input className="search-input"
                type="search"
                onChange={this._onQueryChange}
                onKeyDown={this._onQueryKeyDown}
                placeholder={this.props.placeholder}
                value={this.props.query} />
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