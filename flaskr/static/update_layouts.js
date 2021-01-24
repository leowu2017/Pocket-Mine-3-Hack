let width = parseInt(document.getElementById('width').textContent, 10)
let height = parseInt(document.getElementById('height').textContent, 10)
let blocks = document.getElementById('map-data').getElementsByTagName('img');
let csrf_token = document.getElementById('block').dataset.csrf;
let lastHtmlTarget;
let target;

$.ajaxSetup({
	beforeSend: function(xhr, settings) {
		if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
			xhr.setRequestHeader("X-CSRFToken", csrf_token);
		}
	}
});

// alloc map
let map = new Array(height);
for (let i = 0; i < height; ++i) {
	map[i] = new Array(width);
}
// init map
class Block {
	constructor(id, src) {
		this.id = id;
		this.src = src;
	}
}

for (let block of blocks) {
	let x = block.dataset.x;
	let y = block.dataset.y;
	let id = block.dataset.id;
	map[y][x] = new Block(id, block.src);
}

// component
Vue.component('rowinfo', {
	template: `<div>
			<picture v-if='shouldAppend' :data-after-content='appendContent'>
				<slot/>
			</picture>
			<template v-else>
				<slot/>
			</template>
		</div>`,
	props: ['row', 'column'],
	computed: {
		shouldAppend: function() {
			return ((this.column + 1) == width) & ((this.row + 1) % 5 == 0);
		},
		appendContent: function() {
			return (this.row + 1) + '/' + height
		},
	},
});

// data
var data = {
	map: map,
};

class ExistingBlock {
	constructor(id) {
		this.id = id;
	}
}

class NewBlock {
	constructor(x, y) {
		this.x = x;
		this.y = y;
	}
}

var mapApp = new Vue({
	el: '#map',
	data: data,
	methods: {
		setTargetBlock: function(event) {
			if (lastHtmlTarget) {
				lastHtmlTarget.classList.remove('selected');
			}
			let img = event.target;
			if (img.dataset.id === undefined) {
				target = new NewBlock(img.dataset.x, img.dataset.y);
			} else {
				target = new ExistingBlock(img.dataset.id);
			}
			img.classList.add('selected');
			lastHtmlTarget = img;
		}
	}
});

var blockApp = new Vue({
	el: '#block',
	data: data,
	methods: {
		selectBlock: function(event) {
			if (target) {
				let id = event.target.dataset.id;
				let ajaxData;
				if (target instanceof NewBlock) {
					ajaxData = {
						x: target.x,
						y: target.y,
						block_id: id,
					};
				} else if (target instanceof ExistingBlock) {
					ajaxData = {
						id: target.id,
						block_id: id,
					};
				}
				$.ajax({
					method: "POST",
					contentType: "application/json",
					data: JSON.stringify(ajaxData),
				}).done(function(msg) {
					if(msg.result == 'error'){
						console.log(msg.err);
					}
				});
				if (lastHtmlTarget) {
					lastHtmlTarget.src = event.target.src;
				}
			}
		}
	}
})
