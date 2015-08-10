var React = require('react');
var _ = require('lodash');
var HeadRender = require('components/mixin/HeadRender');
var Tabs = require('components/Tabs');
var Radium = require('radium');
var Banner = require('pages/home/slickers');
var Latest = require('pages/home/latest');
var LatestIndex = require('pages/mobiles/latest');
var Popular = require('pages/home/popular');
var PopularIndex = require('pages/mobiles/popular');

var isMobile = require('utils/ismobile');

var Homepage = React.createClass({
    mixins: [HeadRender],
    propTypes: {
        initLoaded: React.PropTypes.bool
    },
    statics: {
        fetchData: (token, params, query) => {
            return {
                title: "joss",
                name: "groook"
            }
        }
    },

    getInitialState: function () {
        return {
            initLoaded: false
        };
    },

    componentDidUpdate(){
        /*if(!this.state.initLoaded && typeof FB !== 'undefined') {
            this.setState({initLoaded: true});
            // make the API call
            FB.init({
                appId: '844212729007674',
                cookie: true,
                xfbml: true,
                version: 'v2.4'
            });
        }*/
    },

    componentDidMount(){
        var timeout;
        this.props.loadingEvents.on('start', () => {
          clearTimeout(timeout);
          timeout = setTimeout(() => {
            this.setState({ loading: true });
        }, 250);
      });
        this.props.loadingEvents.on('end', () => {
          clearTimeout(timeout);
          this.setState({ loading: false });
      });

        this.setState({
            head: {
                title: "Niimanga - The only manga reader page you'll ever need",
                description: "Niimanga - Manga reader for free and enjoying what you'll need to reading manga popular series",
                sitename: "Niimanga",
                image: "http://niimanga.net/static/res/share.png",
                url: "http://niimanga.net"
            }
        });
        this.socmedPlugin();
    },

    socmedPlugin: function() {
        (function(d, s, id) {
          var js, fjs = d.getElementsByTagName(s)[0];
          if (d.getElementById(id)) return;
          js = d.createElement(s); 
          js.id = id;
          js.async = true;
          js.src = "//connect.facebook.net/en_US/sdk.js#xfbml=1&version=v2.4&appId=844212729007674";
          fjs.parentNode.insertBefore(js, fjs);
      })(document, 'script', 'facebook-jssdk');
        (function(id) {
            if(document.getElementById(id)) return;
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
            if(d.getElementById(id)) return;
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
    },

    render: function() {
        return (
            <div className="container header-wrapper">
            {this.renderHead()}
            { isMobile()? null: (<span>
            <a ref="ad-left" href="#"><div style={styles.left}></div></a>
            <a ref="ad-right" href="#"><div style={styles.right}></div></a>
            </span>)
            }
            <div className="row">
            <div className="col-xs-12 col-md-9">

                <Banner />
                {isMobile()? (<span>
                <div className="title-green"><br /></div>
                <Tabs>
                    <Tabs.Panel className="btn btn-play" title='Hot'>
                      <PopularIndex {...this.props} />
                    </Tabs.Panel>
                    <Tabs.Panel title='Release'>
                      <LatestIndex {...this.props} />
                    </Tabs.Panel>
                </Tabs>
                </span>): ( <Latest {...this.props}/>)}

                <div className="title-green">Social Media Page</div>
               
                <div className="socmed col-xs-12">
                    <div className="col-md-5 col-xs-12">
                        <div className="g-page" 
                        data-width="215" 
                        data-href="//plus.google.com/u/0/109363191390818524400" 
                        data-rel="publisher">
                        </div>
                    </div>
                    <div className="col-md-7 col-xs-12">
                        <div className="fb-page" 
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
                </div>
                </div>
            </div>

            <div className="col-xs-12 col-md-3">

                {!isMobile()?<Popular {...this.props}/>: null }
                
                <div className="title-green">Social Media Share</div>
                
                <div className="socmed col-xs-6">
                    <div className="socmed col-xs-6 fb-like" 
                    data-href="https://www.facebook.com/niimanga" 
                    data-layout="button_count" 
                    data-action="like" 
                    data-show-faces="true" 
                    data-share="false">
                    </div>
                </div>
                <div className="socmed col-xs-6"><div className="fb-share-button" data-href="http://www.niimanga.net" data-layout="button_count"></div></div>
                <div className="socmed col-xs-6"><div className="g-plusone" data-annotation="bubble" data-href="http://www.niimanga.net"></div></div>
                <div className="socmed col-xs-6"><div className="g-follow" data-annotation="bubble" data-height="20" data-href="//plus.google.com/u/0/109363191390818524400" data-rel="publisher"></div></div>

                <div className="socmed">
                    <a className="twitter-timeline card-content" 
                    href="https://twitter.com/niimanga"
                    data-widget-id="625868171711393792">Tweets by @niimanga</a>
                 </div>
            </div>
        </div>
    </div>
            );
}
});

var styles = {
    left: {
        height: '900px',
        left: '-493px',
        top: '34px',
        position: 'fixed',
        width: '50%',
        cursor: 'pointer',
        background: 'url(static/res/ad-banner-left.png) 100% 0% no-repeat scroll transparent'
    },

    right: {
        height: '900px',
        left: '711px',
        top: '34px',
        position: 'fixed',
        width: '50%',
        cursor: 'pointer',
        background: 'url(static/res/ad-banner-right.png) 100% 0% no-repeat scroll transparent'
    }
};

module.exports = Homepage;