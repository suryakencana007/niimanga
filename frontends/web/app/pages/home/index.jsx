var React = require('react'),
    _ = require('lodash'),
    Banner = require('pages/home/banner'),
    Latest = require('pages/home/latest'),
    Popular = require('pages/home/popular');

module.exports = React.createClass({
    propTypes: {
        initLoaded: React.PropTypes.bool
    },

    getInitialState: function () {
        return {
            initLoaded: false
        };
    },

    componentDidUpdate(){
        if(!this.state.initLoaded && typeof FB !== 'undefined') {
            this.setState({initLoaded: true});
            /* make the API call */
            FB.init({
                appId: '844212729007674',
                cookie: true,
                xfbml: true,
                version: 'v2.4'
            });
        }
    },

    componentDidMount(){
      
    },

    componentWillMount() {
        (function(d, s, id) {
          var js, fjs = d.getElementsByTagName(s)[0];
          if (d.getElementById(id)) return;
          js = d.createElement(s); js.id = id;
          js.src = "//connect.facebook.net/en_US/sdk.js";
          fjs.parentNode.insertBefore(js, fjs);
        }(document, 'script', 'facebook-jssdk'));
        (function() {
            var po = document.createElement('script'); po.type = 'text/javascript'; po.async = true;
            po.src = 'https://apis.google.com/js/platform.js';
            var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(po, s);
        })();
    },

    componentWillUnmount(){
        this.setState({initLoaded: false});
        var d = document.getElementsByTagName('script')[0];
        d.parentNode.removeChild(document.getElementById("facebook-jssdk"));
    },

    render: function() {
        return (
                <div className="container header-wrapper">
                    <div className="ad-left home">
                        <div className="ad-box">
                            <a href="#">
                            <img src="static/res/ad-banner-left.png" className="img-responsive" />
                            </a>
                        </div>
                    </div>
                    
                    <div className="row">
                        <div className="col-xs-12 col-md-9">
                            <Banner />
                            <Latest />
                        </div>
                        <div className="col-xs-12 col-md-3">
                            <div className="fb-page card-content" 
                                data-href="https://www.facebook.com/niimanga" 
                                data-small-header="false" 
                                data-adapt-container-width="true" 
                                data-hide-cover="false" 
                                data-show-facepile="true" 
                                data-show-posts="false">
                                <div className="fb-xfbml-parse-ignore">
                                <blockquote cite="https://www.facebook.com/niimanga">
                                <a href="https://www.facebook.com/niimanga">Niimanga</a></blockquote>
                                </div>
                            </div>
                            <div class="g-person" data-width="180" 
                            data-href="//plus.google.com/u/0/114203833938318389879" 
                            data-rel="author"></div>

                            <Popular />
                        </div>
                    </div>
                    <div className="ad-right home">
                        <div className="ad-box">
                            <a href="#" >
                            <img src="static/res/ad-banner-right.png" className="img-responsive" />
                            </a>
                        </div>
                    </div>
                </div>
        );
    }
});;