var chart = LightweightCharts.createChart(document.getElementById("chart"), {
	width: 800,
  height: 400,
	crosshair: {
		mode: LightweightCharts.CrosshairMode.Normal,
	},
});

var candleSeries = chart.addCandlestickSeries();

fetch('https://csci441project.herokuapp.com/history.php')
	.then((r) => r.json())
	.then((response) => {
		console.log(response)

		candleSeries.setData(response);
	})

var binanceSocket = new WebSocket(`wss://stream.binance.us:9443/ws/btcusd@kline_15m`);

binanceSocket.onmessage = function (event) {	
	var message = JSON.parse(event.data);
	
	var candlestick = message.k;
	
	console.log(candlestick)
	
	candleSeries.update({
		time: candlestick.t / 1000,
		open: candlestick.o,
		high: candlestick.h,
		low: candlestick.l,
		close: candlestick.c
	})
}

/* var lastClose = data[data.length - 1].close;
var lastIndex = data.length - 1;

var targetIndex = lastIndex + 105 + Math.round(Math.random() + 30);
var targetPrice = getRandomPrice();

var currentIndex = lastIndex + 1;
var currentBusinessDay = { day: 29, month: 5, year: 2019 };
var ticksInCurrentBar = 0;
var currentBar = {
	open: null,
	high: null,
	low: null,
	close: null,
	time: currentBusinessDay,
};

function mergeTickToBar(price) {
	if (currentBar.open === null) {
		currentBar.open = price;
		currentBar.high = price;
		currentBar.low = price;
		currentBar.close = price;
	} else {
		currentBar.close = price;
		currentBar.high = Math.max(currentBar.high, price);
		currentBar.low = Math.min(currentBar.low, price);
	}
	candleSeries.update(currentBar);
}

function reset() {
	candleSeries.setData(data);
	lastClose = data[data.length - 1].close;
	lastIndex = data.length - 1;

	targetIndex = lastIndex + 5 + Math.round(Math.random() + 30);
	targetPrice = getRandomPrice();

	currentIndex = lastIndex + 1;
	currentBusinessDay = { day: 29, month: 5, year: 2019 };
	ticksInCurrentBar = 0;
}

function getRandomPrice() {
	return 10 + Math.round(Math.random() * 10000) / 100;
}

function nextBusinessDay(time) {
	var d = new Date();
	d.setUTCFullYear(time.year);
	d.setUTCMonth(time.month - 1);
	d.setUTCDate(time.day + 1);
	d.setUTCHours(0, 0, 0, 0);
	return {
		year: d.getUTCFullYear(),
		month: d.getUTCMonth() + 1,
		day: d.getUTCDate(),
	};
}

setInterval(function() {
	var deltaY = targetPrice - lastClose;
	var deltaX = targetIndex - lastIndex;
	var angle = deltaY / deltaX;
	var basePrice = lastClose + (currentIndex - lastIndex) * angle;
	var noise = (0.1 - Math.random() * 0.2) + 1.0;
	var noisedPrice = basePrice * noise;
	mergeTickToBar(noisedPrice);
	if (++ticksInCurrentBar === 5) {
		// move to next bar
		currentIndex++;
		currentBusinessDay = nextBusinessDay(currentBusinessDay);
		currentBar = {
			open: null,
			high: null,
			low: null,
			close: null,
			time: currentBusinessDay,
		};
		ticksInCurrentBar = 0;
		if (currentIndex === 5000) {
			reset();
			return;
		}
		if (currentIndex === targetIndex) {
			// change trend
			lastClose = noisedPrice;
			lastIndex = currentIndex;
			targetIndex = lastIndex + 5 + Math.round(Math.random() + 30);
			targetPrice = getRandomPrice();
		}
	}
}, 200); */

/* let dataStream = [];
function klineStream() { */
    /* const Http = new XMLHttpRequest();
    const url='https://api.binance.us/api/v3/klines?symbol=BTCUSD&interval=1d';
    Http.open("GET", url);
    Http.send();

    Http.onreadystatechange = (e) => {
        let response = JSON.parse(Http.responseText);
        for (let i = 0; i < response.length-1; i++) {
            let timestamp = response[i][0];
            let t = getTime(timestamp/1000);
            let o = parseFloat(response[i][1]);
            let h = parseFloat(response[i][2]);
            let l = parseFloat(response[i][3]);
            let c = parseFloat(response[i][4]);
            let data = { time: t , open: o , high: h , low: l , close: c };
            dataStream.push(data);
        }; */

/*     var binanceSocket = new WebSocket(`wss://stream.binance.us:9443/ws/btcusd@kline_1h`);
    binanceSocket.addEventListener('message', function (event) {
        let message = JSON.parse(event.data);
        let timestamp = message['k']['t'];
        let t = getTime(timestamp);
        let o = parseFloat(message['k']['o']);
        let h = parseFloat(message['k']['h']);
        let l = parseFloat(message['k']['l']);
        let c = parseFloat(message['k']['c']);
        let data = { time: t , open: o , high: h , low: l , close: c };
        dataStream.push(data);
        console.log(dataStream);
    }); 
};

function getTime(ts){
    let date = new Date(ts);
    dateObject = { year: date.getFullYear() , month: date.getMonth()+1 , day: date.getDate() };
    return dateObject;
};

document.onload = klineStream(); */