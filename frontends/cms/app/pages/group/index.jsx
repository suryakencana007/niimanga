var React = require('react');
var _ = require('lodash');
var api = require('utils/api');
var cache = require('utils/cache');
var GridTable = require('components/Grid');
var Form = require('pages/group/form');

module.exports = React.createClass({
    getInitialState: function () {
        return {
            files: [],
            number: 0
        }
    },

    componentDidMount: function () {
      
    },

    _onClickBtnAdd: function () {
      
    },

    _onClickSave: function() {
        var arrform = this.$form.find('form').serializeArray();
        var data = {};
        _.map(arrform, function(arr, i){
            console.log(arr)
            data[arr.name] = arr.value;
        });
        var self = this;
        api.post('/cms/grp/save-new', data, this.props.token)
            .then(function( data ) {
                cache.expire(this.props.token, url);
                self.refs.tableGroup.refresh();
            });
        console.log('save on');
    },

    _onChange: function () {

    },

    render: function() {
        return (
            <div>
                <div className="container">
                    <div className="row">
                        <div className="latest-list col-md-12">
                            <div className="title-green">Table Groups</div>

                            <GridTable ref="tableGroup" 
                            handleAdd={this._onClickBtnAdd} 
                            btnadd="true" 

                            url="/cms/grp/src" fields={
                                [
                                    { 'field': 'id', 'title': 'ID'},
                                    { 'field': 'name', 'title': 'Group Name', 'editable': true},
                                    { 'field': 'slug', 'title': 'Slug Name', 'editable': true}
                                ]
                                }
                            />
                        </div>
                    </div>
                </div>
                <Modal ref="formGroup"
                    title="Group Form"
                    body={Form}
                    save={this._onClickSave}
                />
            </div>
        );
    }
});