/*
	Created by the Semi Autonomous Rescue Team
	Licensed under the GNU General Public License 3.0
*/

var sensorSocket;
var running_config;

var tempChart, distChart;

function update_cameras(config) {
	['front', 'left', 'right', 'back'].forEach(function (e) {
		// Get parent div of camera stream image
		var card = $("#camera_" + e + "_card");
		// Enable the div, if camera is enabled in config file
		config[e]['enabled'] ? card.show() : card.hide();
		// Set image attributes to the relevant URL
		let camera = $("#camera_" + e);
		let id = config[e]['id'];
		camera.attr("src", "http://" + ip + ":8081/" + id + "/stream");
		camera.attr("data-id", config[e]['id']);
	});
	if (!config['back']['enabled'] &&
		!config['left']['enabled'] &&
		!config['right']['enabled']) {
		$("#sensor_toggle").hide();
		$("#btm_view_camera").hide();
		$("#btm_view_sensors").show();
		$("#sensor_toggle").html("<i class='fa fa-fw fa-chart-area'></i> Show Sensors");
		sensorMode = false;
	}
}

function sensorConnection() {
	if(!demo) {
		// Start WebSocket receiver
		sensorSocket = new WebSocket("ws://" + ip + ":5556");
		sensorSocket.onopen = function() {
			sensorConnected = true;
			sensorsConnectedAlert();
		};
		sensorSocket.onclose = function() {
			if (sensorConnected) {
				sensorsDisconnectedAlert();
				sensorConnected = false;
			}

			setTimeout(function () {
				sensorConnection()
			}, 5000);
		};
		// Setup update event
		sensorSocket.onmessage = function (event) {
			var obj = JSON.parse(event.data);

			// Update sensor monitor (in log modal)
			$("#sensor_monitor_pre").html(hljs.highlight("JSON", JSON.stringify(obj, null, "\t")).value);

			if("initial_message" in obj) {
				requestConfig(function(response) {
					configReceivedAlert();

					// Populate visual editor
					// Populating advanced editor happens on configEditor change, which fires when the inital config is set
					configEditor.setValue(response);
					// Keep a copy to track changes
					baseConfig = JSON.stringify(configEditor.getValue());
					savedConfig = baseConfig;
					updateConfigAlerts();

					// Manually set output text of range slider elements
					$('output', $('#visual_editor_container'))[0].innerText = response['control']['default_gamepad_speed'];
					$('output', $('#visual_editor_container'))[1].innerText = response['control']['default_keyboard_speed'];

					// Now handle loading stuff from the config file
					// Enable / disable cameras and set their ports as defined by the config
					update_cameras(response['cameras']);

					response['sensors'].forEach(function (sensor) {
						if (sensor['enabled']) {
							console.log("Sensor type: " + sensor['type']);
						}
					});
				});

				// Other items in the initial message
				// Set running config
				running_config = obj["running_config"]
				$("#current_config").html(running_config);
				$(".editor_filename").val(running_config.slice(0,-5));

				updateConfigSelector();

				// Software versions
				if ("version_robot" in obj) {
					$("#version_robot").html(obj["version_robot"]);
				}
				if ("version_interface" in obj) {
					$("#version_interface").html(obj["version_interface"]);
				}
				if ("version_supervisorext" in obj) {
					$("#version_supervisorext").html(obj["version_supervisorext"]);
				}
			}
		}
	}
}

$(document).on("ready",function () {
	sensorConnection();
});
