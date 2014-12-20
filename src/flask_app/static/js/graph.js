$(function(){
    function render_data(data) {
        d3.selectAll(".test")
        .data(data.xs)
        .style("font-size", function(d) { return d + "px"; });
    }
    $.getJSON(URLS.api, render_data);
})
