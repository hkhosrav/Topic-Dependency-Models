function updateGraph(e) {
    e.preventDefault();

    var query = Array.from(document.querySelectorAll(".item")).map(function(x) {
        var input = x.querySelector("input");
        var value = input.value;
        if (input.type == "checkbox") {
            value = input.checked ? "dynamic" : "static";
        }

        return x.getAttribute("data-name") + "=" + value;
    }).join("&");

    d3.json("http://localhost:9000", function(response) {
        var target = document.getElementById("graphContainer");
        target.innerHTML = "";
        var height = document.getElementById("configurationContainer").getBoundingClientRect().height;
        target.style.height = height + "px";

        // Get all unique nodes
        var uniqueNodes = response
            .reduce(function(a, b) {
                return a.concat(b.data.nodes);
            }, [])
            .reduce(function(carry, node) {
                if (!carry.find(function(x) {
                    return x == node
                })) {
                    carry.push(node);
                }
                return carry;
            }, [])
            .map(function(x) {
                return {
                    id: x
                }
            });

        var uniqueNodeHashMap = uniqueNodes.reduce(function(carry, x) {
            carry[x.id] = x;
            return carry;
        }, {});

        var notifyQueue = [];

        response.forEach(function(x, i) {
            var data = x.data;
            var subGraph = document.createElement("div");

            var subGraphTitle = document.createElement("h2");
            subGraphTitle.className = "subGraphTitle";
            subGraphTitle.innerText = x.name;
            subGraph.appendChild(subGraphTitle);

            var width = document.getElementById("graphContainer").getBoundingClientRect().width / 2;
            subGraph.style.width = width + "px";
            subGraph.style.height = height + "px";
            target.appendChild(subGraph);
            var edges = data.edges.map(function(edge) {
                return {
                    target: uniqueNodeHashMap[edge[0]],
                    source: uniqueNodeHashMap[edge[1]],
                    attempts: edge[2],
                    competency: edge[3]
                };
            });

            drawGraph(subGraph, edges, uniqueNodes, notifyQueue, i);
        });
    });
}

window.addEventListener("load", function() {
    Array.from(document.querySelectorAll(".input"))
        .forEach(function(elem) {
            var min = +elem.getAttribute("data-min") || 0;
            var max = +elem.getAttribute("data-max") || 100;
            var step = +elem.getAttribute("data-step") || (max - min) / 100;

            var initialValue = Math.floor(Math.random() * (max - min)) + min;

            var input = document.createElement("input");
            input.type = "text";
            input.value = initialValue;


            var rangeInput = document.createElement("input");
            rangeInput.type = "range";
            rangeInput.min = min;
            rangeInput.max = max;
            rangeInput.step = step;
            rangeInput.value = initialValue

            var rangeContainer = document.createElement("div");
            rangeContainer.className = "rangeContainer";
            var lowerRange = document.createElement("span");
            lowerRange.innerText = min;
            var upperRange = document.createElement("span");
            upperRange.innerText = max;

            rangeContainer.appendChild(lowerRange);
            rangeContainer.appendChild(rangeInput);
            rangeContainer.appendChild(upperRange);
            elem.appendChild(rangeContainer);
            elem.appendChild(input);

            input.addEventListener("input", function(e) {
                e.preventDefault();
                var val = +e.target.value;
                if (isNaN(val)) {
                    e.target.value = min;
                } else if (val < min) {
                    e.target.value = min;
                } else if (val > max) {
                    e.target.value = max;
                }
                rangeInput.value = e.target.value;
            });

            rangeInput.addEventListener("input", function(e) {
                input.value = e.target.value;
            });
        });

    document.getElementById("simulateButton").addEventListener("click", updateGraph);
});