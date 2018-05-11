<!DOCTYPE html>
<html>
	<!--#########################################################
	# Created by the Semi Autonomous Rescue Team				#
	#															#
	# Author: Jack Williams										#
	# Contributors: Jack Williams								#
	#															#
	# Licensed under GNU General Public License 3.0				#
	##########################################################-->
	
	<title>Help - Video Stream</title><!--The title displayed in the browser tab bar-->
	<head>
		<!--Link Bootstrap-->
		<link rel="stylesheet" href="../assets/bootstrap.css">
		<link rel="stylesheet" href="../assets/style.css">
		<link rel="shortcut icon" href="favicon.ico" type="image/x-icon" />
	</head>
	<body>
		<div class="nav topnav">
			<div class="container">
				<ul>
					<li><br></li>
					<li><a href="../index.php">Home</a></li>
					<li><strong>|</strong></li>
					<li><a href="index.php">Help</a></li>
				</ul>
			</div>
		</div>
		<div class="page-content">
			<div class="container">
				<div class="row">
					<div class="col-md-4">
						<img src="../assets/image/circle-help.png" width="245px" />
					</div>
					<div class="col-md-8">
						<h3>Video Stream</h3>
						<p>Video is streamed directly from the robot to your device via the S.A.R.T Control Interface.</p>
						<p>The stream can be viewed on the <a href="../index.php">homepage</a>.</p>						
						<h3>Troubleshooting</h3>
						<h4><b><img src="../assets/image/image-broken.png" /> icon appears on stream</b></h4>
						<p>If the rest of the site is functional, the stream may have stopped. If you have access to the S.A.R.T, check the camera light to confirm.</p>
						<p>To restart the stream, log in to the SSH terminal and run the command <code>sudo killall motion</code> and then <code>sudo motion</code>.</p>
						<br>
						<h4><b>Framerate is too low</b></h4>
						<p>First, try to restart the stream. Log in to the SSH console and run the command <code>sudo killall motion</code> and then <code>sudo motion</code>.</p>
						<p>If this does not help, attempt to <a href="connection.php">resolve connection issues</a>.</p>
						<p>You can also check the stream settings. Make sure framerate is set to 60FPS.</p>
						<br>
						<h4><b>Stream is black</b></h4>
						<p>If you have access to the S.A.R.T, ensure that the camera has not moved or fallen. If the camera is too close to an object in poor light, the stream may appear black.</p>
						<p>If the S.A.R.T is on a mission, reverse a short distance. The S.A.R.T may be against a wall, blocking the camera.</p>						
						<br>
						<p><a href="index.php">Back to Help</a></li><p>
					</div>
				</div>
			</div>
		</div>
	</body>
</html>