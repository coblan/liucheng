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
/******/ 	return __webpack_require__(__webpack_require__.s = 2);
/******/ })
/************************************************************************/
/******/ ([
/* 0 */
/***/ (function(module, exports) {

/*
	MIT License http://www.opensource.org/licenses/mit-license.php
	Author Tobias Koppers @sokra
*/
// css base code, injected by the css-loader
module.exports = function() {
	var list = [];

	// return the list of modules as css string
	list.toString = function toString() {
		var result = [];
		for(var i = 0; i < this.length; i++) {
			var item = this[i];
			if(item[2]) {
				result.push("@media " + item[2] + "{" + item[1] + "}");
			} else {
				result.push(item[1]);
			}
		}
		return result.join("");
	};

	// import a list of modules into the list
	list.i = function(modules, mediaQuery) {
		if(typeof modules === "string")
			modules = [[null, modules, ""]];
		var alreadyImportedModules = {};
		for(var i = 0; i < this.length; i++) {
			var id = this[i][0];
			if(typeof id === "number")
				alreadyImportedModules[id] = true;
		}
		for(i = 0; i < modules.length; i++) {
			var item = modules[i];
			// skip already imported module
			// this implementation is not 100% perfect for weird media query combinations
			//  when a module is imported multiple times with different media queries.
			//  I hope this will never occur (Hey this way we have smaller bundles)
			if(typeof item[0] !== "number" || !alreadyImportedModules[item[0]]) {
				if(mediaQuery && !item[2]) {
					item[2] = mediaQuery;
				} else if(mediaQuery) {
					item[2] = "(" + item[2] + ") and (" + mediaQuery + ")";
				}
				list.push(item);
			}
		}
	};
	return list;
};


/***/ }),
/* 1 */
/***/ (function(module, exports) {

/*
	MIT License http://www.opensource.org/licenses/mit-license.php
	Author Tobias Koppers @sokra
*/
var stylesInDom = {},
	memoize = function(fn) {
		var memo;
		return function () {
			if (typeof memo === "undefined") memo = fn.apply(this, arguments);
			return memo;
		};
	},
	isOldIE = memoize(function() {
		return /msie [6-9]\b/.test(window.navigator.userAgent.toLowerCase());
	}),
	getHeadElement = memoize(function () {
		return document.head || document.getElementsByTagName("head")[0];
	}),
	singletonElement = null,
	singletonCounter = 0,
	styleElementsInsertedAtTop = [];

module.exports = function(list, options) {
	if(typeof DEBUG !== "undefined" && DEBUG) {
		if(typeof document !== "object") throw new Error("The style-loader cannot be used in a non-browser environment");
	}

	options = options || {};
	// Force single-tag solution on IE6-9, which has a hard limit on the # of <style>
	// tags it will allow on a page
	if (typeof options.singleton === "undefined") options.singleton = isOldIE();

	// By default, add <style> tags to the bottom of <head>.
	if (typeof options.insertAt === "undefined") options.insertAt = "bottom";

	var styles = listToStyles(list);
	addStylesToDom(styles, options);

	return function update(newList) {
		var mayRemove = [];
		for(var i = 0; i < styles.length; i++) {
			var item = styles[i];
			var domStyle = stylesInDom[item.id];
			domStyle.refs--;
			mayRemove.push(domStyle);
		}
		if(newList) {
			var newStyles = listToStyles(newList);
			addStylesToDom(newStyles, options);
		}
		for(var i = 0; i < mayRemove.length; i++) {
			var domStyle = mayRemove[i];
			if(domStyle.refs === 0) {
				for(var j = 0; j < domStyle.parts.length; j++)
					domStyle.parts[j]();
				delete stylesInDom[domStyle.id];
			}
		}
	};
}

function addStylesToDom(styles, options) {
	for(var i = 0; i < styles.length; i++) {
		var item = styles[i];
		var domStyle = stylesInDom[item.id];
		if(domStyle) {
			domStyle.refs++;
			for(var j = 0; j < domStyle.parts.length; j++) {
				domStyle.parts[j](item.parts[j]);
			}
			for(; j < item.parts.length; j++) {
				domStyle.parts.push(addStyle(item.parts[j], options));
			}
		} else {
			var parts = [];
			for(var j = 0; j < item.parts.length; j++) {
				parts.push(addStyle(item.parts[j], options));
			}
			stylesInDom[item.id] = {id: item.id, refs: 1, parts: parts};
		}
	}
}

function listToStyles(list) {
	var styles = [];
	var newStyles = {};
	for(var i = 0; i < list.length; i++) {
		var item = list[i];
		var id = item[0];
		var css = item[1];
		var media = item[2];
		var sourceMap = item[3];
		var part = {css: css, media: media, sourceMap: sourceMap};
		if(!newStyles[id])
			styles.push(newStyles[id] = {id: id, parts: [part]});
		else
			newStyles[id].parts.push(part);
	}
	return styles;
}

function insertStyleElement(options, styleElement) {
	var head = getHeadElement();
	var lastStyleElementInsertedAtTop = styleElementsInsertedAtTop[styleElementsInsertedAtTop.length - 1];
	if (options.insertAt === "top") {
		if(!lastStyleElementInsertedAtTop) {
			head.insertBefore(styleElement, head.firstChild);
		} else if(lastStyleElementInsertedAtTop.nextSibling) {
			head.insertBefore(styleElement, lastStyleElementInsertedAtTop.nextSibling);
		} else {
			head.appendChild(styleElement);
		}
		styleElementsInsertedAtTop.push(styleElement);
	} else if (options.insertAt === "bottom") {
		head.appendChild(styleElement);
	} else {
		throw new Error("Invalid value for parameter 'insertAt'. Must be 'top' or 'bottom'.");
	}
}

function removeStyleElement(styleElement) {
	styleElement.parentNode.removeChild(styleElement);
	var idx = styleElementsInsertedAtTop.indexOf(styleElement);
	if(idx >= 0) {
		styleElementsInsertedAtTop.splice(idx, 1);
	}
}

function createStyleElement(options) {
	var styleElement = document.createElement("style");
	styleElement.type = "text/css";
	insertStyleElement(options, styleElement);
	return styleElement;
}

function createLinkElement(options) {
	var linkElement = document.createElement("link");
	linkElement.rel = "stylesheet";
	insertStyleElement(options, linkElement);
	return linkElement;
}

function addStyle(obj, options) {
	var styleElement, update, remove;

	if (options.singleton) {
		var styleIndex = singletonCounter++;
		styleElement = singletonElement || (singletonElement = createStyleElement(options));
		update = applyToSingletonTag.bind(null, styleElement, styleIndex, false);
		remove = applyToSingletonTag.bind(null, styleElement, styleIndex, true);
	} else if(obj.sourceMap &&
		typeof URL === "function" &&
		typeof URL.createObjectURL === "function" &&
		typeof URL.revokeObjectURL === "function" &&
		typeof Blob === "function" &&
		typeof btoa === "function") {
		styleElement = createLinkElement(options);
		update = updateLink.bind(null, styleElement);
		remove = function() {
			removeStyleElement(styleElement);
			if(styleElement.href)
				URL.revokeObjectURL(styleElement.href);
		};
	} else {
		styleElement = createStyleElement(options);
		update = applyToTag.bind(null, styleElement);
		remove = function() {
			removeStyleElement(styleElement);
		};
	}

	update(obj);

	return function updateStyle(newObj) {
		if(newObj) {
			if(newObj.css === obj.css && newObj.media === obj.media && newObj.sourceMap === obj.sourceMap)
				return;
			update(obj = newObj);
		} else {
			remove();
		}
	};
}

var replaceText = (function () {
	var textStore = [];

	return function (index, replacement) {
		textStore[index] = replacement;
		return textStore.filter(Boolean).join('\n');
	};
})();

function applyToSingletonTag(styleElement, index, remove, obj) {
	var css = remove ? "" : obj.css;

	if (styleElement.styleSheet) {
		styleElement.styleSheet.cssText = replaceText(index, css);
	} else {
		var cssNode = document.createTextNode(css);
		var childNodes = styleElement.childNodes;
		if (childNodes[index]) styleElement.removeChild(childNodes[index]);
		if (childNodes.length) {
			styleElement.insertBefore(cssNode, childNodes[index]);
		} else {
			styleElement.appendChild(cssNode);
		}
	}
}

function applyToTag(styleElement, obj) {
	var css = obj.css;
	var media = obj.media;

	if(media) {
		styleElement.setAttribute("media", media)
	}

	if(styleElement.styleSheet) {
		styleElement.styleSheet.cssText = css;
	} else {
		while(styleElement.firstChild) {
			styleElement.removeChild(styleElement.firstChild);
		}
		styleElement.appendChild(document.createTextNode(css));
	}
}

function updateLink(linkElement, obj) {
	var css = obj.css;
	var sourceMap = obj.sourceMap;

	if(sourceMap) {
		// http://stackoverflow.com/a/26603875
		css += "\n/*# sourceMappingURL=data:application/json;base64," + btoa(unescape(encodeURIComponent(JSON.stringify(sourceMap)))) + " */";
	}

	var blob = new Blob([css], { type: "text/css" });

	var oldSrc = linkElement.href;

	linkElement.href = URL.createObjectURL(blob);

	if(oldSrc)
		URL.revokeObjectURL(oldSrc);
}


/***/ }),
/* 2 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var _plan_board = __webpack_require__(3);

var plan_board = _interopRequireWildcard(_plan_board);

var _worktemplate = __webpack_require__(7);

function _interopRequireWildcard(obj) { if (obj && obj.__esModule) { return obj; } else { var newObj = {}; if (obj != null) { for (var key in obj) { if (Object.prototype.hasOwnProperty.call(obj, key)) newObj[key] = obj[key]; } } newObj.default = obj; return newObj; } }

//import {MubanManager}  from './muban.js'
//import * as liucheng from './flowchart.js'
//import {mount_user_image} from  './flowchart.js'
//import {WorkNodeEditor} from './worknode_editor.js'
//import {flow_has_node_delay} from  './flow_filter.js'
//
//window.MubanManager=MubanManager
//window.mount_user_image=mount_user_image
//window.WorkNodeEditor=WorkNodeEditor
//
//window.flow_has_node_delay=flow_has_node_delay

window.WorkTemplateEditor = _worktemplate.WorkTemplateEditor;

/***/ }),
/* 3 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var _worknode = __webpack_require__(4);

__webpack_require__(5);


var node_editor = new _worknode.WorkNodeEditor();

var plan_board = {
    props: ['row', 'name'],
    //computed:{
    //  nodes:function(){
    //      return this.row.nodes
    //  }
    //},
    data: function data() {
        return {
            is_edit: false,
            show_edit: false
        };
    },

    methods: {
        add_new: function add_new() {
            var self = this;
            var init_node = {
                work_group: self.row.pk,
                status: 'waiting',
                start_time: '',
                _class: 'workboard.worknode'
            };
            node_editor.edit(init_node, function (node) {
                self.row.nodes.push(node);
            });
        },
        toggle_edit: function toggle_edit() {
            this.is_edit = !this.is_edit;
        },
        edit: function edit(node) {
            var tmp_node = ex.copy(node);
            node_editor.edit(tmp_node, function (rt_node) {
                ex.assign(node, rt_node);
            });
        },
        delete_node: function delete_node(node) {
            var r = confirm('真的删除吗？');
            if (r) {
                ex.remove(this.row.nodes, node);
                var post_data = [{ fun: 'del_rows', rows: [node] }];
                ex.post('/_ajax', JSON.stringify(post_data), function (resp) {});
            }
        },
        is_match_search: function is_match_search(node) {
            return is_matched_node(node);
        }
    },
    template: '<div class="flex plan" @mouseenter="show_edit=true" @mouseleave="show_edit=false">\n    <div v-show="show_edit" class="edit-btn" @click="toggle_edit()"><i class="fa fa-pencil-square-o fa-2x" aria-hidden="true"></i></div>\n    <div :class="[\'item\',{\'matched\':is_match_search(node)}]" v-for="node in row.nodes" @click="edit(node)" >\n        <div class="center-h text" >\n            <span v-text="node.short_desp"></span>\n        </div>\n        <div class="status-icon">\n            <span v-if="node.status==\'finish\'" style="color: #00dd00;"><i class="fa fa-check" aria-hidden="true"></i></span>\n            <span v-if="node.start_time"><i class="fa fa-clock-o" aria-hidden="true"></i></span>\n        </div>\n        <div class="delete-icon" v-if="is_edit" @click.stop="delete_node(node)">\n            <span><i class="fa fa-trash" aria-hidden="true"></i></span>\n        </div>\n    </div>\n    <div class="item" @click="add_new()" v-if="is_edit || row.nodes.length==0">\n        <div class="center-vh" >\n            <i class="fa fa-plus fa-2x" aria-hidden="true"></i>\n        </div>\n    </div>\n    </div>'
};

Vue.component('plan-board', plan_board);

function is_matched_node(node) {
    if (!node.start_time) {
        return false;
    }
    if (search_args.owner) {
        if (node.owner != search_args.owner) {
            return false;
        }
    }
    if (search_args._start_start_time) {
        if (node.start_time < search_args._start_start_time) {
            return false;
        }
    }
    if (search_args._end_start_time) {
        if (node.start_time > search_args._end_start_time) {
            return false;
        }
    }
    if (search_args.node_status) {
        if (node.status != search_args.node_status) {
            return false;
        }
    }
    if (!search_args._start_start_time && !search_args._end_start_time && !search_args.node_status && !search_args.owner) {
        return false;
    }
    return true;
}

/***/ }),
/* 4 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
    value: true
});

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

var WorkNodeEditor = exports.WorkNodeEditor = function () {
    function WorkNodeEditor() {
        _classCallCheck(this, WorkNodeEditor);

        var self = this;
        var url = engine_url + '/' + 'workboard.worknode.edit';
        ex.get(url, function (resp) {
            self.heads = resp.heads;
            self.heads = ex.sort_by_names(self.heads, ["short_desp", "owner", "status", "start_time", "long_desp"]);
            //ex.remove(self.heads,function(head){
            //    if(head.name=="work_group"){
            //        return true
            //    }
            //})
        });

        $(function () {
            $('body').append('<div id="worknode-editor">\n     <modal v-show="show_edit">\n        <div @click.stop="" style="max-height: 90vh;max-width: 90vw;">\n            <div style="text-align: right;padding-right: 1em;padding-top: 0.3em;">\n                <a :href="\'/pc/log?rows=workboard.worknode:\'+node_kw.row.pk" target="_blank">\u4FEE\u6539\u65E5\u5FD7</a>\n                <button @click="assure_edit()">\u786E\u5B9A</button>\n                <button @click="show_edit=false">\u53D6\u6D88</button>\n            </div>\n            <div  class=\'field-panel\'>\n                <field  v-for=\'head in node_kw.heads\' :key="head.name" :name=\'head.name\' :kw=\'node_kw\'></field>\n            </div>\n        </div>\n\n    </modal>\n            </div>');

            self.editor = new Vue({
                el: '#worknode-editor',
                data: {
                    show_edit: false,
                    node_kw: {
                        heads: [],
                        row: {},
                        errors: {}
                    }
                },
                methods: {
                    assure_edit: function assure_edit() {
                        var self = this;
                        show_upload();
                        var post_data = [{ fun: 'save', row: this.node_kw.row }];
                        ex.post('/_ajax', JSON.stringify(post_data), function (resp) {
                            if (resp.save.status == 'success') {
                                //var node=ex.findone(self.node_group.nodes,{pk:self.node_kw.row.pk})
                                var node = self.node_kw.row;
                                var new_node = resp.save.row;
                                ex.assign(node, new_node);
                                hide_upload(300);
                                self.show_edit = false;
                                self.callback(node);
                            }
                        });
                    }
                }
            });
        });
    }

    _createClass(WorkNodeEditor, [{
        key: 'edit',
        value: function edit(node, callback) {
            this.editor.node_kw.heads = this.heads;
            this.editor.node_kw.row = ex.copy(node);
            this.editor.show_edit = true;
            this.editor.callback = callback;
        }
    }]);

    return WorkNodeEditor;
}();

/***/ }),
/* 5 */
/***/ (function(module, exports, __webpack_require__) {

// style-loader: Adds some css to the DOM by adding a <style> tag

// load the styles
var content = __webpack_require__(6);
if(typeof content === 'string') content = [[module.i, content, '']];
// add the styles to the DOM
var update = __webpack_require__(1)(content, {});
if(content.locals) module.exports = content.locals;
// Hot Module Replacement
if(false) {
	// When the styles change, update the <style> tags
	if(!content.locals) {
		module.hot.accept("!!./../../../../../../coblan/webcode/node_modules/.0.26.1@css-loader/index.js!./../../../../../../coblan/webcode/node_modules/.6.0.0@sass-loader/lib/loader.js!./plan_board.scss", function() {
			var newContent = require("!!./../../../../../../coblan/webcode/node_modules/.0.26.1@css-loader/index.js!./../../../../../../coblan/webcode/node_modules/.6.0.0@sass-loader/lib/loader.js!./plan_board.scss");
			if(typeof newContent === 'string') newContent = [[module.id, newContent, '']];
			update(newContent);
		});
	}
	// When the module is disposed, remove the <style> tags
	module.hot.dispose(function() { update(); });
}

/***/ }),
/* 6 */
/***/ (function(module, exports, __webpack_require__) {

exports = module.exports = __webpack_require__(0)();
// imports


// module
exports.push([module.i, ".plan {\n  flex-wrap: wrap;\n  position: relative; }\n  .plan .item {\n    width: 7em;\n    height: 3em;\n    border: 1px solid #a8a8a8;\n    text-align: center;\n    position: relative;\n    cursor: pointer; }\n    .plan .item:hover {\n      background-color: #f6fcf0; }\n    .plan .item.matched {\n      border: 2px dashed red; }\n  .plan .edit-btn {\n    position: absolute;\n    left: -3em;\n    color: #ffb23d;\n    cursor: pointer;\n    padding: 0.3em 1em; }\n  .plan .text {\n    width: 7em; }\n  .plan .status-icon {\n    position: absolute;\n    right: 0.2em;\n    bottom: 0.2em; }\n  .plan .delete-icon {\n    position: absolute;\n    right: 0;\n    top: -0.2em;\n    color: red;\n    padding: 0.1em 0.4em;\n    border-radius: 2px; }\n    .plan .delete-icon:hover {\n      background-color: #cecece; }\n\n#id_long_desp {\n  width: 40em;\n  height: 26em; }\n", ""]);

// exports


/***/ }),
/* 7 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
    value: true
});

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

__webpack_require__(8);

var WorkTemplateEditor = exports.WorkTemplateEditor = function () {
    function WorkTemplateEditor() {
        _classCallCheck(this, WorkTemplateEditor);

        var self = this;

        $(function () {
            $('body').append('<div id="worktemplate-editor">\n     <modal v-show="show_edit">\n        <div @click.stop="" style="max-height: 90vh;max-width: 90vw;min-height: 40em;min-width: 50em;">\n            <div style="text-align: right;padding-right: 1em;padding-top: 0.3em;">\n                <!--<a :href="\'/pc/log?rows=workboard.worknode:\'+node_kw.row.pk" target="_blank">\u4FEE\u6539\u65E5\u5FD7</a>-->\n                <button @click="assure_edit()">\u786E\u5B9A</button>\n                <button @click="show_edit=false">\u53D6\u6D88</button>\n            </div>\n            <div  class=\'field-panel\'>\n                <field  v-for=\'head in kw.heads\' :key="head.name" :name=\'head.name\' :kw=\'kw\'></field>\n            </div>\n        </div>\n\n    </modal>\n            </div>');

            self.editor = new Vue({
                el: '#worktemplate-editor',
                data: {
                    show_edit: false,
                    editable: true,
                    kw: {
                        heads: [{ name: 'short_desp', type: 'linetext', label: '简短描述' }, { name: 'long_desp', type: 'blocktext', label: '详细描述' }],
                        row: { short_desp: '', long_desp: '' },
                        errors: {}
                    }
                },
                methods: {
                    assure_edit: function assure_edit() {
                        this.callback(this.kw.row);
                        this.show_edit = false;
                    }

                }
            });
        });
    }

    _createClass(WorkTemplateEditor, [{
        key: 'edit',
        value: function edit(node, callback) {
            //this.editor.node_kw.heads=this.heads
            this.editor.kw.row = ex.copy(node);
            this.editor.show_edit = true;
            this.editor.callback = callback;
        }
    }, {
        key: 'set_editable',
        value: function set_editable(editable) {
            if (editable) {
                this.editor.kw.heads = [{ name: 'short_desp', type: 'linetext', label: '简短描述' }, { name: 'long_desp', type: 'blocktext', label: '详细描述' }];
            } else {
                this.editor.kw.heads = [{ name: 'short_desp', type: 'linetext', label: '简短描述', readonly: true }, { name: 'long_desp', type: 'blocktext', label: '详细描述', readonly: true }];
            }
        }
    }]);

    return WorkTemplateEditor;
}();

var editor = new WorkTemplateEditor();

var com_worktemplate_pan = {
    props: ['content', 'editable'],
    //data:function(){
    //
    //    return {
    //
    //    }
    //},
    template: '<div class="flex work-template-pan">\n        <div class="item" v-for="node in content" @click="edit(node)">\n\n            <div class="center-h item" >\n                <span v-text="node.short_desp"></span>\n            </div>\n\n            <span v-if="editable" class="delete-btn" @click.stop="del_node(node)">\n               <i class="fa fa-trash" aria-hidden="true"></i>\n            </span>\n\n        </div>\n        <div v-if="editable" class="item" @click="add_new()">\n            <div class="center-vh">\n                <i class="fa fa-plus fa-2x" aria-hidden="true"></i>\n            </div>\n        </div>\n    </div>',
    data: function data() {
        return {
            count: 1
        };
    },
    methods: {
        add_new: function add_new() {

            var new_content = {
                short_desp: '工作步骤',
                long_desp: '',
                count: this.count
            };
            this.count += 1;

            this.content.push(new_content);
        },
        edit: function edit(node) {
            editor.set_editable(this.editable);
            editor.edit(node, function (new_node) {
                ex.assign(node, new_node);
            });
        },
        del_node: function del_node(node) {
            ex.remove(this.content, node);
        }
    }

};

Vue.component('com-worktemplate-pan', com_worktemplate_pan);

/***/ }),
/* 8 */
/***/ (function(module, exports, __webpack_require__) {

// style-loader: Adds some css to the DOM by adding a <style> tag

// load the styles
var content = __webpack_require__(9);
if(typeof content === 'string') content = [[module.i, content, '']];
// add the styles to the DOM
var update = __webpack_require__(1)(content, {});
if(content.locals) module.exports = content.locals;
// Hot Module Replacement
if(false) {
	// When the styles change, update the <style> tags
	if(!content.locals) {
		module.hot.accept("!!./../../../../../../coblan/webcode/node_modules/.0.26.1@css-loader/index.js!./../../../../../../coblan/webcode/node_modules/.6.0.0@sass-loader/lib/loader.js!./worktemplate.scss", function() {
			var newContent = require("!!./../../../../../../coblan/webcode/node_modules/.0.26.1@css-loader/index.js!./../../../../../../coblan/webcode/node_modules/.6.0.0@sass-loader/lib/loader.js!./worktemplate.scss");
			if(typeof newContent === 'string') newContent = [[module.id, newContent, '']];
			update(newContent);
		});
	}
	// When the module is disposed, remove the <style> tags
	module.hot.dispose(function() { update(); });
}

/***/ }),
/* 9 */
/***/ (function(module, exports, __webpack_require__) {

exports = module.exports = __webpack_require__(0)();
// imports


// module
exports.push([module.i, ".work-template-pan {\n  position: relative; }\n  .work-template-pan .item {\n    width: 7em;\n    height: 3em;\n    border: 1px solid #a8a8a8;\n    position: relative;\n    cursor: pointer; }\n  .work-template-pan .item:hover {\n    background-color: #fafff1; }\n  .work-template-pan .delete-btn {\n    position: absolute;\n    top: 0;\n    right: 0;\n    padding: 0.2em 0.4em;\n    border-radius: 2px;\n    color: red; }\n    .work-template-pan .delete-btn:hover {\n      background-color: #e8e8e8; }\n", ""]);

// exports


/***/ })
/******/ ]);