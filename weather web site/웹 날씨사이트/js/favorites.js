// 즐겨찾기 추가 (서버로 데이터 전송)
function addToFavorites(item) {
    fetch('http://your-server-url/favorites', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ item })
    })
    .then(response => response.json())
    .then(data => {
        console.log('즐겨찾기에 추가됨:', data);
    });
}

// 즐겨찾기 불러오기 (서버에서 데이터 가져오기)
function loadFavorites() {
    fetch('http://your-server-url/favorites')
        .then(response => response.json())
        .then(data => {
            console.log('저장된 즐겨찾기 목록:', data);
        });
}

// 페이지 로드 시 즐겨찾기 목록 가져오기
document.addEventListener('DOMContentLoaded', () => {
    loadFavorites();
});
