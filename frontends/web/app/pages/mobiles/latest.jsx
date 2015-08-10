var React = require('react');
var _ = require('lodash');
var Radium = require('radium');
var cache = require('utils/cache');
var api = require('utils/api');
var Loading = require('components/Loading');
var Alert = require('components/Alert');
var InfiniteScroll = require('components/scroller/InfiniteScroll');
var Card = require('components/manga/Card');


var latest = React.createClass({
    getInitialState: function () {
        return {
            limit: 10,
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
        var url = '/api/v1/latest?page=' + newState.offset + '&cards=' + newState.limit;
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

    _onScroll: function(e) {

    },
    
    renderCard: function (card, index){
        return <Card manga={card} key={index}/>;
    },

    render: function() {
        return(          
            <div className="row">
                <div className="latest-list">
                <div className="title-green">Latest Manga</div>
                    {this.state.error? 
                        <Alert msg={'There is some trouble with the system! please reload this page'} />:
                    <InfiniteScroll
                    onScroll={this._onScroll}
                    hasMore={true}
                    onRequestMoreItems={this._onRequestMoreItems}
                    threshold={250}
                    style={styles.messagesList}>
                    {this.state.cards.map(this.renderCard)}
                    </InfiniteScroll>
                }
                </div>
                <Loading loading={this.state.fetching} />
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
module.exports = latest;