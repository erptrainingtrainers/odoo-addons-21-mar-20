odoo.define('clg_base.Dashboard', function (require) {
"use strict";

var AbstractAction = require('web.AbstractAction');
var core = require('web.core');
var rpc = require('web.rpc');
var session = require('web.session');
var _t = core._t;
var QWeb = core.qweb;

var StudentDashboard = AbstractAction.extend({
	template: 'DashboardMain',
	
	init: function(parent, action, options) {
		this._super.apply(this, arguments);
        console.log("Init called");
    },
    
    start: function() {
      console.log("START called")
      var self = this;
      self.fetch_data();
      this._super.apply(this, arguments);
    },
    
    fetch_data: function() {
    	console.log("Fetch Data called");
    	var self = this;
        this._rpc({
                model: 'clg.student',
                method: 'get_student_details',
                args: [[]]
        }).then(function(result) {
        	console.log(result);
        	self.$('.o_dashboard').append(QWeb.render('StudentDetails', {widget: result}));
        });
    },
	
});

core.action_registry.add('student_dashboard', StudentDashboard);

return StudentDashboard;
});