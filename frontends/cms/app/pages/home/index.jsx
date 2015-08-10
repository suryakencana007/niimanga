var React = require('react');
var Button = require('components/base/button');

module.exports = React.createClass({
    render: function() {
        console.log(this.props.token);
        return (
            <div>
                <div className="container">
                    <div className="row">
                        <div className="latest-list col-md-12">
                            <div className="title-green">Selamat Datang di CMS Niimanga</div>
                            <Button>ok</Button>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
});