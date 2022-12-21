const express = require('express')
const parse = require("csv-parse")
const os = require('os')
const fs = require("fs")

//调用方法创建一个服务器
const app = express()
const port = 3000
//解析json格式的请求体
app.use(express.json())
//解析查询字符串格式的情趣 
app.use(express.urlencoded({extended:true}))


app.get('/', (req, res) => {
  res.send('Hello World!')
})

app.all('*', function (req, res, next) {
    res.header('Access-Control-Allow-Origin', '*');
    //Access-Control-Allow-Headers ,可根据浏览器的F12查看,把对应的粘贴在这里就行
    res.header('Access-Control-Allow-Headers', 'Content-Type');
    res.header('Access-Control-Allow-Methods', '*');
    res.header('Content-Type', 'application/json;charset=utf-8');
    next();
});



app.get('/read-csv', function(req, res) {

    const filepath = './assets/driver1_trajectory.csv'
    const data = fs.readFileSync(filepath)
    console.log('read-csv')
    //使用resdata{'initdata', 1}作为传输数据信号
    //
    parse.parse(data, (err, records) => {
        resdata = {
            'columns': records[0], 
            'data': records.splice(1, records.length).map((d) => {return [+d[0], +d[1]+0.0025, +d[2]-0.0025, +d[3], d[4]]}), 
            'initdata': 1}
        if (err) {
            console.error(err)
            return res.status(400).json({success: false, message: 'An error occurred'})
        }
        return res.json(resdata)
    })
})

app.listen(port, () => {
    console.log(`Example app listening on port ${port}`)
})