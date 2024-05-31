Them = 'NoThem';
function initialState(themeName) {
    localStorage.setItem('theme',themeName);
    document.documentElement.className = themeName;
    document.cookie = `theme=${themeName}; max-age=31536000; path=/`; // Установка куки с новой темой
    Them = themeName;


}

const cookies = document.cookie.split(';');

for (let cookie of cookies) {
    const [name, value] = cookie.trim().split('=');
    if (name === 'theme') {
        initialState(value);
    }
}
if (Them === 'NoThem')
{
    initialState('light-theme');
}
