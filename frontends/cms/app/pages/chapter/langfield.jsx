var React = require("react"),
    Select = require('components/selectfield/Select');

module.exports = React.createClass({
    getDefaultProps: function () {
        return {
            searchable: false
        };
    },

    getInitialState: function() {
        return {
            value: null
        };
    },

    _onChange: function(newValue) {
        if(this.props.onChange)this.props.onChange(newValue);
    },

    render: function () {
        return (
            <Select
                asyncOptions={this.fetchLangs}
                name={this.props.name}
                ref="selectLang"
                searchable={this.props.searchable}
                value={this.props.value}
                onChange={this._onChange} />
        );
    },

    fetchLangs: function (input, callback) {
        input = input.toLowerCase();
        if(input.length > 0) {
            $.get('cms/chapter/lang', function (result) {
                console.log(result);
                var opts = {}
                if (result.rows.length > 0) {
                    opts = {
                        options: result.rows,
                        complete: true
                    };
                } else {
                    opts.complete = false;
                }
                callback(null, opts);
                return;
            });
        }
        callback(null, {complete: false});
    }
});