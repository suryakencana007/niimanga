/** @flow */

import React, { Component, PropTypes} from'react';
import { Route, DefaultRoute, RouteHandler, Link } from 'react-router';
import router from 'utils/router';
import SearchBox from 'components/SearchBox';


export default class Navbar extends Component {

    static propTypes = {
        genres: PropTypes.array
    };

    constructor(){
        super();
        this.state = { query: ''};
        this._handleSearch = this._handleSearch.bind(this);
        this._handleChange = this._handleChange.bind(this);
    }

    _handleSearch(query){
        if (!query || query.trim().length < 2) {
            return;
        }
        router.transitionTo('search', {q: query});
        this.setState({query: ''});
    }

    _handleChange(query){
        this.setState({query: query});
    }

    render(): any {
        return (
            <header className="navbar navbar-fixed-top">
                <div className="navbar-inner">
                    <div className="container clearfix">
                        <div className="nav-logo">
                            <Link to="root" >Niimanga<span className="site-logo"></span></Link>
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
                                    <Link to="chapters" >Chapters</Link>
                                </li>
                                <li className="border-rigth">
                                    <Link to="group" >Login</Link>
                                </li>
                            </ul>
                        </div>
                         <SearchBox
                        onQueryChange={this._handleChange}
                        onQuerySubmit={this._handleSearch}
                        query={this.state.query}
                        placeholder="Searching series name..."
                        />
                        
                    </div>
                </div>
            </header>
        );
    }
}