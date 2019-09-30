/*
	Created by the Semi Autonomous Rescue Team
	Licensed under the GNU General Public License 3.0
*/

var ssh_count = 1;
var ssh_current = 1;
	
function focusCurrentSsh() {
	setTimeout(function() {
		$("#ssh_iframe_" + ssh_current).focus();
	}, 200);
}

var ssh_tab_icon='<i class="fa fa-fw fa-terminal"></i> ';

$(document).ready(function() {
    $('#ssh-new-tab').click(function() {
		ssh_count++;
		let iframe_url = $("#ssh_iframe_1").attr("src"); // We know the correct URL exists in iframe 1 - use it.
		
		// Get ready to go to the new tab
		$('#ssh-tab-' + ssh_current + ' > a').removeClass("active");
		$('#ssh-term-' + ssh_current).removeClass("active");
		$('#ssh-term-' + ssh_current).removeClass("show");
		ssh_current = ssh_count;
		
		// Create the tab and terminal
		$('#ssh-new-tab').before('<li class="nav-item ssh-tab" id="ssh-tab-'+ ssh_count +'"><a class="nav-link text-dark active" href="#ssh-term-' + ssh_count + '" role="tab" data-toggle="tab" aria-selected="true">' + ssh_tab_icon + ssh_count + '</a></li>');
        $('#ssh-term-content').append($('<div class="tab-pane fade active show" id="ssh-term-' + ssh_count + '"><iframe id="ssh_iframe_'+ ssh_count +'" src="'+ iframe_url +'" width="100%" height="400px" onload="focusCurrentSsh()" class="rounded-bottom"></iframe></div>'));
    });
	
	$("#sshModal").on('shown.bs.modal', function () {
		focusCurrentSsh(); // Focus the current SSH iframe on modal open
		// Set the src of the modal on first load only
		if ($("#ssh_iframe_1").attr("src") == "") {	// Prevent refresh every time the modal is loaded
			$("#ssh_iframe_1").attr("src", portString(4200));
		}
	});
	
	// Refresh terminal
	$("#ssh-refresh-button").click(function () {
		$("#ssh_iframe_" + ssh_current).attr("src", $("#ssh_iframe_" + ssh_current).attr("src"));
	});
	
	// Focus the SSH terminal when the user switches tabs
	$("#ssh-term-list").click(function(){
		try {
			ssh_current = event.target.closest(".ssh-tab").getAttribute("id").replace(/[^0-9\.]/g, '');
			focusCurrentSsh();
		} catch (e) {
			return;
		}
	});
});
