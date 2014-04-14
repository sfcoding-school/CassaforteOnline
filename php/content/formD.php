<script>
	$(document).ready(function() {
		
		$('#recupera').click(function() { 
			var codice = $('#recuperaCodice').val();
			var email = $('#recuperaEmail').val();
			//alert('codice: '+codice+' lenght: '+codice.length);
			if ((codice.length==10) && (controllaMail(email))){
				$('#formU').hide();
				$("#coperchio").toggleClass("clicked");
				$('#down').html('attendere');
				$.get('download.php', {code: codice, email: email})
					.done(function(data){
						if(data!=-1){
							//alert(data);
							$('#down').html('il download inizierà automaticamente..');
							$("body").append("<iframe src='download.php/?fileUuid=" + data + 
								"' style='display: none;' ></iframe>");
						}else{
							$('#down').html('fallito');
						}
					});

				//$('#down').attr('src', 'download.php/?code='+codice+'&email='+email);
				//window.location='download.php/?code='+codice+'&email='+email;
			}else{
				$('#recuperaError').text('codice errato!');
			}
		});
	});

</script>

<div id="formD">
	<div id="recuperaError" class='error'></div>
	<table class='formTableD'>
		<tr>
			<td colspan="2" class="testo">inserisci qui il codice del file e la tua email:</td>
		</tr>
		<tr>
			<td>Email:</td>
			<td><input class="inputText" type="text" id="recuperaEmail"
				<?php 
				session_start();
				if (isset($_SESSION['user'])) {
					echo "value='".$_SESSION['user']."' disabled";
				}
			?>
			></td>
		</tr>
		<tr>
			<td>Codice:</td>
			<td><input class="inputText" type="text" id="recuperaCodice"></td>		
		</tr>
		<tr>
			<td colspan="2"><div id="recupera" class="button">Recupera</div></td>
		</tr>
	</table>	
</div>