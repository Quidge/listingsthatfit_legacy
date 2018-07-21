// console.log(steps.length);
console.log('test');

// Pass through wizard stuff
var steps = $("#measurementsForm section");
console.log(steps);
count = steps.length

$("#submitFinal").hide();
$("#measurementsForm").before("<ul class='nav' id='steps'></ul>");

steps.each(function(i) {
	// var name = $(this).find("legend").html();
	var name = $(this).attr('name');
	$("#steps").append("<li class='nav-item' id='stepDesc" + i + "'> Step " + (i + 1) + " <span>" + name + "</span></li>");
	// $(this).wrap("<div id='step" + i + "'></div>");
	$(this).attr('id', 'step' + i);
	$('.section_content', this).append('<div class="row"><div class="col"><p id="step' + i + 'commands"></p></div></div>');
	createDevButton(i);
	if (i == 0) {
		createNextButton(i); // to do
		selectStep(i);
	}
	else if (i == count - 1) {
		$("#step" + i).hide();
		createPrevButton(i); // to do
	}
	else {
		$("#step" + i).hide();
		createPrevButton(i);
		createNextButton(i);
	}
	thisFieldNextButton = $("#step" + i + "Next");
	thisFieldInputs = $("#step" + i + " input");
	// console.log(thisFieldInputs.show())
	thisFieldInputs.each(function() {
		// $(this).change(function() {checkInputsAndModifyButton(thisFieldInputs, thisFieldNextButton)});
		$(this).change(function() {
			allFilled = true;
			$("#step" + i + " input").each(function() {
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
	inputsToCheck.each(function() {
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
	
	$("#" + stepName + "commands")
		.append("<button type='button' id='" + stepName + "Populate' class='btn btn-info'>DevPopulate</button>");
	
	$("#" + stepName + "Populate").bind("click", function(e) {
		updateSummaryPage();
		$("#" + stepName + " input").each(function() {
			// console.log($(this));
			$(this).val(22);
			$(this).change();
		});
	});
}

function createPrevButton(i) {
	
	var stepName = "step" + i;
	
	$("#" + stepName + "commands").append("<button type='button' id='" + stepName + "Prev' class='prev btn btn-primary'>< Back</>");
	
	$("#" + stepName + "Prev").bind("click", function(e) {
		$("#" + stepName).hide();
		$("#step" + (i - 1)).show();
		selectStep(i - 1);
	})
}

function createNextButton(i) {
	var stepName = "step" + i;
	$("#" + stepName + "commands").append("<button type='button' id='" + stepName + "Next' class='next disabled btn btn-primary' disabled>Next ></>");
	// console.log(document.querySelectorAll("#" + stepName + " input[required]"))
	$("#" + stepName + "Next").bind("click", function(e) {
		// if ($("#step" + i + " input[required]").every(function(input) {if(input.val() == "") {return input}})) {
			// console.log('you fucked up')
		// }
		$("#" + stepName).hide();
		$("#step" + (i + 1)).show();
		selectStep(i + 1);
	})
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
	}
}

function updateSummaryPage() {
	$(".summary.clothing-category-row").each(function() {
		summaryCategoryDiv = $(this).children().first().next();
		stupidMaster = summaryCategoryDiv.data('stupid_master');
		clothingType = summaryCategoryDiv.data('clothing_type');
		$('div.measurement-info', summaryCategoryDiv).each(function() {
			measurementType = $(this).data('measurement_type');
			idStringPartial = [stupidMaster, clothingType, measurementType].join('-');
			// idStringMeasurement = idStringPartial + "-measurement";
			// idStringTolerance = idStringTolerance + "-tolerance"
			msmt_val = +$("#" + idStringPartial + "-measurement").val()
			tolerance_val = +$("#" + idStringPartial + "-tolerance").val()
			// console.log(idStringPartial, typeof(msmt_val), tolerance_val);
			$('span.measurement-type', $(this)).text(measurementType);
			$('span.measurement-value[data-measurement_value_type="start"]', $(this)).text((msmt_val-tolerance_val)+'"');
			$('span.measurement-value[data-measurement_value_type="end"]', $(this)).text((msmt_val+tolerance_val)+'"');
		});
	});
}

function updateSummaryRow(directorDict, measurement_val, tolerance_val) {
	d = directorDict
	// get the right row
	string = 'div[data-stupid_master="'
		+ d["stupid_master"]
		+ '"][data-clothing_type="'
		+ d["clothing_type"]
		+ '"]'
		+ ' div[data-measurement_type="'
		+ d["measurement_type"]
		+ '"]';
	
	rowDiv = $(string)
	
	// set measurement type
	$("span.measurement-type", rowDiv).text(d["measurement_type"]);

	//set start and end values
	startVal = measurement_val - tolerance_val
	endVal = measurement_val + tolerance_val
	$('span[data-measurement_value_type="start"].measurement-value', rowDiv).text(startVal + '"');
	$('span[data-measurement_value_type="end"].measurement-value', rowDiv).text(endVal + '"');
	
	// console.log(row.show());
}


function roundToEigth(numeric_value) {
	return Math.floor(numeric_value / .125) * .125
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