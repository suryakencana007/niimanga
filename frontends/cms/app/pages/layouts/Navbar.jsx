var React = require('react'),
    Router = require('react-router'),
    { Route, DefaultRoute, RouteHandler, Link } = Router,
    SearchText = require('components/TextInput');

module.exports = React.createClass({
    render: function () {
        return (
            <header className="navbar navbar-fixed-top">
                <div className="navbar-inner">
                    <div className="container clearfix">
                        <div className="nav-logo">
                           <Link to="/" >Niimanga<span className="site-logo"></span></Link>
                        </div>
                        <ul className="top-right-nav">
                            <li className="dropdown border-both">
                                <a data-toggle="dropdown" data-hover="dropdown" className="dropdown-toggle" href="#">Master</a>
                                <div className="dropdown-menu">
                                    <div className="holder-dropdown-menu dropdown-category-thumb">
                                        <div className="row">
                                            <div className="col-md-4">
                                                <ul>
                                                    <li><a href="#"><i className="fa fa-users"></i><span className="title">Group</span></a></li>
                                                    <li><a href="#"><i className="fa fa-cart"></i><span className="title">Genre</span></a></li>
                                                    <li><a href="#"><i className="icon-product-beauty icon-large"></i><span className="title">Season</span></a></li>

                                                </ul>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </li>
                        </ul>
                        <div className="pull-right">
                            <ul className="top-right-nav">
                                <li className="border-left">
                                    <Link to="series" >Series</Link>
                                </li>
                                <li className="border-both">
                                    <Link to="chapter" >Chapters</Link>
                                </li>
                                <li className="border-rigth">
                                    <Link to="group" >Login</Link>
                                </li>
                            </ul>
                        </div>
                        <form className="search-nav" role="search">
                            <div className="search-wrapper">
                                <div className="search-parent">
                                    <SearchText type="text" placeholder="cari title manga"/>
                                    <span className="btn-search-wrapper">
                                        <button className="btn btn-search" type="submit">
                                            <i className="fa fa-search"></i>
                                        </button>
                                    </span>
                                </div>
                            </div>
                        </form>
                    </div>
                </div>
            </header>
        );
    }
});