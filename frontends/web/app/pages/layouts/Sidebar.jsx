var React = require('react');
var Router = require('react-router');
var { Link } = Router;
var {Component, PropTypes} = require('react/addons');

class SideBar extends Component {

    render() {
        return (
            <nav id="slide-menu">
            <div className="nav-logo" style={{float: 'none', padding: ' 5px 20px'}}>
            <Link to="/" >Niimanga<span className="site-logo"></span></Link>
            </div>
            <ul>
            <li><Link className="link-cover" to="/">
            <i className="fa fa-home fa-fw"></i><span>Home</span></Link></li>
            <li><Link className="link-cover" to="/">
            <i className="fa fa-tags fa-fw"></i><span>Genres</span></Link></li>
            <li><Link className="link-cover" to="latest" >
            <i className="fa fa-rss fa-fw"></i> Latest Manga</Link>
            </li>
            <li><Link className="link-cover" to="popular" >
            <i className="fa fa-fire fa-fw"></i>Hot Manga</Link>
            </li>            
            </ul>
            </nav>
            );
    }
}

module.exports = SideBar;