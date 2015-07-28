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
          var js, fjs = d.getElementsByTagName(s)[0],
          p=/^http:/.test(d.location)?'http':'https';
          js = d.createElement(s); 
          js.id = id;
          js.type = 'text/javascript';
          js.async = true;
          js.src =p+"://connect.facebook.net/en_US/sdk.js";
          fjs.parentNode.insertBefore(js, fjs);
        }(document, 'script', 'facebook-jssdk'));
        (function(id) {
            var po = document.createElement('script'); 
            po.id=id;
            po.type = 'text/javascript';
            po.async = true;
            po.src = 'https://apis.google.com/js/platform.js';
            var s = document.getElementsByTagName('script')[0]; 
            s.parentNode.insertBefore(po, s);
        })("google-pjs");
        (function(d,s,id){
            var js,fjs=d.getElementsByTagName(s)[0],
            p=/^http:/.test(d.location)?'http':'https';
            js=d.createElement(s);
            js.id=id;
            js.type = 'text/javascript';
            js.async = true;
            js.src=p+"://platform.twitter.com/widgets.js";
            fjs.parentNode.insertBefore(js,fjs);
            
        })(document,"script","twitter-wjs");
    },

    componentWillUnmount(){
        this.setState({initLoaded: false});
        var d = document.getElementsByTagName('script')[0];
        d.parentNode.removeChild(document.getElementById("facebook-jssdk"));
        d.parentNode.removeChild(document.getElementById("google-pjs"));
        d.parentNode.removeChild(document.getElementById("twitter-wjs"));
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
                            <div className="fb-page socmed card-content" 
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

                            <Popular />
                            <div className="title-green">Social Media Page</div>
                            <div className="socmed">
                                <div className="g-page" 
                                data-width="215" 
                                data-href="//plus.google.com/u/0/109363191390818524400" 
                                data-rel="publisher"></div>
                            </div>
                            <div className="socmed">
                                <a className="twitter-timeline card-content" 
                                href="https://twitter.com/niimanga"
                                 data-widget-id="625868171711393792">Tweets by @niimanga</a>
                            </div>
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