$(function () {
    //http://jsfiddle.net/influenztial/qy7h5/
    //https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API/Tutorial/Using_images
    //https://www.w3schools.com/tags/canvas_rect.asp
    //https://www.w3schools.com/tags/canvas_drawimage.asp
    var imageLoader = $('#imageLoader')[0];
    imageLoader.addEventListener('change', handleImage, false);
});

function handleImage(e) {
    var canvas = document.getElementById('imageCanvas');
    var ctx = canvas.getContext('2d');
    var reader = new FileReader();
    clear_fields();
    reader.onload = function (event) {
        var img = new Image();
        img.onload = function () {
            //img.width = "400px";
            //img.height = "600px";
            canvas.width = img.width;
            canvas.height = img.height;
            ctx.drawImage(img, 0, 0);
        }
        img.src = event.target.result;
    }
    reader.readAsDataURL(e.target.files[0]);
    sendImage();
}


function clear_fields() {
    $("#resultado").html("");

}

function sendImage() {
    var formData = new FormData();
    var img = document.getElementById('imageLoader').files[0];
    formData.append('file', img);
    $.ajax({
        url: "/api/recognition", // url where to submit the request
        type: "POST", // type of action POST || GET
        dataType: 'json', // data type
        data: formData, // post data || get data,
        processData: false,
        contentType: false,
        success: function (result) {
            var array = result;
            var json = JSON.stringify(result);
            console.log('Typeof: ' + typeof (array));
            $("#resultado").html(json);
            drawFaceLocation(array);
        },
        error: function (xhr, resp, text) {
            console.log(xhr, resp, text);
        }
    });
}

function drawFaceLocation(array) {
    var canvas = document.getElementById('imageCanvas');
    var ctx = canvas.getContext('2d');

    for (n in array) {
        var persons = array[n];
        var name = persons[0];
        var face_location = persons[1];
        top_ = face_location[0];
        right_ = face_location[1];
        bottom_ = face_location[2];
        left_ = face_location[3];
        width = (left_ - right_);
        height = (top_ - bottom_);
        console.log('top: ' + top_);
        console.log('right: ' + right_);
        console.log('bottom: ' + bottom_);
        console.log('left: ' + left_);
        console.log('name: ' + name);
        ctx.beginPath();
        ctx.lineWidth = "3";
        ctx.rect(right_, bottom_, width, height);
        ctx.stroke();
        ctx.beginPath();
        size = 18;
        ctx.font = size + 'px Arial';
        ctx.fillStyle = 'red';
        ctx.textAlign = 'center';
        ctx.fillText(name, left_ + (ctx.measureText(name).width / 2), (bottom_ + size));
        ctx.stroke();

        var dataURL = canvas.toDataURL();
        document.getElementById('canvasImg').src = dataURL;

}
}