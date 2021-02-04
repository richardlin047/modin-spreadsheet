var modin_spreadsheet = require('./index');

var base = require('@jupyter-widgets/base');

/**
 * The widget manager provider.
 */
module.exports = {
  id: 'modin_spreadsheet',
  requires: [base.IJupyterWidgetRegistry],
  activate: function(app, widgets) {
      widgets.registerWidget({
          name: 'modin_spreadsheet',
          version: modin_spreadsheet.version,
          exports: modin_spreadsheet
      });
    },
  autoStart: true
};
