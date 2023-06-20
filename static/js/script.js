// script.js

// フォーム要素とドロップゾーンを取得
const form = document.getElementById('upload-form');
const dropZone = document.getElementById('drop-zone');

// ドラッグオーバー時のイベントリスナーを設定
dropZone.addEventListener('dragover', (event) => {
  event.preventDefault();
  dropZone.classList.add('dragover');
});

// ドラッグリーブ時のイベントリスナーを設定
dropZone.addEventListener('dragleave', () => {
  dropZone.classList.remove('dragover');
});

// ドロップ時のイベントリスナーを設定
dropZone.addEventListener('drop', (event) => {
  event.preventDefault();
  dropZone.classList.remove('dragover');

  const files = event.dataTransfer.files;
  for (let i = 0; i < files.length; i++) {
    const fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.name = 'image';
    fileInput.accept = 'image/*';
    fileInput.files = files;

    form.appendChild(fileInput);
  }
});

function deleteFile(save_path) {
  // Ajaxリクエストを作成
  const xhr = new XMLHttpRequest();
  xhr.open('POST', '/delete', true);
  xhr.setRequestHeader('Content-Type', 'application/json');

  // レスポンスの処理
  xhr.onload = function() {
    if (xhr.status === 200) {
      // ファイル削除成功
      alert('ファイルを削除しました: ' + save_path);
      // 削除されたファイルの要素をDOMから削除するなどの処理を追加することもできます
    } else {
      // ファイル削除失敗
      alert('ファイルの削除に失敗しました');
    }
  };

  // リクエストの送信
  xhr.send(JSON.stringify({ save_path: save_path }));
}