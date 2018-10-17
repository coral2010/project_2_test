d3.json('/entrances').then(function(d){console.log(d)});

function buildBubbleChart() {
    // instead of referencing /scraped_data, each d3.json should reference route with its specific collection
    var url = '/economic_benefits';

    d3.json(url).then(function(data) {
        console.log('Economic Benefit Data');
        console.log(data);
        console.log('-----------------------------------')
        
        
        var years = data[0].years;
        var amounts = data[0].amounts;
        var jobCounts = data[0].job_counts;
        var visitorCounts = data[0].visitor_counts
        console.log('Years');
        console.log(years);
        console.log('Economic Benefit $ Amount (in millions');
        console.log(amounts);
        console.log('Job Counts');
        console.log(jobCounts);
        console.log('Visitor Counts');
        console.log(visitorCounts);

    });
};


buildBubbleChart()

