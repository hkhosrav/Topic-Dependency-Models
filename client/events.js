function generateMockData() {
    function randInt(r) {
        return Math.floor(Math.random() * r);
    }
    var nodes = new Array(10).fill(0).map(x => String.fromCharCode(65 + randInt(6)));
    edges = [];

    nodes.forEach(x => {
        edges.push([
            x,
            x,
            randInt(100),
            randInt(100)
        ]);
        var randomNode = nodes[randInt(nodes.length)];
        if (randomNode == x) return;
        edges.push([
            x,
            randomNode,
            randInt(100),
            randInt(100)
        ]);
    });

    return {
        nodes: nodes,
        edges: edges
    };
}

function updateGraph(e) {
    var query = Array.from(document.querySelectorAll(".item")).map(x => {
        var input = x.querySelector("input");
        var value = input.value;
        if (input.type == "checkbox") {
            value = input.checked ? "dynamic" : "static";
        }

        return x.getAttribute("data-name") + "=" + value;
    }).join("&");

    // Mock query response ...
    var response = [generateMockData(), generateMockData()];

    var target = document.getElementById("graphContainer");
    target.innerHTML = "";
    var height = document.getElementById("configurationContainer").getBoundingClientRect().height;

    target.style.height = height + "px";

    var uniqueNodes = response
        .reduce((a, b) => a.nodes.concat(b.nodes))
        .reduce((carry, node) => {
            if (!carry.find(x => x == node)) {
                carry.push(node);
            }
            return carry;
        }, [])
        .map(x => ({
            id: x
        }));


    response.forEach((x, i) => {
        var subGraph = document.createElement("div");
        var width = document.getElementById("graphContainer").getBoundingClientRect().width / response.length;
        subGraph.style.width = width + "px";
        subGraph.style.height = height + "px";
        target.appendChild(subGraph);
        var edges = x.edges.map(edge => ({
            target: uniqueNodes.find(x => x.id == edge[0]),
            source: uniqueNodes.find(x => x.id == edge[1]),
            attempts: edge[2],
            competency: edge[3]
        }));
        drawGraph(subGraph, edges, uniqueNodes, i == 0);
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