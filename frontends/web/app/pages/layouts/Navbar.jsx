var React = require('react'),
    Router = require('react-router'),
    { Route, DefaultRoute, RouteHandler, Link } = Router;

module.exports = React.createClass({
    mixins: [
        require('react-router').Navigation, // needed for transitionto
    ],

    getInitialState: function() {
        return {
            query: ''
        };
    },

    getDefaultProps: function() {
        return {
            genres: []
        }
    },

    handleSearch: function (e) {
        e.preventDefault(); // So that browser won't submit an old-fashioned POST
        console.log(this.state.query);
        var query = this.state.query
        if (!query || query.trim().length < 2) {
            return;
        }
        this.transitionTo('search', {q: query});
        this.setState({query: ''});
    },

    handleChange: function(event) {
        var val = event.target.value;
        console.log(val);
        this.setState({query: val});
    },

    getGenres: function(gen, start, end) {
        gen = gen.slice(start, end);
        return Object.keys(gen).map(function(uid) {
            return (<li><Link to="genre" params={{q: gen[uid].value}}><i className="fa fa-folder-o fa-fw"></i><span className="title">{gen[uid].label}</span></Link></li>);
        });
    },

    render: function () {
        if(this.props.genres && this.props.genres.length > 0) {
            var genres_o = this.getGenres(this.props.genres, 0, 10);
            var genres_t = this.getGenres(this.props.genres, 10, 20);
            var genres_th = this.getGenres(this.props.genres, 20, 30);
            var genres_fo = this.getGenres(this.props.genres, 30, 40);
        }   
        return (
            <header className="navbar navbar-fixed-top">
                <div className="navbar-inner">
                    <div className="container clearfix">
                        <div className="nav-logo">
                            <Link to="/" >Niimanga<span className="site-logo"></span></Link>
                        </div>
                        <ul className="top-right-nav">
                            <li className="dropdown border-both">
                                <a data-toggle="dropdown" data-hover="dropdown" className="dropdown-toggle" href="#">Genres</a>
                                <div className="dropdown-menu">
                                    <div className="holder-dropdown-menu dropdown-category-thumb">
                                        <div className="row">
                                            <div className="col-md-3">
                                                <ul>
                                                {genres_o}
                                                </ul>
                                            </div>
                                            <div className="col-md-3">
                                                <ul>
                                                {genres_t}
                                                </ul>
                                            </div>
                                            <div className="col-md-3">
                                                <ul>
                                                {genres_th}
                                                </ul>
                                            </div>
                                            <div className="col-md-3">
                                                <ul>
                                                {genres_fo}
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
                                    <Link to="latest" >Latest Manga</Link>
                                </li>
                                <li className="border-both">
                                    <Link to="popular" >Hot Manga</Link>
                                </li>
                            </ul>
                        </div>
                        <form className="search-nav" role="search" onSubmit={ this.handleSearch } >

                            <div className="search-wrapper">
                                <div className="search-parent">
                                    <input className="form-control" onChange={this.handleChange} type="text" value={this.state.query} placeholder="Searching series name..."/>
                                    <span className="btn-search-wrapper">
                                        <button className="btn btn-search" type="submit">
                                            <i className="fa fa-search fa-fw"></i>
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