var React = require('react');
var _ = require('lodash');
var Radium = require('radium');
var cache = require('utils/cache');
var api = require('utils/api');
var Loading = require('components/Loading');
var Alert = require('components/Alert');
var InfiniteScroll = require('components/scroller/InfiniteScroll');
var ListCard = require('components/manga/ListCard');

var popular = React.createClass({
    getInitialState: function () {
        return {
            limit: 25,
            offset: 0,
            cards : [],
            fetching: false
        }
    },

    fetchCards: function () {
        var newState = this.state;
        newState.fetching = true;

        this.setState(newState);

        var self = this;
        var url = '/popular?page=' + newState.offset + '&cards=' + newState.limit;
        var result = api.post(url, this.props.token).then((data) => {
            cache.expire(this.props.token, url);
            self.updateCardsData(data);
            self.setState({fetching: false});
        }).then(null, function(){
            self.setState({error: true});
            self.setState({fetching: false});
        });
    },

    updateCardsData: function (data) {
        this.setState({
            cards: this.state.cards.concat(data),
            offset: this.state.offset + 1
        });
    },

    _onRequestMoreItems: function (){
        this.fetchCards();
    },
    
    renderCard: function (card, index){
        return <ListCard manga={card} key={index}/>;
    },

    render: function() {
        return(
           <div className="container">
           <div className="row">
                <div className="popular-list">
                    <div className="title-green">Popular Manga</div>
                    {this.state.error? 
                            <Alert msg={'There is some trouble with the system! please reload this page'} />:
                        <InfiniteScroll
                        hasMore={true}
                        onRequestMoreItems={this._onRequestMoreItems}
                        threshold={250}
                        style={styles.messagesList}>
                        <center>
                        {this.state.cards.map(this.renderCard)}
                        </center>
                        </InfiniteScroll>
                    }
                </div>
                <Loading loading={this.state.fetching} />
            </div>
            </div>
            );
    }
});

var styles = {
    wrapperList: {
        height: '250px',
        overflow: 'hidden'
    },
    messagesList: {
        height: '100%'
    },
}
module.exports = popular;