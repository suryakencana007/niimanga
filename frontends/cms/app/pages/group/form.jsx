var React = require("react");

module.exports = React.createClass({

    render: function() {
        return (
            <form className="form-horizontal">
                <div className="form-group">
                    <label className="col-md-4 control-label" for="name">Group Name</label>
                    <div className="col-md-6">
                        <input id="name" name="name" type="text" placeholder="Group Name" className="form-control input-md" />
                        <span className="help-block">Here goes your group name</span>
                    </div>
                </div>
            </form>
        );
    }
});