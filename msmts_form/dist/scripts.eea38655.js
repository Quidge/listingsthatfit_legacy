// modules are defined as an array
// [ module function, map of requires ]
//
// map of requires is short require name -> numeric require
//
// anything defined in a previous bundle is accessed via the
// orig method which is the require for previous bundles

// eslint-disable-next-line no-global-assign
parcelRequire = (function (modules, cache, entry, globalName) {
  // Save the require from previous bundle to this closure if any
  var previousRequire = typeof parcelRequire === 'function' && parcelRequire;
  var nodeRequire = typeof require === 'function' && require;

  function newRequire(name, jumped) {
    if (!cache[name]) {
      if (!modules[name]) {
        // if we cannot find the module within our internal map or
        // cache jump to the current global require ie. the last bundle
        // that was added to the page.
        var currentRequire = typeof parcelRequire === 'function' && parcelRequire;
        if (!jumped && currentRequire) {
          return currentRequire(name, true);
        }

        // If there are other bundles on this page the require from the
        // previous one is saved to 'previousRequire'. Repeat this as
        // many times as there are bundles until the module is found or
        // we exhaust the require chain.
        if (previousRequire) {
          return previousRequire(name, true);
        }

        // Try the node require function if it exists.
        if (nodeRequire && typeof name === 'string') {
          return nodeRequire(name);
        }

        var err = new Error('Cannot find module \'' + name + '\'');
        err.code = 'MODULE_NOT_FOUND';
        throw err;
      }

      localRequire.resolve = resolve;

      var module = cache[name] = new newRequire.Module(name);

      modules[name][0].call(module.exports, localRequire, module, module.exports, this);
    }

    return cache[name].exports;

    function localRequire(x){
      return newRequire(localRequire.resolve(x));
    }

    function resolve(x){
      return modules[name][1][x] || x;
    }
  }

  function Module(moduleName) {
    this.id = moduleName;
    this.bundle = newRequire;
    this.exports = {};
  }

  newRequire.isParcelRequire = true;
  newRequire.Module = Module;
  newRequire.modules = modules;
  newRequire.cache = cache;
  newRequire.parent = previousRequire;
  newRequire.register = function (id, exports) {
    modules[id] = [function (require, module) {
      module.exports = exports;
    }, {}];
  };

  for (var i = 0; i < entry.length; i++) {
    newRequire(entry[i]);
  }

  if (entry.length) {
    // Expose entry point to Node, AMD or browser globals
    // Based on https://github.com/ForbesLindesay/umd/blob/master/template.js
    var mainExports = newRequire(entry[entry.length - 1]);

    // CommonJS
    if (typeof exports === "object" && typeof module !== "undefined") {
      module.exports = mainExports;

    // RequireJS
    } else if (typeof define === "function" && define.amd) {
     define(function () {
       return mainExports;
     });

    // <script>
    } else if (globalName) {
      this[globalName] = mainExports;
    }
  }

  // Override the current require with this new one
  return newRequire;
})({"scripts/index.js":[function(require,module,exports) {
// console.log(steps.length);
console.log('test');

// Pass through wizard stuff
var steps = $("#measurementsForm section");
console.log(steps);
count = steps.length;

$("#submitFinal").hide();
$("#measurementsForm").before("<ul id='steps'></ul>");

steps.each(function (i) {
	// var name = $(this).find("legend").html();
	var name = $(this).find("legend").html();
	$("#steps").append("<li id='stepDesc" + i + "'> Step " + (i + 1) + " <span>" + name + "</span></li>");
	$(this).wrap("<div id='step" + i + "'></div>");
	$(this).append("<p id='step" + i + "commands'></p>");
	createDevButton(i);
	if (i == 0) {
		createNextButton(i); // to do
		selectStep(i);
	} else if (i == count - 1) {
		$("#step" + i).hide();
		createPrevButton(i); // to do
	} else {
		$("#step" + i).hide();
		createPrevButton(i);
		createNextButton(i);
	}
	thisFieldNextButton = $("#step" + i + "Next");
	thisFieldInputs = $("#step" + i + " input");
	// console.log(thisFieldInputs.show())
	thisFieldInputs.each(function () {
		// $(this).change(function() {checkInputsAndModifyButton(thisFieldInputs, thisFieldNextButton)});
		$(this).change(function () {
			allFilled = true;
			$("#step" + i + " input").each(function () {
				if ($(this).val() == "") {
					bttn = $("#step" + i + "Next");
					bttn.prop('disabled', true);
					bttn.addClass("disabled");
					allFilled = false;
					return false;
				}
			});
			if (allFilled) {
				bttn = $("#step" + i + "Next");
				bttn.prop('disabled', false);
				bttn.removeClass("disabled");
			}
			// console.log(allFilled)
		});
	});
});

function checkInputsAndModifyButton(inputsToCheck, buttonToModify) {
	// console.log(inputsToCheck.show());
	allFilled = true;
	inputsToCheck.each(function () {
		if ($(this).val() == "") {
			// console.log($(this));
			buttonToModify.prop('disabled', true);
			buttonToModify.addClass("disabled");
			allFilled = false;
		}
	});
	// console.log('got here')
	if (allFilled) {
		buttonToModify.prop('disabled', false);
		buttonToModify.removeClass("disabled");
	}
	return allFilled;
}

function createDevButton(i) {
	var stepName = "step" + i;

	$("#" + stepName + "commands").append("<button type='button' id='" + stepName + "Populate' class='btn btn-info'>DevPopulate</button>");

	$("#" + stepName + "Populate").bind("click", function (e) {
		updateSummaryPage();
		$("#" + stepName + " input").each(function () {
			// console.log($(this));
			$(this).val(22);
			$(this).change();
		});
	});
}

function createPrevButton(i) {

	var stepName = "step" + i;

	$("#" + stepName + "commands").append("<button type='button' id='" + stepName + "Prev' class='prev btn btn-primary'>< Back</>");

	$("#" + stepName + "Prev").bind("click", function (e) {
		$("#" + stepName).hide();
		$("#step" + (i - 1)).show();
		selectStep(i - 1);
	});
}

function createNextButton(i) {
	var stepName = "step" + i;
	$("#" + stepName + "commands").append("<button type='button' id='" + stepName + "Next' class='next disabled btn btn-primary' disabled>Next ></>");
	// console.log(document.querySelectorAll("#" + stepName + " input[required]"))
	$("#" + stepName + "Next").bind("click", function (e) {
		// if ($("#step" + i + " input[required]").every(function(input) {if(input.val() == "") {return input}})) {
		// console.log('you fucked up')
		// }
		$("#" + stepName).hide();
		$("#step" + (i + 1)).show();
		selectStep(i + 1);
	});
}

function selectStep(i) {
	$("#steps li").removeClass("current");
	$("#stepDesc" + i).addClass("current");
}

// Extrapolate values stuff

$("#whatthefuck").click(extrapolateAll);
// console.log($("#whatthefuck"));

function extrapolateAll() {
	oie = overwriteIfEmpty;

	// Sportcoat msmts

	oie($("#sportcoat-jacket-chest_flat-measurement"), +$("#suit-jacket-chest_flat-measurement").val());
	oie($("#sportcoat-jacket-chest_flat-tolerance"), +$("#suit-jacket-chest_flat-tolerance").val());

	oie($("#sportcoat-jacket-shoulders-tolerance"), +$("#suit-jacket-shoulders-tolerance").val());
	oie($("#sportcoat-jacket-shoulders-measurement"), +$("#suit-jacket-shoulders-measurement").val());

	oie($("#sportcoat-jacket-sleeve-measurement"), +$("#suit-jacket-sleeve-measurement").val());
	oie($("#sportcoat-jacket-sleeve-tolerance"), +$("#suit-jacket-sleeve-tolerance").val());

	oie($("#sportcoat-jacket-waist_flat-measurement"), +$("#suit-jacket-waist_flat-measurement").val());
	oie($("#sportcoat-jacket-waist_flat-tolerance"), +$("#suit-jacket-waist_flat-tolerance").val());

	oie($("#sportcoat-jacket-length-measurement"), +$("#suit-jacket-length-measurement").val());
	oie($("#sportcoat-jacket-length-tolerance"), +$("#suit-jacket-length-tolerance").val());

	// Coats and jackets msmts

	oie($("#coats_and_jackets-jacket-chest_flat-measurement"), +$("#suit-jacket-chest_flat-measurement").val() + .5);
	oie($("#coats_and_jackets-jacket-chest_flat-tolerance"), +$("#suit-jacket-chest_flat-tolerance").val() * 1.2);

	oie($("#coats_and_jackets-jacket-shoulders-measurement"), +$("#suit-jacket-shoulders-measurement").val() + .25);
	oie($("#coats_and_jackets-jacket-shoulders-tolerance"), +$("#suit-jacket-shoulders-tolerance").val() * 1.2);

	oie($("#coats_and_jackets-jacket-sleeve-measurement"), +$("#suit-jacket-sleeve-measurement").val());
	oie($("#coats_and_jackets-jacket-sleeve-tolerance"), 3);

	// Casual shirt msmts

	oie($("#casual_shirt-shirt-chest_flat-measurement"), +$("#dress_shirt-shirt-chest_flat-measurement").val());
	oie($("#casual_shirt-shirt-chest_flat-tolerance"), +$("#dress_shirt-shirt-chest_flat-tolerance").val() * 1.3);

	oie($("#casual_shirt-shirt-sleeve-measurement"), +$("#dress_shirt-shirt-sleeve-measurement").val());
	oie($("#casual_shirt-shirt-sleeve-tolerance"), +$("#dress_shirt-shirt-sleeve-tolerance").val() * 1.3);

	oie($("#casual_shirt-shirt-shoulders-measurement"), +$("#dress_shirt-shirt-shoulders-measurement").val());
	oie($("#casual_shirt-shirt-shoulders-tolerance"), +$("#dress_shirt-shirt-shoulders-tolerance").val() * 1.3);

	// Pant msmts

	oie($("#pant-pant-waist_flat-measurement"), +$("#suit-pant-waist_flat-measurement").val());
	oie($("#pant-pant-waist_flat-tolerance"), +$("#suit-pant-waist_flat-tolerance").val());

	oie($("#pant-pant-hips_flat-measurement"), +$("#suit-pant-hips_flat-measurement").val());
	oie($("#pant-pant-hips_flat-tolerance"), +$("#suit-pant-hips_flat-tolerance").val());

	oie($("#pant-pant-inseam-measurement"), +$("#suit-pant-inseam-measurement").val());
	oie($("#pant-pant-inseam-tolerance"), +$("#suit-pant-inseam-tolerance").val());

	oie($("#pant-pant-rise-measurement"), +$("#suit-pant-rise-measurement").val());
	oie($("#pant-pant-rise-tolerance"), +$("#suit-pant-rise-tolerance").val());

	oie($("#pant-pant-cuff_width-measurement"), +$("#suit-pant-cuff_width-measurement").val());
	oie($("#pant-pant-cuff_width-tolerance"), +$("#suit-pant-cuff_width-tolerance").val());

	// Sweater msmts

	oie($("#sweater-sweater-chest_flat-measurement"), +$("#dress_shirt-shirt-chest_flat-measurement").val());
	oie($("#sweater-sweater-chest_flat-tolerance"), +$("#dress_shirt-shirt-chest_flat-tolerance").val() * 1.5);

	oie($("#sweater-sweater-sleeve-measurement"), +$("#dress_shirt-shirt-sleeve-measurement").val() + .5);
	oie($("#sweater-sweater-sleeve-tolerance"), +$("#dress_shirt-shirt-sleeve-tolerance").val() * 1.5);

	oie($("#sweater-sweater-shoulders-measurement"), +$("#dress_shirt-shirt-shoulders-measurement").val());
	oie($("#sweater-sweater-shoulders-tolerance"), +$("#dress_shirt-shirt-shoulders-tolerance").val() * 1.5);

	// oie($("#sweater-sweater-length-measurement"), $("#suit-jacket-length-measurement").val() - 1);
	// oie($("#sweater-sweater-length-tolerance"), ($("#suit-jacket-length-tolerance").val() * 1.5);

	// updateSummaryOutput(parseIdToData('sweater-sweater-shoulders'), 220000, 5000)

	// console.log('extrapolated!')
}

// console.log(updateSummaryOutput(parseIdToData('sweater-sweater-shoulders'), 0, 0));

function parseIdToData(stringName) {
	dataArray = stringName.split("-");
	return {
		"stupid_master": dataArray[0],
		"clothing_type": dataArray[1],
		"measurement_type": dataArray[2]
	};
}

function updateSummaryPage() {
	$(".summary.clothing-category-row").each(function () {
		summaryCategoryDiv = $(this).children().first().next();
		stupidMaster = summaryCategoryDiv.data('stupid_master');
		clothingType = summaryCategoryDiv.data('clothing_type');
		$('div.measurement-info', summaryCategoryDiv).each(function () {
			measurementType = $(this).data('measurement_type');
			idStringPartial = [stupidMaster, clothingType, measurementType].join('-');
			// idStringMeasurement = idStringPartial + "-measurement";
			// idStringTolerance = idStringTolerance + "-tolerance"
			msmt_val = +$("#" + idStringPartial + "-measurement").val();
			tolerance_val = +$("#" + idStringPartial + "-tolerance").val();
			// console.log(idStringPartial, typeof(msmt_val), tolerance_val);
			$('span.measurement-type', $(this)).text(measurementType);
			$('span.measurement-value[data-measurement_value_type="start"]', $(this)).text(msmt_val - tolerance_val + '"');
			$('span.measurement-value[data-measurement_value_type="end"]', $(this)).text(msmt_val + tolerance_val + '"');
		});
	});
}

function updateSummaryRow(directorDict, measurement_val, tolerance_val) {
	d = directorDict;
	// get the right row
	string = 'div[data-stupid_master="' + d["stupid_master"] + '"][data-clothing_type="' + d["clothing_type"] + '"]' + ' div[data-measurement_type="' + d["measurement_type"] + '"]';

	rowDiv = $(string);

	// set measurement type
	$("span.measurement-type", rowDiv).text(d["measurement_type"]);

	//set start and end values
	startVal = measurement_val - tolerance_val;
	endVal = measurement_val + tolerance_val;
	$('span[data-measurement_value_type="start"].measurement-value', rowDiv).text(startVal + '"');
	$('span[data-measurement_value_type="end"].measurement-value', rowDiv).text(endVal + '"');

	// console.log(row.show());
}

function roundToEigth(numeric_value) {
	return Math.floor(numeric_value / .125) * .125;
}

// function allInputsHaveValues(inputs_array) {
// return inputs_array.every(input) {input.value != ""}
// 

function overwriteIfEmpty(targetElement, value) {
	if (targetElement.val() == "") {
		targetElement.val(roundToEigth(value));
		targetElement.change();
	}
}
},{}],"../../../../../../../usr/local/lib/node_modules/parcel-bundler/src/builtins/hmr-runtime.js":[function(require,module,exports) {
var global = arguments[3];
var OVERLAY_ID = '__parcel__error__overlay__';

var OldModule = module.bundle.Module;

function Module(moduleName) {
  OldModule.call(this, moduleName);
  this.hot = {
    data: module.bundle.hotData,
    _acceptCallbacks: [],
    _disposeCallbacks: [],
    accept: function (fn) {
      this._acceptCallbacks.push(fn || function () {});
    },
    dispose: function (fn) {
      this._disposeCallbacks.push(fn);
    }
  };

  module.bundle.hotData = null;
}

module.bundle.Module = Module;

var parent = module.bundle.parent;
if ((!parent || !parent.isParcelRequire) && typeof WebSocket !== 'undefined') {
  var hostname = '' || location.hostname;
  var protocol = location.protocol === 'https:' ? 'wss' : 'ws';
  var ws = new WebSocket(protocol + '://' + hostname + ':' + '57617' + '/');
  ws.onmessage = function (event) {
    var data = JSON.parse(event.data);

    if (data.type === 'update') {
      console.clear();

      data.assets.forEach(function (asset) {
        hmrApply(global.parcelRequire, asset);
      });

      data.assets.forEach(function (asset) {
        if (!asset.isNew) {
          hmrAccept(global.parcelRequire, asset.id);
        }
      });
    }

    if (data.type === 'reload') {
      ws.close();
      ws.onclose = function () {
        location.reload();
      };
    }

    if (data.type === 'error-resolved') {
      console.log('[parcel] ✨ Error resolved');

      removeErrorOverlay();
    }

    if (data.type === 'error') {
      console.error('[parcel] 🚨  ' + data.error.message + '\n' + data.error.stack);

      removeErrorOverlay();

      var overlay = createErrorOverlay(data);
      document.body.appendChild(overlay);
    }
  };
}

function removeErrorOverlay() {
  var overlay = document.getElementById(OVERLAY_ID);
  if (overlay) {
    overlay.remove();
  }
}

function createErrorOverlay(data) {
  var overlay = document.createElement('div');
  overlay.id = OVERLAY_ID;

  // html encode message and stack trace
  var message = document.createElement('div');
  var stackTrace = document.createElement('pre');
  message.innerText = data.error.message;
  stackTrace.innerText = data.error.stack;

  overlay.innerHTML = '<div style="background: black; font-size: 16px; color: white; position: fixed; height: 100%; width: 100%; top: 0px; left: 0px; padding: 30px; opacity: 0.85; font-family: Menlo, Consolas, monospace; z-index: 9999;">' + '<span style="background: red; padding: 2px 4px; border-radius: 2px;">ERROR</span>' + '<span style="top: 2px; margin-left: 5px; position: relative;">🚨</span>' + '<div style="font-size: 18px; font-weight: bold; margin-top: 20px;">' + message.innerHTML + '</div>' + '<pre>' + stackTrace.innerHTML + '</pre>' + '</div>';

  return overlay;
}

function getParents(bundle, id) {
  var modules = bundle.modules;
  if (!modules) {
    return [];
  }

  var parents = [];
  var k, d, dep;

  for (k in modules) {
    for (d in modules[k][1]) {
      dep = modules[k][1][d];
      if (dep === id || Array.isArray(dep) && dep[dep.length - 1] === id) {
        parents.push(k);
      }
    }
  }

  if (bundle.parent) {
    parents = parents.concat(getParents(bundle.parent, id));
  }

  return parents;
}

function hmrApply(bundle, asset) {
  var modules = bundle.modules;
  if (!modules) {
    return;
  }

  if (modules[asset.id] || !bundle.parent) {
    var fn = new Function('require', 'module', 'exports', asset.generated.js);
    asset.isNew = !modules[asset.id];
    modules[asset.id] = [fn, asset.deps];
  } else if (bundle.parent) {
    hmrApply(bundle.parent, asset);
  }
}

function hmrAccept(bundle, id) {
  var modules = bundle.modules;
  if (!modules) {
    return;
  }

  if (!modules[id] && bundle.parent) {
    return hmrAccept(bundle.parent, id);
  }

  var cached = bundle.cache[id];
  bundle.hotData = {};
  if (cached) {
    cached.hot.data = bundle.hotData;
  }

  if (cached && cached.hot && cached.hot._disposeCallbacks.length) {
    cached.hot._disposeCallbacks.forEach(function (cb) {
      cb(bundle.hotData);
    });
  }

  delete bundle.cache[id];
  bundle(id);

  cached = bundle.cache[id];
  if (cached && cached.hot && cached.hot._acceptCallbacks.length) {
    cached.hot._acceptCallbacks.forEach(function (cb) {
      cb();
    });
    return true;
  }

  return getParents(global.parcelRequire, id).some(function (id) {
    return hmrAccept(global.parcelRequire, id);
  });
}
},{}]},{},["../../../../../../../usr/local/lib/node_modules/parcel-bundler/src/builtins/hmr-runtime.js","scripts/index.js"], null)
//# sourceMappingURL=/scripts.eea38655.map