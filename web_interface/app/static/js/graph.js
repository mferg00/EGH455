 backgroundColors = [
	'rgba(255, 99, 132, 0.2)',
	'rgba(54, 162, 235, 0.2)',
	'rgba(255, 206, 86, 0.2)',
	'rgba(75, 192, 192, 0.2)',
	'rgba(153, 102, 255, 0.2)',
	'rgba(255, 159, 64, 0.2)'
 ]

 borderColors = [
	'rgba(255, 99, 132, 1)',
	'rgba(54, 162, 235, 1)',
	'rgba(255, 206, 86, 1)',
	'rgba(75, 192, 192, 1)',
	'rgba(153, 102, 255, 1)',
	'rgba(255, 159, 64, 1)'
 ]
 
 function openPage(pageName, elmnt, backgroundcolor) {
		// Hide all elements with class="tabcontent" by default */
		var i, tabcontent, tablinks;
		tabcontent = document.getElementsByClassName("tabcontent");
		for (i = 0; i < tabcontent.length; i++) {
			tabcontent[i].style.display = "none";
		}
	
		// Remove the background color of all tablinks/buttons
		tablinks = document.getElementsByClassName("tablink");
		for (i = 0; i < tablinks.length; i++) {
			tablinks[i].style.backgroundColor = "";
		}
	
		// Show the specific tab content
		document.getElementById(pageName).style.display = "block";

		if (pageName != 'Gases'){
			var result = document.getElementsByClassName("tabcontent_extra")
			result[0].style.display = "none";
		}
	
		// Add the specific color to the button used to open the tab content
		elmnt.style.backgroundColor = backgroundcolor;
	}

	function createChart(id,total_data,index,label){
		var time = []
		var data = []
		total_data.forEach(function(arr){
			time.push(Math.round(arr[1],2));
			data.push(arr[index]);
		})
		new Chart(document.getElementById(id).getContext('2d'), {
			type: 'line',
			data: {
					labels: time,
					datasets: [{
							label: label,
							data: data,
							backgroundColor: backgroundColors[index-2],
							borderColor: borderColors[index-2],
							borderWidth: 2
					}]
			},
			options: {
					scales: {
						xAxes: [ {
							scaleLabel: {
								display: true,
								labelString: 'Time (s)'
							}
						}],
						yAxes: [ {
							display: true,
							scaleLabel: {
								display: true,
								labelString: label
							}
						}]
					}
			}
		});
	}

	function createNoiseChart(total_data){
		var time = []
		var noise_f1 = []
		var noise_f2 = []
		var noise_f3 = []
		total_data.forEach(function(arr){
			time.push(Math.round(arr[1],2));
			noise_f1.push(arr[6]);
			noise_f2.push(arr[7]);
			noise_f3.push(arr[8]);
		})
		new Chart(document.getElementById('noise').getContext('2d'), {
			type: 'line',
			data: {
					labels: time,
					datasets: [{
							label: 'Frequency (20 Hz - 3350 Hz)',
							fill: false,
							data: noise_f1,
							backgroundColor: backgroundColors[0],
							borderColor: borderColors[0],
							borderWidth: 2
					}, {
							label: 'Frequency (3350 Hz - 6680 Hz)',
							fill: false,
							data: noise_f2,
							backgroundColor: backgroundColors[1],
							borderColor: borderColors[1],
							borderWidth: 2
					},{
							label: 'Frequency (6680 Hz - 10010 Hz)',
							fill: false,
							data:  noise_f3,
							backgroundColor: backgroundColors[2],
							borderColor: borderColors[2],
							borderWidth: 2
					}]
			},
			options: {
					scales: {
						xAxes: [ {
							scaleLabel: {
								display: true,
								labelString: 'Time (s)'
							}
						}],
						yAxes: [ {
							display: true,
							scaleLabel: {
								display: true,
								labelString: 'Noise (dB)'
							}
						}]
					}
			}
		});
	}

	function generateTable(row,output) {

		return `
					<tr>
					<th>Gases</th>
					<th>Value</th>
					<th>Threshold</th>
					<th>Unit</th>
					<th>Status</th>
				</tr>
				<tr>
					<td>Oxidise</td>
					<td>${row[3]}</td>
					<td>${row[0]}</td>
					<td>Ohms</td>
					<td>${output[0]}</td>
				</tr>
				<tr>
					<td>Reducing</td>
					<td>${row[4]}</td>
					<td>${row[1]}</td>
					<td>Ohms</td>
					<td>${output[1]}</td>
				</tr>
				<tr>
					<td>Nh3</td>
					<td>${row[5]}</td>
					<td>${row[2]}</td>
					<td>Ohms</td>
					<td>${output[2]}</td>
				</tr>
			 `
	}

  function ajax_other(){
		$.ajax({
			url: "http://localhost:5000/get_data",
			type: 'GET',
			success: function(res) {
				var sensors = ["pressure","humidity","light","temperature"];
				var labels = ["Pressure (Pa)","Humidity (%)","Light (Lux)","Temperature (Celsius)"];
				for(var i = 0; i < sensors.length; i++){
					createChart(sensors[i],res,i+2,labels[i]);
				}
				createNoiseChart(res);
			}
		});
	}
	
	function ajax_gases(){
		$.ajax({
			url: "http://localhost:5000/get_gases",
			type: 'GET',
			success: function(res){
				if (res.length > 0){
						var output = []
						if(res[0][3] > res[0][0]){
							output.push('Above');
						}
						else{
							output.push('Below');
						}
						if(res[0][4] > res[0][1]){
							output.push('Above');
						}
						else{
							output.push('Below');
						}
						if(res[0][5] > res[0][2]){
							output.push('Above');
						}
						else{
							output.push('Below');
						}
						$('#gas_table').empty();
						$('#gas_table').append(generateTable(res[0],output));
				}
			}
		});
	}


	setInterval(ajax_other, 3000);
	setInterval(ajax_gases, 3000);