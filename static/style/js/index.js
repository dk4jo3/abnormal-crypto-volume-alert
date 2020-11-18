async function getData(std_cap) {
    const results = await fetch('volumeData.json');
    const dataObj = await results.json();

    // get keys and push into a new array, remove the time one, and filter out the ones below std_cap
    let objKeys =
        Object.keys(dataObj)
        .filter(key => key !== 'time' && dataObj[key].upper_std >= std_cap);


    //    Data Set Format for dataObj['bitcoin']
    //    last_hour_volume: 16632680789.936144
    //    upper_std: -0.9745
    //    volume_mean: 25002672636.009663
    //    volume_std: 8589051940.060508
    //    1h: 0.23


    // .map the keys to get html content and generate html content

    const cards = objKeys.map(key => {
        return `<div class="card">
                    <a href="https://coingecko.com/en/coins/${key}" class="custom-card"><div class="card-body">
                        <h2 class="card-title">${dataObj[key].symbol}</h2>
                        <hr>
                        <h5>${dataObj[key].upper_std}</h5>
                        <p>
                        <span ${dataObj[key].hour >= 0 ? `class="red"` : `class="green"`}>1H : ${dataObj[key].hour >= 0 ? `+` : ``}${dataObj[key].hour} % </span><br>
                        <span ${dataObj[key].day >= 0 ? `class="red"` : `class="green"`}>1D : ${dataObj[key].day >= 0 ? `+` : ``}${dataObj[key].day} % </span><br>
                        <span ${dataObj[key].week >= 0 ? `class="red"` : `class="green"`}>1W : ${dataObj[key].week >= 0 ? `+` : ``}${dataObj[key].week} % </span>
                        </p>
                    </div>
                </div></a>`
    }).join('');
    const cardRow = document.querySelector('.card-row');
    const timeRow = document.querySelector('.donate-row .time');
    timeRow.textContent = `Last update: ${dataObj['time']}`
    cardRow.innerHTML = cards;
}

let slider = document.querySelector('.custom-range')

//divide by 100 since the html range is 0 to 50 
stdMulti.innerHTML = (slider.valueAsNumber) / 10

function refresh() {
    rangeValue = (slider.valueAsNumber) / 10

    // divided by 10 to since the HTML slider range is 0 to 50
    stdMulti.innerHTML = rangeValue

    //re-run getData() with the input value param
    getData(rangeValue)
}

//refresh when it moves
slider.addEventListener('input', refresh)

getData((slider.valueAsNumber) / 10);
