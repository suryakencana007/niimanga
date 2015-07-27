var $ = require('jquery');
var React = require('react');

module.exports = React.createClass({
    propTypes: {
        init: React.PropTypes.bool,
        search: React.PropTypes.bool,
        refresh: React.PropTypes.bool,
        clickToSelect: React.PropTypes.bool,
        singleSelect: React.PropTypes.bool,
        usave: React.PropTypes.func,
        save: React.PropTypes.func,
        onCheckRow: React.PropTypes.func,
        onClickRow: React.PropTypes.func
    },

    getDefaultProps: function() {
        return {
            init: true,
            search: true,
            refresh: true,
            clickToSelect: false,
            singleSelect: false,
            usave: undefined,
            save: undefined,
            onCheckRow: undefined,
            onClickRow: undefined
        };
    },

    componentDidMount: function () {
        this._init();
    },

    componentWillUnmount: function () {
        //this.$grid = React.findDOMNode(this.refs.table);
        this.$grid.bootstrapTable('destroy');
    },

    _init: function () {
        var node = React.findDOMNode(this.refs.table);
        this.$grid = $(node);
        
        this.$grid.bootstrapTable({
            url: this.props.url,
            method: this.props.method || 'POST',
            columns: this.props.fields
        });

        // events grid table
        if (this.props.usave) this._onEditableSave(this.props.usave);        
        if (this.props.save) this._onEditable();
        if (this.props.onCheckRow) this._onCheckRow();
        if (this.props.onUnCheckRow) this._onUnCheckRow();
        if (this.props.onClickRow) this._onClickRow();
    },

    _onEditable: function () {
        var self = this;
        self.$grid.on('editable-save.bs.table', function($el, field, row, old, col) {            
            var index = col.parents('tr[data-index]').data('index');
            // console.log(index);
            self.props.save(field, row, old, index);
        });
    },

    _onEditableSave: function (url){
        //var node = React.findDOMNode(this.refs.table);
        //var $table = $(this.$grid);
        var self = this;
        self.$grid.on('editable-save.bs.table', function($el, field, row, old) {
            $.post(url,
                { row:JSON.stringify(row), old:old, field:field})
            .done(function( data ) {
                self.$grid.bootstrapTable('refresh');
            });            
        });
    },

    _onUnCheckRow: function () {        
        var self = this;
        self.$grid.on('uncheck.bs.table', function($el, data){
            // data = {}
            self.props.onUnCheckRow(data);
        });
    },

    _onCheckRow: function () {
        var self = this;
        self.$grid.on('check.bs.table', function($el, data){
            // data = {}
            self.props.onCheckRow(data);
        });
    },

    _onClickRow: function () {
        var self = this;
        self.$grid.on('click-row.bs.table', function($el, data){
            // data = {}
            self.props.onClickRow(data);
        });
    },

    refresh: function () {
        this.$grid.bootstrapTable('refresh');
        console.log('refresh');
    },

    insertDataRow: function (data) {
        // data = {}
        this.$grid.bootstrapTable('insertRow', {
            index: 0,
            row: data
        });
    },

    insertDataRows: function (data) {
        // data = []
        this.$grid.bootstrapTable('append', data);
        this.$grid.bootstrapTable('scrollTo', 'bottom');
        this.refresh();
    },

    updateRow: function (i, data) {
        // data = {}
        this.$grid.bootstrapTable('updateRow', {index: i, row: data});
        this.refresh();
    },

    removeRow: function (field, data) {
        // data = [value, value]
        this.$grid.bootstrapTable('remove', {field: field, values: data});
        this.refresh();
    },

    setDataSet: function (data) {
        console.log(data);
        this.$grid.bootstrapTable('load', data);
    },

    getDataSet: function () {
        return this.$grid.bootstrapTable('getData');
    },

    getRowSelection: function () {
        return this.$grid.bootstrapTable('getSelections');
    },

    renderFields: function (data, index) {
        return (
            <th data-field={data.field}
            data-visible={data.visible || true}
            data-type={data.type || 'text'}
            data-editable={data.editable || false}>{data.value}</th>
            );
    },

    render: function () {
        return (
            <div className="col-xs-12 col-sm-12">
            {this.props.btnadd ? <button className="btn btn-default" onClick={this.props.handleAdd}><i className="glyphicon glyphicon-plus"></i></button> : null}
            <table ref="table"
            data-toolbar="#post"
            data-show-refresh={this.props.refresh}
            data-search-align="left"
            data-buttons-align="left"
            data-toolbar-align="right"
            data-pagination="true"
            data-side-pagination="server"
            data-page-list="[5, 10, 20, 50, 100, 200]"
            data-search={this.props.search}
            data-check-on-init={this.props.init}
            data-click-to-select={this.props.clickToSelect}
            data-single-select={this.props.singleSelect}
            data-height="480">
            </table>
            </div>
            );
    }
});