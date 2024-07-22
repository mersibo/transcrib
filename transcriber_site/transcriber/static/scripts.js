document.addEventListener('DOMContentLoaded', function() {
    let dropZone = document.getElementById('drop_zone');
    let progressBar = document.getElementById('progress_bar');
    let downloadLink = document.getElementById('download_link');

    dropZone.ondrop = function(e) {
        e.preventDefault();
        this.className = 'drop_zone';
        uploadFile(e.dataTransfer.files[0]);
    };

    dropZone.ondragover = function() {
        this.className = 'drop_zone_hover';
        return false;
    };

    dropZone.ondragleave = function() {
        this.className = 'drop_zone';
        return false;
    };

    function uploadFile(file) {
        let formData = new FormData();
        formData.append('file', file);
        
        let xhr = new XMLHttpRequest();
        xhr.open('POST', '/upload/', true);

        xhr.upload.onprogress = function(e) {
            if (e.lengthComputable) {
                let percentage = (e.loaded / e.total) * 100;
                progressBar.value = percentage;
            }
        };

        xhr.onload = function() {
            if (xhr.status === 200) {
                let response = JSON.parse(xhr.responseText);
                downloadLink.href = response.download_url;
                downloadLink.style.display = 'block';
                alert('File uploaded and processed successfully');
            } else {
                alert('An error occurred!');
            }
        };

        xhr.send(formData);
        
        
        let eventSource = new EventSource('/upload/');
        eventSource.onmessage = function(event) {
            let progress = parseInt(event.data);
            progressBar.value = progress;
            if (progress === 100) {
                eventSource.close();
            }
        };
    }
});
