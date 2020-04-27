$(document).ready(function () {


    //.. Load Report
    $.getJSON("../generated_data/report.json", function (json) {
        $('#total_tweets').html(json.total_tweets);


        const pos_neg_ctx = document.getElementById('posNegPie').getContext('2d');
        const pos_tweet_count = json.positive_count;
        const neg_tweet_count = json.negative_count;

        //.. handle positive and negative count
        let data = [pos_tweet_count, neg_tweet_count]
        pieChart(pos_neg_ctx, data)
        $('#pos_tweet_cnt').html(pos_tweet_count)
        $('#neg_tweet_cnt').html(neg_tweet_count)


        //.. handle emojie count
        data = json.top_words;
        let id = '#wordCount';
        let columns = [{title: 'Word'}, {title: 'Occurrence'}]
        dataTables(id, data, columns)


        //.. handle emojie count
        data = json.emoji_count
        id = '#emojiCount';
        columns = [{title: 'Emoji'}, {title: 'Occurrence'}]
        dataTables(id, data, columns)

         //.. handle geo count
        data = json.user_locations
        id = '#geoCount';
        columns = [{title: 'Location'}, {title: 'Occurrence'}]
        dataTables(id, data, columns)

        //.. handle positive tweets
        $('#savedPosTotal').html(json.total_certain_positive);
        rawData = json.positive_tweets;
        data = [];
        rawData.forEach(function(d){
            data.push([d.confidence, d.tweet])
        });
        id = '#savedPosTweets';
        columns = [{title: 'Confidence Level'}, {title: 'tweet'}]
        dataTables(id, data, columns)

                //.. handle positive tweets
        $('#savedNegTotal').html(json.total_certain_negative);
        rawData = json.negative_tweets;
        data = [];
        rawData.forEach(function(d){
            data.push([d.confidence, d.tweet])
        });
        id = '#savedNegTweets';
        columns = [{title: 'Confidence Level'}, {title: 'tweet'}]
        dataTables(id, data, columns)




    });

    //.. Load Config
    $.getJSON("../config.json", function (json) {
        $('#conf_level').html(json.confidence_level);
        $('#conf_save_level').html(json.tweet_save_limit);
        $('#top_word_limit').html(json.top_word_limit);


    });

}); //.. end ready function


//.. Function to handle pie charts
function pieChart(ctx, data) {
    var myChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: ['Positive Tweets', 'Negative Tweets'],
            datasets: [{
                label: '# of Votes',
                data: data,
                backgroundColor: [
                    'rgb(38,255,14)',
                    'rgb(235,54,54)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: false
        }

    });
}


//.. Function to handle data tables
function dataTables(id, dataset, columns) {
    $(id).DataTable({
        data: dataset,
        columns: columns
    });
}






