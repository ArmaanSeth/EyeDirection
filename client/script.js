const video = document.querySelector("video");
const p = document.querySelector("p");
const websocket = new WebSocket("ws://localhost:8765");
if (navigator.mediaDevices.getUserMedia) {
  navigator.mediaDevices
    .getUserMedia({ video: true })
    .then(function (stream) {
      video.srcObject = stream;
      websocket.binaryType = "arraybuffer";
      video.play();
      websocket.onopen = () => {
        p.innerHTML = "Hurray!, You are connected to the world chat";
      };
      //send the stream to the server every 0.1s
      video.addEventListener("play", function () {
        setInterval(() => {
          sendFrame();
        }, 100);
      });
      function sendFrame() {
        //used canvas to send blob object
        let canvas = document.createElement("canvas");
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        let context = canvas.getContext("2d");
        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        canvas.toBlob(function (blob) {
          websocket.send(blob);
        }, "image/jpeg");
      }
      
    })
    .catch(function (error) {
      console.log("Something went wrong with webcam access: ", error);
    });
}
