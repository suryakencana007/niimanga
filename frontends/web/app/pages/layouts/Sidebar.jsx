var React = require('react'),
Router = require('react-router'),
{ Route, DefaultRoute, RouteHandler, Link } = Router;

var CategoryNav = React.createClass({
  getInitialState: function () {
    return { isOpen: this.props.defaultIsOpen};
  },

  getDefaultProps: function () {
    return { isOpen: false };
  },

  componentWillReceiveProps: function (newProps) {
    if (!this.state.isOpen)
      this.setState({ isOpen: newProps.defaultIsOpen });
  },

  toggle: function () {
    this.setState({ isOpen: !this.state.isOpen });
  },

  buildToggleClassName: function () {
    var toggleClassName = 'CategoryNav__Toggle';
    if (this.state.isOpen)
      toggleClassName += ' CategoryNav__Toggle--is-open';
    return toggleClassName;
  },

  renderItems: function () {
    var category = this.props.category;
    return this.state.isOpen ? category.items.map(function (item) {
      var params = { name: item.name, category: category.name };
      return (
        <li key={item.name}>
        <Link to="item" params={params}>{item.name}</Link>
        </li>
        );
    }) : null;
  },

  render: function () {
    var category = this.props.category;
    return (
      <div className="CategoryNav">
      <h3
      className={this.buildToggleClassName()}
      onClick={this.toggle}
      >{category.name}</h3>
      <ul>{this.renderItems()}     
      </ul>  
      </div>
      );
  }
});

module.exports = React.createClass({
  renderCategory: function (category) {
    return <CategoryNav
    key={category.name}
    defaultIsOpen={category.name === this.props.activeCategory}
    category={category}/>;
  },

  render: function () {
    return (
      <div className="Sidebar">
      {this.props.categories.map(this.renderCategory)}
      </div>
      );
  }
});