const fs = require('fs');
const fileName = 'output.csv'; 
const columnNames = ['ODKAZ', 'KLUCOVE SLOVO', 'TOP', 'SCORE_2018/19', 'SCORE_2020/21', 'SCORE_2022/23'];
const headerRow = columnNames.join(';') + '\n';
fs.appendFileSync(fileName, headerRow, 'utf-8');
const parse = require('papaparse');

const filePathKeywords = 'related_queries_js.csv';

const googleTrends = require('google-trends-api');

var alreadyFetchedQuery = {};

const years = [['2018-01-01', '2019-12-31'], ['2020-01-01', '2021-12-31'], ['2022-01-01', '2023-12-31']]

function mean(array) {
    const length = array.length;

    if (length === 0) {
        return 0;
    }

    let sum = 0;
    for (let i = 0; i < length; i++) {
        sum += array[i];
    }

    return sum / length;
}

async function iterateData(result) {
    const dfContent = result.data;
    for (const entry of dfContent) {
        const link = entry['ODKAZ'];
        const keyword = entry['KLUCOVE SLOVO'];
        const topQuery = entry['TOP DOPYT'];
        console.log(topQuery);

        var scoreIndividualYear = [];

        if (topQuery in alreadyFetchedQuery) {
            for (let i = 0; i < years.length; i++) {
                scoreIndividualYear.push(alreadyFetchedQuery[topQuery][i]);
            }
        } else {
            for (let i = 0; i < years.length; i++) {
                const score = await fetchData(topQuery, years[i]);
                scoreIndividualYear.push(score);
            }
            alreadyFetchedQuery[topQuery] = scoreIndividualYear;
            console.log("ALREADY FETCHED QUERY");
            console.log(alreadyFetchedQuery);
        }

        const jsonData = [link, keyword, topQuery, scoreIndividualYear[0], scoreIndividualYear[1], scoreIndividualYear[2]];
        const csvContent = jsonData.map(value => `"${value}"`).join(';') + '\n';
        const fileName = 'output.csv';
        fs.appendFileSync(fileName, csvContent, 'utf-8');
        scoreIndividualYear = [];
    };
}


async function fetchData(topQuery, years) {
    try {
        const res = await googleTrends.interestOverTime({
            keyword: topQuery,
            startTime: new Date(years[0]), // 2018
            endTime: new Date(years[1]),  // 2019
            geo: '',
        });

        const data = JSON.parse(res);
        const timelineData = data.default.timelineData;

        const values = timelineData.map(item => item.value[0]);
        var score = mean(values);
        return score


    } catch (error) {
        console.error("Error fetching data:", error);
    }
}

fs.readFile(filePathKeywords, 'utf-8', (err, data) => {
    if (err) {
        return;
    }
    const result = parse.parse(data, {
        header: true,
        delimiter: ';'
    });
    iterateData(result)

});


