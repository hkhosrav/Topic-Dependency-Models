function updateGraph(e) {
    var query = Array.from(document.querySelectorAll(".item")).map(function (x) {
        var input = x.querySelector("input");
        var value = input.value;
        if (input.type == "checkbox") {
            value = input.checked ? "dynamic" : "static";
        }

        return x.getAttribute("data-name") + "=" + value;
    }).join("&");

    d3.json("//localhost:9000", function (response) {
        var target = document.getElementById("graphContainer");
        target.innerHTML = "";
        var height = document.getElementById("configurationContainer").getBoundingClientRect().height;
        target.style.height = height + "px";

        // Get all unique nodes
        var uniqueNodes = response
            .reduce(function (a, b) {
                return a.concat(b.data.nodes);
            }, [])
            .reduce(function (carry, node) {
                if (!carry.find(function (x) {
                        return x == node
                    })) {
                    carry.push(node);
                }
                return carry;
            }, [])
            .map(function (x) {
                return {
                    id: x
                }
            });

        var uniqueNodeHashMap = uniqueNodes.reduce(function (carry, x) {
            carry[x.id] = x;
            return carry;
        }, {});

        var notifyQueue = [];

        response.forEach(function (x, i) {
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
            var edges = data.edges.map(edge => ({
                target: uniqueNodeHashMap[edge[0]],
                source: uniqueNodeHashMap[edge[1]],
                attempts: edge[2],
                competency: edge[3]
            }));

            drawGraph(subGraph, edges, uniqueNodes, notifyQueue, i);
        });
    });
}

window.addEventListener("load", function () {
    Array.from(document.querySelectorAll(".input"))
        .forEach(elem => {
            var initialValue = Math.floor(Math.random() * 300);

            var input = document.createElement("input");
            input.type = "text";
            input.value = initialValue;

            var rangeInput = document.createElement("input");
            rangeInput.type = "range";
            rangeInput.min = "0";
            rangeInput.max = "300";
            rangeInput.value = initialValue

            var rangeContainer = document.createElement("div");
            rangeContainer.className = "rangeContainer";
            var lowerRange = document.createElement("span");
            lowerRange.innerText = "0";
            var upperRange = document.createElement("span");
            upperRange.innerText = "300";

            rangeContainer.appendChild(lowerRange);
            rangeContainer.appendChild(rangeInput);
            rangeContainer.appendChild(upperRange);
            elem.appendChild(rangeContainer);
            elem.appendChild(input);

            rangeInput.addEventListener("input", function (e) {
                input.value = e.target.value;
            });
            input.addEventListener("change", updateGraph);
            rangeInput.addEventListener("change", updateGraph);
        });

    document.getElementById("myonoffswitch").addEventListener("change", updateGraph)
    updateGraph();
});