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
                asyncOptions={this.fetchSeries}
                name={this.props.name}
                ref="selectSeries"
                
                value={this.props.value}
                onChange={this._onChange} />
        );
    },

    fetchSeries: function (input, callback) {
        input = input.toLowerCase();
        if(input.length > 1) {
            $.get('cms/series/search?q=' + input, function (result) {
                console.log(result);
                var opts = {}
                if (result.rows.length > 0) {
                    opts = {
                        options: result.rows,
                        complete: true
                    };
                    console.log('search');
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