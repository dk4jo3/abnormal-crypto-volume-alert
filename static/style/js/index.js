// asyng function to fetch
//async function getData() {
//    const results = await fetch('volumeData.json');
//    const dataObj = await results.json();
//    console.log(dataObj);
//
//
//    // shorten Object.keys function
//    function getKeys(n) {
//        return Object.keys(n);
//    }
//
//    // get keys and push into a new array
//
//    let objKeys = [];
//
//    // -1 since the last object is time
//    for (i = 0; i < getKeys(dataObj).length - 1; i++) {
//        objKeys.push(getKeys(dataObj)[i]);
//    }
//    console.log(objKeys)
//
//    // .map the keys to get html content and generate html content
//    const cards = objKeys.map(key => {
//        return `<div class="col-md-4">
//                <div class="card">
//                    <div class="card-body">
//                        <h2 class="card-title">${key}</h2>
//                        <hr>
//                        <h5>${dataObj[key].btc}%</h5>
//                        <span class="card-label">BTC</span>
//                        <hr>
//                        <div class="row">
//                            <div class="col-6">
//                                <h5>${dataObj[key].alt_mean}%</h5>
//                                <p class="card-label">Alts Mean</p>
//                            </div>
//                            <div class="col-6">
//                                <h5>${dataObj[key].alt_median}%</h5>
//                                <p class="card-label">Alts Median</p>
//                            </div>
//                        </div>
//
//                    </div>
//                </div>
//            </div>`
//    }).join('');
//    const cardRow = document.querySelector('.card-row');
//    const timeRow = document.querySelector('.donate-row .time');
//    timeRow.textContent = `Last update: ${dataObj['time']}`
//    console.log(cards);
//    cardRow.innerHTML = cards;
//
//}
//
//getData();


let slider = document.querySelector('.custom-range')
stdMulti.innerHTML = (slider.valueAsNumber) / 100

function refresh() {
    // divided by 100 to since the HTML slider range is 0 to 500 
    stdMulti.innerHTML = (slider.valueAsNumber) / 100
}

slider.addEventListener('input', refresh)