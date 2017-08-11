function drawGraph(target, edges, nodes, tick) {
    var bBox = target.getBoundingClientRect();
    var width = bBox.width;
    var height = bBox.height;

    var nodeRadius = 20;
    var graphWidth = width - (nodeRadius * 2);
    var graphHeight = height - (nodeRadius * 2);

    function ticked(link, node, labels, radius) {
        return function () {
            node
                .attr("cx", (d, i) => {
                    if (tick) {
                        d.x = Math.max(radius, Math.min(graphWidth - radius, d.x));
                        return d.x;
                    }
                    return nodes[i].x;
                })
                .attr("cy", (d, i) => {
                    if (tick) {
                        d.y = Math.max(radius, Math.min(graphHeight - radius, d.y));
                        return d.y;
                    }
                    return nodes[i].y;
                });

            link
                .attr("x1", d => d.source.x)
                .attr("y1", d => d.source.y)
                .attr("x2", d => d.target.x)
                .attr("y2", d => d.target.y);

            labels
                .attr("dx", d => d.x)
                .attr("dy", d => d.y + 4);
        };
    };


    var selfLoops = edges.filter(x => x.source == x.target);
    var minRange = 2;
    var maxRange = 10;
    var normalise = (min, max, v) => {
        return (maxRange - minRange) * ((v - min) / (max - min)) + minRange;
    };

    var maxWeight = d3.max(edges.map(x => x.attempts));
    var minWeight = d3.min(edges.map(x => x.attempts));
    var lineColour = d3.interpolate("pink", "#256");
    var maxColour = d3.max(edges.map(x => x.competency));
    var minColour = d3.min(edges.map(x => x.competency));
    var getStrokeColour = d => lineColour((d.competency - maxColour) / (minColour - maxColour));

    var svg = d3.select(target)
        .html(null)
        .append("svg")
        .attr("width", width)
        .attr("height", height);

    var container = svg
        .append("g")
        .attr("class", "container")
        .attr("transform", `translate(${nodeRadius},${nodeRadius})`);

    var forceLink = d3.forceLink(edges);
    var simulation = d3.forceSimulation(nodes)
        .force("collision", d3.forceCollide(3 * nodeRadius))
        .force("link", forceLink.distance(3 * nodeRadius))
        .force("body", d3.forceManyBody().distanceMin(nodeRadius))
        .force("center", d3.forceCenter(graphWidth / 2, graphHeight / 2));

    var link = container.append("g")
        .attr("class", "links")
        .selectAll("line")
        .data(edges)
        .enter()
        .append("line")
        .attr("stroke", getStrokeColour)
        .attr("stroke-width", d => normalise(minWeight, maxWeight, d.attempts));
    var node = container.append("g")
        .attr("class", "nodes")
        .selectAll("circle")
        .data(nodes)
        .enter().append("circle")
        .attr("r", nodeRadius)
        .attr("stroke", d => {
            var foundSelfLoop = selfLoops.find(selfLoop => selfLoop.source == d);
            if (foundSelfLoop) {
                return getStrokeColour(foundSelfLoop);
            }
            return "#444";
        })
        .attr("stroke-width", d => {
            var foundSelfLoop = selfLoops.find(selfLoop => selfLoop.source == d);
            if (foundSelfLoop) {
                return normalise(minWeight, maxWeight, foundSelfLoop.attempts);
            }
            return 1;
        })
        .attr("fill", "#fff");
    var labels = container.append("g")
        .attr("class", "labels")
        .selectAll("text")
        .data(nodes)
        .enter().append("text")
        .attr("dx", d => d.cx)
        .attr("dy", d => d.cy)
        .attr("text-anchor", "middle")
        .text(d => d.id);

    simulation
        .on("tick", ticked(link, node, labels, nodeRadius));
}