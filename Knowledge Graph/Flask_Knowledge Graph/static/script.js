// initialize global variables.
var edges;
var nodes;
var network; 
var container;
var options, data;
let nodeFilterValue = "";

// parsing and collecting nodes and edges from the python
nodes = new vis.DataSet([{"id": "earphone", "label": "earphone", "shape": "dot", "size": 10, types_: "3C"}, 
{"id": "starbucks_flg", "label": "starbucks_flg", "shape": "dot", "size": 10}, 
{"id": "scooter_flg", "label": "scooter_flg", "shape": "dot", "size": 10}, 
{"id": "drink_flg", "label": "drink_flg", "shape": "dot", "size": 10}, 
{"id": "internet_flg", "label": "internet_flg", "shape": "dot", "size": 10}, 
{"id": "mouse", "label": "mouse", "shape": "dot", "size": 10, types_: "3C"}, 
{"id": "bikini", "label": "bikini", "shape": "dot", "size": 10, types_: "sports"}, 
{"id": "shopping_flg", "label": "shopping_flg", "shape": "dot", "size": 10}, 
{"id": "swimsuit", "label": "swimsuit", "shape": "dot", "size": 10, types_: "sports"}, 
{"id": "house_flg", "label": "house_flg", "shape": "dot", "size": 10}]);

edges = new vis.DataSet([{"arrows": "to", "from": "earphone", "title": "fashion-designed", "to": "starbucks_flg", "weight": 1}, 
{"arrows": "to", "from": "earphone", "title": "waterproof", "to": "scooter_flg", "weight": 1}, 
{"arrows": "to", "from": "earphone", "title": "3C", "to": "drink_flg", "weight": 1}, 
{"arrows": "to", "from": "earphone", "title": "fashion-designed", "to": "internet_flg", "weight": 1}, 
{"arrows": "to", "from": "mouse", "title": "FPS", "to": "starbucks_flg", "weight": 1}, 
{"arrows": "to", "from": "mouse", "title": "FPS", "to": "drink_flg", "weight": 1}, 
{"arrows": "to", "from": "bikini", "title": "fashion-designed", "to": "shopping_flg", "weight": 1}, 
{"arrows": "to", "from": "bikini", "title": "one-piece", "to": "starbucks_flg", "weight": 1}, 
{"arrows": "to", "from": "bikini", "title": "fashion-designed", "to": "internet_flg", "weight": 1}, 
{"arrows": "to", "from": "swimsuit", "title": "one-piece", "to": "house_flg", "weight": 1},
{"arrows": "to", "from": "swimsuit", "title": "one-piece", "to": "shopping_flg", "weight": 1}]);


// add nodeFilterSelector
const nodeFilterSelector = document.getElementById("nodeFilterSelect");

// This method is responsible for drawing the graph, returns the drawn network
function drawGraph(data) {
	var container = document.getElementById('mynetwork');

	// adding nodes and edges to the graph
	data = {nodes: nodes, edges: edges};

	var options = {
		"configure": {
			"enabled": true,
			"filter": [
				"physics"
			]
		},
		"edges": {
			"color": {
				"inherit": true
			},
			"smooth": {
				"enabled": false,
				"type": "continuous"
			}
		},
		"interaction": {
			"dragNodes": true,
			"hideEdgesOnDrag": false,
			"hideNodesOnDrag": false
		},
		"physics": {
			"enabled": true,
			"stabilization": {
				"enabled": true,
				"fit": true,
				"iterations": 1000,
				"onlyDynamicEdges": false,
				"updateInterval": 50
					}
				}
			}; // option ends


	// if this network requires displaying the configure window,
	// put it in its div
	options.configure["container"] = document.getElementById("config");
	
	network = new vis.Network(container, data, options);
	console.log(network)
	return network;
	
}

nodeFilterSelector.addEventListener("change", (e) => {
// set new value to filter variable
	nodeFilterValue = e.target.value;
	console.log("Event Change")
	/*
	refresh DataView,
	so that its filter function is re-calculated with the new variable
	*/
	nodesView.refresh();

});


const nodesFilter = (node) => {
	if (nodeFilterValue === "") {
		return true;
	}
	switch (nodeFilterValue) {
		case "3C":
			console.log("Change3c")
			return node.types_ === "3C";
		case "sports":
			console.log("ChangeSports")
			return node.types_ === "sports";
		default:
			console.log("First Time")
			return true;
	}
};

const nodesView = new vis.DataView(nodes, { filter: nodesFilter });

drawGraph({nodes: nodesView});


$("#mainSubmit").click(function(e){
  e.preventDefault();
  console.log("Submit")
  $.ajax({
    url: '/',
    type: 'post',
    data: $("#kg").serialize(),
    dataType: 'json',
    success:function(response){
      console.log("SUCCESS")
    }
  })
})