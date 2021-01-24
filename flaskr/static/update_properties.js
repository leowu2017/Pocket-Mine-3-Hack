var title = document.getElementById("title").value;
var width = document.getElementById("width").value;
var height = document.getElementById("height").value;

var data = {
	title: title,
	width: width,
	height: height,
};

var appHeader = new Vue({
	el: '#header',
	data: data,
});

var appForm = new Vue({
	el: '#form',
	data: data,
});

appForm.$watch('title', function(newVal, _oldVal) {
	document.title = newVal;
});