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


    // .map the keys to get html content and generate html content

    const cards = objKeys.map(key => {
        return `<div class="card">
                    <div class="card-body">
                        <h2 class="card-title">${dataObj[key].symbol}</h2>
                        <hr>
                        <h5>${dataObj[key].upper_std}</h5>
                    </div>
                </div>`
    }).join('');
    const cardRow = document.querySelector('.card-row');
    const timeRow = document.querySelector('.donate-row .time');
    timeRow.textContent = `Last update: ${dataObj['time']}`
    cardRow.innerHTML = cards;
}

getData();


let slider = document.querySelector('.custom-range')

//divide by 100 since the html range is -500 to 500 
stdMulti.innerHTML = (slider.valueAsNumber) / 100

function refresh() {
    rangeValue = (slider.valueAsNumber) / 100

    // divided by 100 to since the HTML slider range is 0 to 500 
    stdMulti.innerHTML = rangeValue

    //rerun getData() with the input value param
    getData(rangeValue)
}

//refresh when it moves
slider.addEventListener('input', refresh)
