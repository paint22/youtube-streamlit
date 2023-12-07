document.addEventListener('DOMContentLoaded', function () {
    const openCameraButton = document.getElementById('openCamera');
    const camera = document.getElementById('camera');
    const takePhotoButton = document.getElementById('takePhoto');
    const cancelCameraButton = document.getElementById('cancelCamera');
    const retakePhotoButton = document.getElementById('retakePhoto');
    const confirmPhotoButton = document.getElementById('confirmPhoto');
    const photoInput = document.getElementById('photo');
    const canvas = document.getElementById('canvas');
    const context = canvas.getContext('2d');
    let mediaStream;
    let isCaptured = false;

    // カメラを開く処理を関数にまとめる
    function openCamera() {
        navigator.mediaDevices.getUserMedia({ video: true })
            .then(function (stream) {
                mediaStream = stream;
                camera.srcObject = stream;
                openCameraButton.style.display = 'none';
                takePhotoButton.style.display = 'inline';
                cancelCameraButton.style.display = 'inline';
                camera.style.display = 'block';
                // カメラを再生
                camera.play();
            })
            .catch(function (error) {
                console.error('カメラアクセスエラー:', error);
                alert('カメラにアクセスできません。');
            });
    }

    // キャンセル処理を関数にまとめる
    function cancelCamera() {
        // カメラストリームを停止
        if (mediaStream) {
            mediaStream.getTracks().forEach(track => track.stop());
        }
        // カメラ要素を非表示にし、カメラを開くボタンを再表示
        camera.style.display = 'none';
        openCameraButton.style.display = 'inline';
        takePhotoButton.style.display = 'none';
        cancelCameraButton.style.display = 'none';
        confirmPhotoButton.style.display = 'none';
        retakePhotoButton.style.display = 'none';

        // 写真が撮影されていれば、キャプチャした写真とキャンバスを隠し、再びカメラを表示
        if (isCaptured) {
            capturedPhoto.style.display = 'none';
            canvas.style.display = 'none';
            isCaptured = false;
        }
    }

    // 撮影処理を関数にまとめる
    function takePhoto() {
        // 写真を撮影
        context.drawImage(camera, 0, 0, canvas.width, canvas.height);
        takePhotoButton.style.display = 'none';
        retakePhotoButton.style.display = 'inline';
        confirmPhotoButton.style.display = 'inline';
        capturedPhoto.style.display = 'none';
        canvas.style.display = 'block';
        isCaptured = true;
    }

    // 撮り直し処理を関数にまとめる
    function retakePhoto() {
        // 撮り直し
        takePhotoButton.style.display = 'inline';
        retakePhotoButton.style.display = 'none';
        confirmPhotoButton.style.display = 'none';
        capturedPhoto.style.display = 'none';
        canvas.style.display = 'none';

        // カメラを再表示
        camera.style.display = 'block';
        isCaptured = false; // 写真がキャプチャされていない状態に戻す
    }

    // 確認処理を関数にまとめる
    function confirmPhoto() {
        // カメラストリームを停止
        if (mediaStream) {
            mediaStream.getTracks().forEach(track => track.stop());
        }

        // 写真を確認して保存
        const photoDataURL = canvas.toDataURL('image/jpeg');
        photoInput.value = photoDataURL;
        const fileName = 'photo_' + new Date().toISOString().replace(/:/g, '-') + '.jpeg';
        const blob = dataURLtoBlob(photoDataURL);
        const url = window.URL.createObjectURL(blob);

        // ファイルをダウンロード
        const a = document.createElement('a');
        a.href = url;
        a.download = fileName;
        a.style.display = 'none';
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);

        // 撮影した写真を表示
        capturedPhoto.src = photoDataURL;
        capturedPhoto.style.display = 'block';
        canvas.style.display = 'none';

        retakePhotoButton.style.display = 'none';
        confirmPhotoButton.style.display = 'none';
        takePhotoButton.style.display = 'inline';
        isCaptured = true; // 写真がキャプチャされた状態に設定
        camera.style.display = 'none'; // カメラを非表示にする

        // カメラ画面を非表示にする
        camera.style.display = 'none';
        alert('写真を撮影しました。フォームにアップロードしてください。');
    }

    // Data URL を Blob に変換する関数
    function dataURLtoBlob(dataURL) {
        const arr = dataURL.split(',');
        const mime = arr[0].match(/:(.*?);/)[1];
        const byteString = atob(arr[1]);
        const arrayBuffer = new ArrayBuffer(byteString.length);
        const int8Array = new Uint8Array(arrayBuffer);

        for (let i = 0; i < byteString.length; i++) {
            int8Array[i] = byteString.charCodeAt(i);
        }

        return new Blob([int8Array], { type: mime });
    }

   // UUIDを生成する関数
function generateUUID() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = Math.random() * 16 | 0, v = c === 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}

// フォームの送信時の処理
const itemForm = document.getElementById('itemForm');
itemForm.addEventListener('submit', async function (event) {
    event.preventDefault();

    const formData = new FormData(itemForm);

    if (isCaptured) {
        const photoDataURL = canvas.toDataURL('image/jpeg');
        const photoBlob = dataURLtoBlob(photoDataURL);
        const randomFileName = generateUUID() + '.jpeg'; // ランダムなファイル名を生成
        formData.append('photo', new File([photoBlob], randomFileName, { type: 'image/jpeg' }));
    } else {
        const fileInput = document.getElementById('写真');
        if (fileInput.files[0]) {
            formData.append('photo', fileInput.files[0]);
        }
    }

    try {
        const response = await fetch('/api/add_item', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (data.error) {
            console.error('エラー:', data.error);
        } else {
            console.log('物品が正常に登録されました。');
        }
    } catch (error) {
        console.error('エラー:', error);
    }
});

    // カメラを開くボタンのクリックイベントリスナー
    openCameraButton.addEventListener('click', function () {
        openCamera();
    });

    // キャンセルボタンのクリックイベントリスナー
    cancelCameraButton.addEventListener('click', function () {
        cancelCamera();
    });

    // 撮影ボタンのクリックイベントリスナー
    takePhotoButton.addEventListener('click', function () {
        takePhoto();
    });

    // 撮り直しボタンのクリックイベントリスナー
    retakePhotoButton.addEventListener('click', function () {
        retakePhoto();
    });

    // 確認ボタンのクリックイベントリスナー
    confirmPhotoButton.addEventListener('click', function () {
        confirmPhoto();
    });
});