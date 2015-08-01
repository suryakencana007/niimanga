var React = require('react'),
    _ = require('lodash'),
    $ = require('jquery'),
    GridTable = require('components/Grid'),
    Modal = require('components/modal'),
    Form = require('pages/group/form');

module.exports = React.createClass({
    getInitialState: function () {
        return {
            files: [],
            number: 0
        }
    },

    componentDidMount: function () {
        var node = React.findDOMNode(this.refs.formGroup);
        this.$modal = $(node);

        //emitter.on(constants.changed, function() {
        //    this.$el.modal("hide");
        //}.bind(this));
    },

    _onClickBtnAdd: function () {
        this.refs.formGroup.show();
    },

    _onClickSave: function() {
        var arrform = this.$modal.find('form').serializeArray();
        var data = {};
        _.map(arrform, function(arr, i){
            console.log(arr)
            data[arr.name] = arr.value;
        });
        var self = this;
        $.post('/cms/grp/save-new', data)
            .done(function( data ) {
                self.refs.tableGroup.refresh();
                self.refs.formGroup.close();
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

                            <GridTable ref="tableGroup" handleAdd={this._onClickBtnAdd} btnadd="true" url="/cms/grp/src" usave="/cms/grp/edit-able" fields={
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