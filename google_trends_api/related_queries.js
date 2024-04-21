const fs = require('fs');
const parse = require('papaparse');
const googleTrends = require('google-trends-api');

const file_path_keywords = 'input_for_top_queries_js.csv';
const topResults = {};

fs.readFile(file_path_keywords, 'utf8', (err, data) => {
  if (err) {
    return;
  }

  const result = parse.parse(data, {
    header: true,
    delimiter: ';'
  });

  const columnNames = ['ODKAZ', 'KLUCOVE SLOVO', 'TOP DOPYT'];
  const headerRow = columnNames.join(';') + '\n';
  const fileName = 'top_queries_js.csv';
  fs.appendFileSync(fileName, headerRow, 'utf-8');

  const df_content = result.data;
  df_content.forEach((entry, index) => {
    const link = entry['ODKAZ'];
    const keywordsValue = entry['KLUCOVE SLOVO'];
    console.log(keywordsValue);
    if (keywordsValue in topResults) {
      existing_values = topResults[keywordsValue]
      for (const value of existing_values) {
        const jsonData = [link, keywordsValue, value];
        const csvContent = jsonData.map(value => `"${value}"`).join(';') + '\n';
        fs.appendFileSync(fileName, csvContent, 'utf-8')
      }
    } else {
      topResults[keywordsValue] = [];
      console.log(keywordsValue);
      googleTrends.relatedQueries({ keyword: keywordsValue, startTime: new Date('2018-01-01'), endTime: new Date('2023-12-31') })
        .then((res) => {
          const data = JSON.parse(res);
          for (const rankedKeyword of data.default.rankedList) {
            for (const keyword of rankedKeyword.rankedKeyword) {
              const queryValue = keyword.query;
              topResults[keywordsValue].push(queryValue)
              const jsonData = [link, keywordsValue, queryValue];
              const csvContent = jsonData.map(value => `"${value}"`).join(';') + '\n';
              fs.appendFileSync(fileName, csvContent, 'utf-8');
            }
          }
        })
        .catch((err) => {
          console.log(err);
        })
    }
  });
});