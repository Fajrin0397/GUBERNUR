const DEFAULT_CORD = [0.692574, 127.370179];
    const myMap = L.map("mymap");

    
    const atrib = "Tidore, 20-November-2023";

    const osmTile = new L.TileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {minzoom:2, maxzoom:20, attribution:atrib});
    
    
    var Esri_WorldImagery = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
	attribution: 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'
});
    
    
    myMap.setView(new L.LatLng(DEFAULT_CORD[0], DEFAULT_CORD[1]), 10);
    myMap.addLayer(osmTile);

    // const Marker = L.marker(DEFAULT_CORD).addTo(Map);

    let markers = L.markerClusterGroup();
   
    var baseMap = {
      'OSM' : osmTile,
      'Esri_WorldImagery': Esri_WorldImagery
    }
    L.control.layers(baseMap).addTo(myMap)
    L.Control.geocoder().addTo(myMap);
    
    var markersLayer = new L.LayerGroup();
    L.control.search({
            position: 'topleft',
            layer: markersLayer,
            initial: false,
            zoom: 12,
            marker: false
        }).addTo(myMap);

    fetch('/tojson')
    .then(res => {
     return res.json()})
    .then(res => {
        for(mr of res.users){
      var lok = L.marker([mr.lat, mr.lon]);
      var ids = mr.Idtps
      lok.bindPopup(`<h4>${mr.nama_tps}</h4>  
      <button type="button"data-toggle="modal" data-target="#exampleModal" onclick='getTps(${ids})'>
          lihat hasil
      </button>
       `
      )
      
        
      markers.addLayer(lok);
      myMap.addLayer(markers);
      myMap.fitBounds(markers.getBounds())
    }
    })
    
    function getTps(tps){
      fetch('/jsonprov/'+tps)
      .then(cek => {
        return cek.json()
      })
      .then(cek => {
        var tampung1 = cek.map(function(index){
          return index.nama
        })

        var tampung2 = cek.map(function(index){
          return index.suara 
        })
            const data = {
                labels: tampung1,
                datasets: [{
                  //label: cek.nama_tps,
                  backgroundColor: ['blue', 'red','orange', 'purple', 'green', 'yellow'],
                  borderColor: 'rgb(255, 99, 132)',
                  data: tampung2 }]
                                }
                                const config = {
                                type: 'pie',
                                data: data,
                                options: {
                                        plugins:{
                                          legend:{
                                            display: false,
                                            
                                          } }
                                      }
              }
            var ctx = document.getElementById('ChartKu').getContext('2d');
            let chartStatus = Chart.getChart("ChartKu");
            if (chartStatus != undefined) {
              chartStatus.destroy();
              }  
            let myChart = new Chart(
            ctx,
            config)
      })
    }
 
    L.control.search().addTo(myMap);
    let sidebar = L.control.sidebar('sidebar', {
      position: 'left'
    });
  
    myMap.addControl(sidebar);  
    var easy = L.easyButton('fa-exchange', function(){
      sidebar.toggle();
    }).addTo(myMap);  

    let prov = document.getElementById('lokasiprov');
    let socket = io()

    socket.on('connect', function(){
      prov.onchange = function(){
      // console.log(pilihDapil.value)
      socket.emit('datadprprov', prov.value)
    }
    })

    socket.on('hasJsonprov', JsonData => {
      let tampungNama = JsonData.map(function(index){
      return index.Nama_Caleg
      })

      let tampungSuara = JsonData.map(function(index){
        return index.Total_suara
      })
      const ctx = document.getElementById('myChartProv').getContext('2d');
      let chartStatus = Chart.getChart("myChartProv");
            if (chartStatus != undefined) {
              chartStatus.destroy();
              }  

        const myChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: tampungNama,

            datasets: [{
                data: tampungSuara,
                backgroundColor: [
                    'green','blue','red', 'purple', 'yellow', 'orange' 
                ],
                borderWidth: 1
            }]
        },
        options: {
          plugins:{
            legend:{
              display: false,
            } }
        }
    });
    })