function generateRandomMap() {
    var map = document.getElementById('map');
    map.innerHTML = ''; 

    for (var i = 0; i < 150; i++) {
        for (var j = 0; j < 150; j++) {
            var cell = document.createElement('div');
            cell.className = 'cell';

            var rand = Math.random();
            if (rand < 0.01) { 
                var buildingImg = document.createElement('img');
                buildingImg.src = 'build1.png';
                buildingImg.className = 'building-img';
                cell.appendChild(buildingImg);
            } else if (rand < 0.05) { 
                cell.className += ' building';
                cell.style.width = '30px';
                cell.style.height = '30px';
            } else if (rand < 0.15) {
                cell.className += ' building';
                cell.style.width = '20px';
                cell.style.height = '20px';
            } else if (rand < 0.25) { 
                cell.className += ' house';
                cell.style.width = '10px';
                cell.style.height = '20px';
            } else if (rand < 0.5) { 
                cell.className += ' road';
            }

            map.appendChild(cell);
        }
    }
}

generateRandomMap();

document.getElementById('redesign-btn').addEventListener('click', function() {
    generateRandomMap();
});
