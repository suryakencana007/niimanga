var React = require('react');

module.exports = React.createClass({
    render: function() {
        console.log(this.props.token);
        return (
            <div>
                <div className="container">
                    <div className="row">
                        <div className="latest-list col-md-12">
                            <div className="title-green">Selamat Datang di CMS Niimanga</div>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
});