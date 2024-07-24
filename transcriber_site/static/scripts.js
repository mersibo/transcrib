document.addEventListener('DOMContentLoaded', function() {
    let body = document.body;
    let progressBar = document.getElementById('progress_bar');
    let downloadLink = document.getElementById('download_link');
    let fileInput = document.getElementById('file_input');
    let uploadArea = document.getElementById('upload_area');

    body.ondragover = function(event) {
        event.preventDefault();
        body.classList.add('dragging');
    };

    body.ondragleave = function(event) {
        event.preventDefault();
        body.classList.remove('dragging');
    };

    body.ondrop = function(event) {
        event.preventDefault();
        body.classList.remove('dragging');
        if (event.dataTransfer.files.length > 0) {
            var file = event.dataTransfer.files[0];
            uploadFile(file);
        }
    };

    fileInput.addEventListener('change', function(event) {
        if (this.files.length > 0) {
            uploadFile(this.files[0]);
            progressBar.style.opacity = '1'; 
            uploadArea.classList.add('moving-up'); 
        }
    });

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
                alert('Файл успешно загружен и обработан');
            } else {
                alert('Произошла ошибка!');
            }
        };

        xhr.onerror = function() {
            alert('Ошибка загрузки: ' + xhr.statusText);
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