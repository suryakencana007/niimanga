var React = require('react');
var Router = require('react-router');
var { Link } = Router;
var Radium = require('radium');
var {Component, PropTypes} = require('react/addons');
import SidebarHeader from 'components/linkgroup/header.jsx';
import SidebarLinkGroup from 'components/linkgroup/link-group.jsx';
import SidebarLink from 'components/linkgroup/link.jsx';

@Radium.Enhancer
class SideBar extends Component {

    render() {
        return (
            <nav style={styles.baseNav}>
            <div className="nav-logo" style={{float: 'none', padding: ' 5px 20px'}}>
            <Link to="/" >Niimanga<span className="site-logo"></span></Link>
            </div>
            <div style={styles.base}>
                <SidebarHeader>Site</SidebarHeader>
                <SidebarLinkGroup>
                <SidebarLink linkto={'/'} iconClass={ 'fa fa-home fa-fw' } external={ true }>Home</SidebarLink>
                <SidebarLink linkto={'/'} iconClass={ 'fa fa-tags fa-fw' } external={ true }>Genres</SidebarLink>
                </SidebarLinkGroup>
                <SidebarHeader>Manga</SidebarHeader>
                <SidebarLinkGroup>
                <SidebarLink linkto={'latest'} iconClass={ 'fa fa-rss fa-fw' } external={ true }>Latest</SidebarLink>
                <SidebarLink linkto={'popular'} iconClass={ 'fa fa-fire fa-fw' } external={ true }>Hot</SidebarLink>
                </SidebarLinkGroup>
            </div>
            </nav>
            );
    }
}

var styles = {
    base: {
        position: 'relative',
        paddingLeft: '10px',
        width: '100%',
        maxWidth: '225px'
    },
    baseNav: {
        width: '250px'
    }
};
module.exports = SideBar;