/******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, {
/******/ 				configurable: false,
/******/ 				enumerable: true,
/******/ 				get: getter
/******/ 			});
/******/ 		}
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = 0);
/******/ })
/************************************************************************/
/******/ ([
/* 0 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var _muban = __webpack_require__(1);

var _flowchart = __webpack_require__(2);

var liucheng = _interopRequireWildcard(_flowchart);

function _interopRequireWildcard(obj) { if (obj && obj.__esModule) { return obj; } else { var newObj = {}; if (obj != null) { for (var key in obj) { if (Object.prototype.hasOwnProperty.call(obj, key)) newObj[key] = obj[key]; } } newObj.default = obj; return newObj; } }

window.MubanManager = _muban.MubanManager;

/***/ }),
/* 1 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
    value: true
});

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

var MubanManager = exports.MubanManager = function () {
    function MubanManager(muban_table_url) {
        _classCallCheck(this, MubanManager);

        this.table_url = muban_table_url;
        this.vue_inst = null;
        this.select_callback = null;
    }

    _createClass(MubanManager, [{
        key: 'select',
        value: function select(callback) {
            if (!this.vue_inst) {
                this.vue_inst = this._mount();
            }
            this.vue_inst.show_me = true;
            this.select_callback = callback;
        }
    }, {
        key: '_mount',
        value: function _mount() {
            $('body').append('<div id="_muban_list">\n        <modal v-show="show_me" @click.native="show_me=false">\n              <muban-list class="muban-list" @click.native.stop="" table_url="' + this.table_url + '"></muban-list>\n        </modal>\n        </div>');
            var manager = this;
            window._muban_list = new Vue({
                el: '#_muban_list',
                data: {
                    show_me: false
                },
                mounted: function mounted() {
                    this.$on('row-click', function (row) {
                        manager.select_callback(row);
                    });
                }
            });
            return window._muban_list;
        }
    }]);

    return MubanManager;
}();

function emit_to_parent(com_inst, event_name, arg) {
    var par = com_inst.$parent;
    while (par) {
        var rt = par.$emit(event_name, arg);
        par = par.$parent;
    }
}

var muban_list = {
    props: ['table_url'],
    data: function data() {
        return {
            heads: [],
            rows: [],
            row_pages: {
                options: [],
                crt_page: 1
            }
        };
    },
    mixins: [table_fun],
    mounted: function mounted() {
        this.goto_page(1);
    },
    methods: {
        goto_page: function goto_page(page_num) {
            var self = this;
            var url = ex.appendSearch(this.table_url, { _page: page_num });
            ex.get(url, function (resp) {

                self.heads = resp.heads;
                self.rows = resp.rows;
                self.row_pages = resp.row_pages;

                self.heads[0].type = "click-td";
                ex.each(self.heads, function (head) {
                    if (head.name == 'relations') {
                        head.type = "flowchart-td";
                    }
                });
            });
        }
    },
    template: '<div>\n        <com-table class=\'table fake-suit\' :has_check="false" :map="map"\n            :heads="heads" :rows="rows" v-model="selected"></com-table>\n\n        <paginator :nums=\'row_pages.options\' :crt=\'row_pages.crt_page\' @goto_page=\'goto_page($event)\'></paginator>\n    </div>'
};
Vue.component('muban-list', muban_list);

var click_td = {
    props: ['name', 'row'],
    template: '<span  @click="on_click()" v-text="row[name]"></span>',
    methods: {
        on_click: function on_click() {
            //this.$parent.$emit('row-click',this.row)
            emit_to_parent(this, 'row-click', this.row);
        }
    }
};
Vue.component('click-td', click_td);

/***/ }),
/* 2 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var flowchart_base = {
    template: '<div class="mermaid" v-text="memraid_text">\n    </div>',
    props: ['node_group'],
    mounted: function mounted() {},
    computed: {
        memraid_text: function memraid_text() {
            var text = "graph LR;";
            ex.each(this.node_group.nodes, function (node) {
                if (node.short_desp) {
                    text += ex.template('{id}["{desp}"];', { id: node.id, desp: node.short_desp });
                } else {
                    text += ex.template('{id};', { id: node.id });
                }
            });
            ex.each(this.node_group.relations, function (relation) {
                text += ex.template("{src}-->{dst};", { src: relation[0], dst: relation[1] });
            });
            return text;
        }
    }
};
Vue.component('com-flowchart', flowchart_base);

var flowchart_td = {
    props: ['name', 'row'],
    template: ' <div class="mermaid" v-text="memraid_text"></div>',
    mounted: function mounted() {
        this.render();
    },
    watch: {
        memraid_text: function memraid_text() {
            this.render();
        }
    },
    computed: {
        node_group: function node_group() {
            var node_group_local = ex.copy(this.row);
            //node_group_local.relations=JSON.parse(node_group_local.relations)
            return node_group_local;
        },
        memraid_text: function memraid_text() {
            var text = "graph LR;";
            ex.each(this.node_group.nodes, function (node) {
                if (node.short_desp) {
                    text += ex.template('{id}["{desp}"];', { id: node.id, desp: node.short_desp });
                } else {
                    text += ex.template('{id};', { id: node.id });
                }
            });
            ex.each(this.node_group.relations, function (relation) {
                text += ex.template("{src}-->{dst};", { src: relation[0], dst: relation[1] });
            });
            return text;
        }
    },
    methods: {
        render: function render() {
            var self = this;
            Vue.nextTick(function () {
                mermaid.init({ noteMargin: 10 }, self.$el);
            });
        }
    }

};
Vue.component('flowchart-td', flowchart_td);

/***/ })
/******/ ]);