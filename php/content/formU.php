<script>
	$(document).ready(function() {

		var sizeFile=0;
		var uploadObj = $("#fileuploader").uploadFile({
			url : "uploadScript.php",
			fileName : "myfile",
			dynamicFormData : function() {
				//var data ="XYZ=1&ABCD=2";
				var email = $('#uploadEmail').val();
				var data = {
					"email" : email
				};
				return data;
			},
			showQueueDiv : "status",
			onSelect : function(files) {
				sizeFile = files[0].size;
				var email = $('#uploadEmail').val();

				if (controllaMail(email)){
					$.post( "checkDime.php", { email: email, dim: sizeFile })
	  					.done(function(data) {
	  						//alert(data)
	    					if (data == true){
	    						//$(this).remove();
								//uploadObj.startUpload();
								$("#coperchio").toggleClass("clicked");
								uploadObj.startUpload();
	 						}else{
	 							$('#uploadError').text("spazio esaurito");
	 						}    						
	  					});
				}else{
					$('#uploadError').text("email non valida");
				}	
				//return false;
			},
			showStatusAfterSuccess : false,
			dragDropStr : "<div>Trascina un file qui</div>",
			showFileCounter : false,
			showCancel : true,
			showProgress : true,
			showAbort: false,
			uploadButtonClass : "buttonUpload",
			autoSubmit : false,
			onSuccess : function(files, data, xhr) {
				$("#status").append("il tuo codice è: <p class='codice'>"+data+"<p>");
			},
			onCancel : function(files, pd) {
				//$("#coperchio").toggleClass("clicked");
			},
			statusBarWidth : 380,
            dragdropWidth : 313
		});

	$("#cancelUpload").click(function() {
		uploadObj.cancelAll();
		$('#status').empty();
		$("#coperchio").toggleClass("clicked");
	});
		
	});

</script>
<div id="formU">
<div id="uploadError" class='error'></div>
<table>
	<tr>
		<td colspan="2">per uplodare inserire un email e clicca upload:</td>
	</tr>
	<tr>
		<td style="width: 10px;">Email:</td>
		<td>
			<input id="uploadEmail" class="inputText" type="email" 
			<?php 
				session_start();
				if (isset($_SESSION['user'])) {
					echo "value='".$_SESSION['user']."' disabled";
				}
			?>
			>
		</td>
	</tr>
	<tr>
		<td colspan="2"><div id="fileuploader">Upload</div></td>	
	</tr>
</table>
</div>