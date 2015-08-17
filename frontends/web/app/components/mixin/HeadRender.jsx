var Helmet = require('react-helmet'),
React = require('react');
var HeadRender = function (){
  var meta = [
  {"name": "description", "content": this.state.head.description},

  {"property": "og:locale", "content": "en_US"},
  {"property": "og:type", "content": "article" },
  {"property": "og:title", "content": this.state.head.title},
  {"property": "og:description", "content": this.state.head.description},
  {"property": "og:url", "content": this.state.head.url},
  {"property": "og:site_name", "content": this.state.head.sitename},
  {"property": "og:image", "content": this.state.head.image},

  {"name": "twitter:card", "content": "summary_large_image"},
  {"name": "twitter:description", "content": this.state.head.description},
  {"name": "twitter:title", "content": this.state.head.title},
  {"name": "twitter:domain", "content": this.state.head.sitename},
  {"name": "twitter:image", "content": this.state.head.image},
  {"name": "twitter:creator", "content": "@suryakencana007"},
  {"name": "twitter:site", "content": "@niimanga"}
  ];
  var link = [
  {"rel": "canonical", "href": "http://niimanga.net"},
  {"rel": "alternate", "href": "http://niimanga.net/#/"},
  {"rel": "publisher", "href": "https://plus.google.com/109363191390818524400" },
  {"rel": "author", "href": "https://twitter.com/@suryakencana007" },

  ];
  return (
    <span>
    <Helmet 
    title={this.state.head.title}
    meta={meta}
    link={link}
    />
    </span>
    );
};

module.exports = {
  getInitialState: function() {
    return {
     head: {
      title: "Niimanga - The only manga reader page you'll ever need",
      description: "Niimanga - Manga reader for free and enjoying what you'll need to reading manga popular series",
      sitename: "Niimanga",
      image: "http://niimanga.net/static/socmed.png",
      url: "http://niimanga.net"
    }
  }
},
renderHead: HeadRender
}