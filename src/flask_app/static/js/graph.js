$(function(){
    var cell_w = 20;
    var cell_h = 20;

    var on_data = function(data) {
        console.log('...done!');
        render_characters(data.persons);
        render_graph(data.visits, data.locations);
        render_transitions(data.transitions, data.locations);
    };

    var render_characters = function(chars) {
        d3.select('.character-list').selectAll('li')
            .data(chars)
            .enter().append('li')
            .text(function(d) { return d; });
    };

    var render_graph = function(data, locations) {
        var graph = d3.select('.graph');
        graph.text('')
            .attr('style', 'height: ' + (cell_h *  locations.length + 2) + "px;");

        graph.selectAll('div .location-legend')
            .data(locations)
            .enter().append('div').attr('class', 'location-legend')
            .text(function(d) { return d; })
            .attr('style', function(d, i) {
                return [
                    "top: " + (cell_h * i) + "px;",
                    "left: -183px;",
                    "width: 180px;",
                    "text-align: right;"
                ].join('\n');
            });

        graph.selectAll('div .point')
            .data(data)
            .enter().append('div').attr('class', 'point')
            .attr('style', function(d, i) {
                return [
                    "width: " + cell_w + "px;",
                    "height:" + (cell_h * locations.length) + "px;",
                    "left:  " + (cell_w * i) + "px;"
                ].join("\n");
            })
            .selectAll('div .location')
            .data(function(d, i) {
                return d;
            })
            .enter().append('div').attr('class', 'location')
            .attr('style', function(d, i) {
                return "width: 20px; height: 20px;" + "top:" + (20 * i) + "px;";
            })
            .attr('title', function(d, i) {
                if (d.length > 0) {
                    var persons = d.join(' and ');
                    var location = locations[i];
                    return (persons + " are at " +  location);
                }
                return "";
            })
        ;
    };

    var render_transitions = function(transitions, locations) {
        var color = d3.scale.category20();
        var svg = d3.select('.transitions');
        svg.attr({height: (cell_h *  locations.length + 2), width: 1000})
            .selectAll('g')
            .data(transitions)
            .enter().append('g')
            .each(function (d, pearson_n) {
                var g = d3.select(this);
                g.selectAll('line')
                    .data(d).enter().append('line')
                    .each(function(d) {
                        var x1 = d[0].position;
                        var y1 = d[0].location;
                        var x2 = d[1].position;
                        var y2 = d[1].location;
                        d3.select(this).attr({
                            x1: x1 * cell_w + cell_w / 2,
                            y1: y1 * cell_h + cell_h / 2,
                            x2: x2 * cell_w + cell_w / 2,
                            y2: y2 * cell_h + cell_h / 2,
                            stroke: color(pearson_n),
                            "stroke-width": 2
                        });
                    });
                g.selectAll('circle')
                    .data(d).enter().append('circle')
                    .each(function(d) {
                        var x = d[0].position;
                        var y = d[0].location;
                        d3.select(this).attr({
                            cx: x * cell_w + cell_w / 2,
                            cy: y * cell_h + cell_h / 2,
                            r: 3,
                            fill: color(pearson_n)
                        });
                    });
            });
    };

    d3.json(URLS.api, on_data);
    // on_data(the_data);
});
