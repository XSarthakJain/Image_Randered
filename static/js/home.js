
function readURL(input) {
    
    if (input.files && input.files[0]) {
      var reader = new FileReader();
      
      reader.onload = function(e) {
        $('#imagePlacedID').attr('src', e.target.result);
        alert(e.target.result);
        console.log(e.target.result);
      }
      
      reader.readAsDataURL(input.files[0]); // convert to base64 string

    // Validation
    document.getElementById("upload_Image").style.display="block";
    document.getElementById("SelectFileId").style.display="none";
    }
  
    
  }
  
  $("#SelectFileId").change(function() {
    readURL(this);
  });
  