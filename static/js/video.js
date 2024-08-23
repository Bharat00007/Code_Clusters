const localVideo = document.getElementById('localVideo');
const remoteVideo = document.getElementById('remoteVideo');

navigator.mediaDevices.getUserMedia({ video: true, audio: true })
    .then(stream => {
        localVideo.srcObject = stream;
        const peer = new SimplePeer({
            initiator: location.hash === '#init',
            trickle: false,
            stream: stream
        });

        peer.on('signal', data => {
            console.log('SIGNAL', JSON.stringify(data));
        });

        peer.on('stream', stream => {
            remoteVideo.srcObject = stream;
        });

        // For demonstration purposes, we'll log the signaling data to the console.
        // In a real-world app, you'd send it to the other peer via your Flask-SocketIO backend.
    })
    .catch(error => {
        console.error('Error accessing media devices.', error);
    });
