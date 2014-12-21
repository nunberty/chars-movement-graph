$(function(){
    var on_data = function(data) {
        console.log('...done!');
        render_characters(data.persons);
        render_graph(data.visits, data.locations);
    };

    var render_characters = function(chars) {
        d3.select('.character-list').selectAll('li')
            .data(chars)
            .enter().append('li')
            .text(function(d) { return d; });

    };

    var render_graph = function(data, locations) {
        var cell_w = 20;
        var cell_h = 20;
        var g = d3.select('.graph');
        g.text('')
            .attr('style', 'height: ' + (cell_h *  locations.length + 2) + "px;");

        g.selectAll('div .location-legend')
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

        g.selectAll('div .point')
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
            .text(function(d) {
                return d.length > 0 ? "x": "";
            })
            .on('click', function(d, i) {
                if (d.length > 0) {
                    var persons = d.join(' and ');
                    var location = locations[i];
                    alert(persons + " are at " +  location);
                }
            })
        ;
    };

    // d3.json(URLS.api, on_data);
    on_data(the_data);
});








































var the_data = {"persons": ["Mrs. Jones", "Boxer", "Moses", "Mollie", "Clover", "Benjamin", "Monday Mr Whymper", "Meetings Snowball", "Comrade Napoleon", "Mollie\u2019s", "Squealer", "Snowball\u2019s", "Major"], "visits": [[[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], ["Mrs. Jones"]], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], ["Major"], [], [], [], [], [], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], ["Mrs. Jones"], [], [], [], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], ["Moses"], [], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], ["Mrs. Jones"], [], [], [], [], [], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], ["Mrs. Jones"]], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], ["Meetings Snowball"], [], [], [], []], [[], ["Meetings Snowball"], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], ["Meetings Snowball"], [], [], [], [], [], [], [], [], ["Meetings Snowball"], [], []], [[], ["Comrade Napoleon", "Meetings Snowball"], [], [], [], [], [], [], [], ["Comrade Napoleon", "Meetings Snowball"], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], ["Mrs. Jones"], [], [], [], [], [], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], ["Mrs. Jones"]], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], ["Mrs. Jones"], [], [], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], ["Meetings Snowball"]], [[], [], [], [], [], [], [], [], [], [], [], [], [], ["Squealer"], [], [], [], [], [], [], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], ["Monday Mr Whymper", "Mrs. Jones"], [], [], [], [], [], [], [], [], [], [], [], [], ["Monday Mr Whymper", "Mrs. Jones"]], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], ["Comrade Napoleon", "Monday Mr Whymper"], [], ["Comrade Napoleon", "Monday Mr Whymper"], [], [], ["Comrade Napoleon", "Monday Mr Whymper"]], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], ["Clover"], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], ["Meetings Snowball"], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], ["Meetings Snowball", "Monday Mr Whymper"], [], ["Meetings Snowball", "Monday Mr Whymper"], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], ["Monday Mr Whymper"], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], ["Meetings Snowball", "Monday Mr Whymper"], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], ["Comrade Napoleon"], [], [], [], [], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], ["Comrade Napoleon"], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], ["Comrade Napoleon"], [], [], [], [], [], [], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], ["Mrs. Jones"], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], ["Comrade Napoleon", "Mrs. Jones"], [], ["Comrade Napoleon", "Mrs. Jones"], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], ["Mrs. Jones"], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], ["Mrs. Jones"], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], ["Comrade Napoleon", "Mrs. Jones"], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], ["Meetings Snowball", "Mrs. Jones"], [], ["Meetings Snowball", "Mrs. Jones"], [], [], []], [[], [], [], [], ["Mrs. Jones"], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []], [[], [], [], [], [], ["Boxer"], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], ["Comrade Napoleon", "Mrs. Jones"], [], [], [], [], [], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], ["Squealer"], [], [], [], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], ["Boxer", "Comrade Napoleon"], [], [], [], [], [], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], ["Boxer", "Squealer"], [], [], [], [], [], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], ["Clover"], [], [], [], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], ["Mrs. Jones"], [], []], [[], ["Major"], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], ["Benjamin"], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], ["Mrs. Jones"], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], ["Mrs. Jones"], [], [], [], [], []]], "title": "Animal Farm", "locations": ["Hides", "England", "Man", "Frederick\u2019", "Fox-wood", "Jessie", "Pilkington\u2019", "Humanity\u2019", "Mankind", "Beasts", "England\u201d", "England.\u2019", "Clementine", "Minimus", "Willingdon Beauty", "England\u2019", "Animalism", "Nature", "Sugarcandy Mountain", "Julius Caesar\u2019s", "Queen Victoria", "Boxer\u2019s", "Pinchfield Farm", "MANOR FARM", "Foxwood Farm", "Seven Commandments", "Science", "Manor Farm"]};
