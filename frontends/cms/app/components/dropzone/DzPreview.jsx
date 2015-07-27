var React = require('react');
var filesize = require('components/dropzone/filesize');
var DzPreview = React.createClass({

    getDefaultProps: function() {
        return {
            file: {}
        };
    },

    getInitialState: function() {
        return {
            thumbnail: null
        };
    },

    onClick: function(e) {
        e.preventDefault();
        e.stopPropagation();
    },

    getProgress: function() {
        var file = this.props.file;

        var percent = file.percent || 0;

        percent = Math.ceil(percent * 100) / 100;
        var css = {width: percent + '%'};
        if (typeof file.done === 'string') {
            return <span className="dz-error-message">{file.done}</span>;
        }

        return [
            <div className="dz-progress" key="1">
                <span className="dz-upload" style={css}></span>
            </div>,
            <span className="dz-percent" key="2">{css.width}</span>
        ];
    },

    getClassName: function(file) {
        if (file.done === true) {
            return 'dz-preview dz-success';
        }

        if (typeof file.done === 'string') {
            return 'dz-preview dz-error';
        }

        return 'dz-preview';
    },

    _getExt: function(file) {
        var ext = '';
        if (file.type) {
            ext = file.type.split('/')[1];
        }

        if (!ext || ext.length > 4) {
            var names = file.name.split('.');
            var extName = names[names.length - 1];
            ext = extName || ext;
        }

        return ext;
    },

    render: function() {
        var file = this.props.file;
        var size = filesize(file.size);
        var progress = this.getProgress();
        var imageStyle = {};

        var imgCls = 'cover-image';
        if (file.thumbnail) {
            imageStyle.backgroundImage = 'url(' + file.thumbnail + ')';
        } else {
            imgCls += ' dz-file-type';
        }

        var classname = this.getClassName(file);
        var ext = this._getExt(file);

        return (
            <div className="card books small left-cover" data-uuid={file.uuid} onClick={this.onClick}>
                <div className="card-content">
                    <div className="wrapper-ribbon">
                        <div className="corner-ribbon top-right shadow batoto">{ext}</div>
                    </div>

                    <div className="detail">
                        <div className="dz-filename">
                            Filename：
                            <span title={file.name} className="dz-filename-text">{file.name}</span>
                        </div>
                        <div className="dz-size">
                            <span>Size：{size.join(' ')}</span>
                        </div>
                        {progress}
                    </div>
                </div>
            </div>
        );
    }
});

module.exports = DzPreview;
