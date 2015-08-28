import $ from 'jquery';
import _ from 'lodash';
import React, {Component, PropTypes, findDOMNode} from 'react/addons';

export default class GridTable extends Component {
    static propTypes = {
        init: PropTypes.bool,
        search: PropTypes.bool,
        refresh: PropTypes.bool,
        clickToSelect: PropTypes.bool,
        singleSelect: PropTypes.bool,
        usave: PropTypes.string,
        save: PropTypes.func,
        onCheckRow: PropTypes.func,
        onClickRow: PropTypes.func,
        onClickEdit: PropTypes.func,
        onClickRemove: PropTypes.func
    };

    static defaultProps = {
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

    constructor() {
        super();
        this._init = this._init.bind(this);
        this._onClickEdit = this._onClickEdit.bind(this);
        this._onClickRemove = this._onClickRemove.bind(this);
        this._onEditable = this._onEditable.bind(this);
        this._onEditableSave = this._onEditableSave.bind(this);
        this._onUnCheckRow = this._onUnCheckRow.bind(this);
        this._onCheckRow = this._onCheckRow.bind(this);
        this._onClickRow = this._onClickRow.bind(this);
        this.refresh = this.refresh.bind(this);
        this.insertDataRow = this.insertDataRow.bind(this);
        this.updateRow = this.updateRow.bind(this);
        this.removeRow = this.removeRow.bind(this);
        this.setDataSet = this.setDataSet.bind(this);
        this.getDataSet = this.getDataSet.bind(this);
        this.getRowSelection = this.getRowSelection.bind(this);
        this.renderFields = this.renderFields.bind(this);
    }

    componentDidMount() {
        this._init();
    }

    componentWillUnmount() {        
        this.$grid.bootstrapTable('destroy');
    }

    _init() {
        var node = findDOMNode(this.refs.table);
        this.$grid = $(node);
        
        let fields = [
            { 
                'field': 'action', 'title': 'ACTION',
                'formatter':[
                    '<a class="edit" href="javascript:void(0)" title="Edit">',
                    '<i class="fa fa-pencil-square-o fa-fw"></i>',
                    '</a>',
                    '<a class="remove" href="javascript:void(0)" title="Remove">',
                    '<i class="fa fa-trash-o fa-fw"></i>',
                    '</a>'
                ].join(''),
                'events': { 
                    'click .edit': this._onClickEdit, 
                    'click .remove': this._onClickRemove
                }
            }
        ];
        fields = _.union(fields, this.props.fields);
        this.$grid.bootstrapTable({
            url: this.props.url,
            method: this.props.method || 'POST',
            columns: fields
        });
        // console.log(fields);
        // events grid table
        if (this.props.usave) this._onEditableSave(this.props.usave);
        if (this.props.save) this._onEditable();
        if (this.props.onCheckRow) this._onCheckRow();
        if (this.props.onUnCheckRow) this._onUnCheckRow();
        if (this.props.onClickRow) this._onClickRow();
    }

    _onClickEdit(e, value, row, index){
        this.props.onClickEdit && this.props.onClickEdit(row, index);
    }

    _onClickRemove(e, value, row, index){
        this.props.onClickRemove && this.props.onClickRemove(row, index);
    }

    _onEditable() {
        var self = this;
        self.$grid.on('editable-save.bs.table', function($el, field, row, old, col) {
            var index = col.parents('tr[data-index]').data('index');
            // console.log(index);
            self.props.save(field, row, old, index);
        });
    }

    _onEditableSave(url) {
        //var node = findDOMNode(this.refs.table);
        //var $table = $(this.$grid);
        var self = this;
        self.$grid.on('editable-save.bs.table', function($el, field, row, old) {
            $.post(url,
                { row:JSON.stringify(row), old:old, field:field})
            .done(function( data ) {
                self.$grid.bootstrapTable('refresh');
            });            
        });
    }

    _onUnCheckRow() {        
        var self = this;
        self.$grid.on('uncheck.bs.table', function($el, data){
            // data = {}
            self.props.onUnCheckRow(data);
        });
    }

    _onCheckRow() {
        var self = this;
        self.$grid.on('check.bs.table', function($el, data){
            // data = {}
            self.props.onCheckRow(data);
        });
    }

    _onClickRow() {
        var self = this;
        self.$grid.on('click-row.bs.table', function($el, data){
            // data = {}
            self.props.onClickRow(data);
        });
    }

    refresh() {
        this.$grid.bootstrapTable('refresh');
        console.log('refresh');
    }

    insertDataRow(data) {
        // data = {}
        this.$grid.bootstrapTable('insertRow', {
            index: 0,
            row: data
        });
    }

    insertDataRows(data) {
        // data = []
        this.$grid.bootstrapTable('append', data);
        this.$grid.bootstrapTable('scrollTo', 'bottom');
        this.refresh();
    }

    updateRow(i, data) {
        // data = {}
        this.$grid.bootstrapTable('updateRow', {index: i, row: data});
        this.refresh();
    }

    removeRow(field, data) {
        // data = [value, value]
        this.$grid.bootstrapTable('remove', {field: field, values: data});
        this.refresh();
    }

    setDataSet(data) {
        console.log(data);
        this.$grid.bootstrapTable('load', data);
    }

    getDataSet() {
        return this.$grid.bootstrapTable('getData');
    }

    getRowSelection() {
        return this.$grid.bootstrapTable('getSelections');
    }

    renderFields(data, index) {
        return (
            <th data-field={data.field}
            data-visible={data.visible || true}
            data-type={data.type || 'text'}
            data-editable={data.editable || false}>{data.value}</th>
            );
    }

    render(): any {
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
            data-height="650">
            </table>
            </div>
            );
    }
}