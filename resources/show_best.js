// Author: Areeb Beigh <areebbeigh@gmail.com>
// Not the best of scripts in JS but this gets the job done

var showBest = function(id) {
    var nodes = document.querySelectorAll(id);
    var valueNode = {};
    var nodeValues = [];
    for (var i = 0; i < nodes.length; i++) {
        var node = nodes[i];
        var value = node.textContent;
        valueNode[Number(value)] = node;
        nodeValues.push(Number(value))
    }
    if (id != "#wrong") {
        var greatestValue = 0;
        for (var i = 0; i < nodeValues.length; i++) {
            if (nodeValues[i] > greatestValue)
                greatestValue = nodeValues[i];
        }
        var res = valueNode[greatestValue];
    }
    else {
        // the best entry in wrong is the one that is the minimum
        var smallestValue = 9999999999999999;
        for (var i = 0; i < nodeValues.length; i++) {
            if (nodeValues[i] < smallestValue)
                smallestValue = nodeValues[i];
        }
        var res = valueNode[smallestValue];
    }
    res.style = "border: 2px solid red;"
};

var showBestAll = function() {
     showBest("#accuracy");
     showBest("#speed");
     showBest("#right");
     showBest("#wrong");
}