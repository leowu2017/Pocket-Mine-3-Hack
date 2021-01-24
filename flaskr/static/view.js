let width = parseInt(document.getElementById('width').textContent, 10)
let height = parseInt(document.getElementById('height').textContent, 10)
let blocks = document.getElementById('map-data').getElementsByTagName('img');

// alloc map (y, x)
let map = new Array(height);
for (let i = 0; i < height; ++i) {
	map[i] = new Array(width);
}
// init map
class Block {
	constructor(src) {
		this.src = src;
	}
}

for (let block of blocks) {
	let x = block.dataset.x;
	let y = block.dataset.y;
	map[y][x] = new Block(block.src);
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

var mapApp = new Vue({
	el: '#map',
	data: data,
});
