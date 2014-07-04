'use strict';


// Declare app level module which depends on filters, and services
angular.module('myApp', [
  'ngRoute',
  'myApp.filters',
  'myApp.services',
  'myApp.directives',
  'myApp.controllers',
  'ngResource',
  'ngCookies',
  'ui.bootstrap'
]).
config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/calendar', {templateUrl: '../static/app/partials/calendar.html', controller: 'CalendarCtrl'});
  $routeProvider.when('/students', {templateUrl: '../static/app/partials/students.html', controller: 'StudentListCtrl'});
  $routeProvider.otherwise({redirectTo: '/'});
}]).
config(['$httpProvider', function($httpProvider){
        // django and angular both support csrf tokens. This tells
        // angular which cookie to add to what header.
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    }]).
    factory('api', function($resource){
        function add_auth_header(data, headersGetter){
            var headers = headersGetter();
            headers['Authorization'] = ('Basic ' + btoa(data.username +
                                        ':' + data.password));
        }
        return {
            auth: $resource('/api/auth/login\\/', {}, {
                login:  {method: 'POST', transformRequest: add_auth_header},
                logout: {method: 'DELETE'}
            }),
            users: $resource('/api/users\\/', {}, {
                create: {method: 'POST'}
            }),
            schools: $resource('/api/schools\\/', {}, {
                get: {method: 'GET', isArray: true}
            }),
            students: $resource('/api/students\\/', {},{
                get: {method: 'GET', isArray: true}
            })
        };
    });