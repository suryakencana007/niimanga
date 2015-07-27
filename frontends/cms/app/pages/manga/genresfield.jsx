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
                asyncOptions={this.fetchGenres}
                name={this.props.name}
                ref="genreSeries"
                delimiter=","
				multi={true}
				allowCreate={true}
                searchable={this.props.searchable}
                value={this.props.value}
                onChange={this._onChange} />
        );
    },

    fetchGenres: function (input, callback) {
        input = input.toLowerCase();
        if(input.length > 1) {
            $.get('api/v1/genres?q=' + input, function (result) {
                console.log(result);
                var opts = {}
                if (result.rows.length > 0) {
                    var rows = result.rows;
                    rows = Object.keys(rows).map(function(key){
                        return {label: rows[key].label, value: rows[key].label}
                    });
                    opts = {
                        options: rows,
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