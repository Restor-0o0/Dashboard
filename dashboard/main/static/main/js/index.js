
/*Код для смены тем(определение тем, слушатели на кнопку,сохранение темы в печеньках, перерисовка графиков после смены темы)*/
const btn = document.querySelector('.button-theme');

Them = 'NoThem';
function initialState(themeName) {
    localStorage.setItem('theme',themeName);
    document.documentElement.className = themeName;
    document.cookie = `theme=${themeName}; max-age=31536000; path=/`; // Установка куки с новой темой
    Them = themeName;
    if(themeName == 'dark-theme'){
        btn.textContent = '☽';

    } else{
        btn.textContent = '☀';
    }

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
function toggleTheme(){
    if(localStorage.getItem('theme') == 'dark-theme'){
        initialState('light-theme');
    } else{
        initialState('dark-theme');
    }
}

btn.addEventListener('click', (e) => {
    e.preventDefault();
    toggleTheme()

/*Перерисовка графиков*/

for (var i = 0; i < ChartsArray.length; i++) {
var ctx = document.getElementById('myChart'+i).getContext('2d');
ChartsArray[i].destroy();
ChartsArray[i] = new Chart(ctx, {
type: 'line',
data: {
    labels: labels[i],
    datasets: [{
        label: '',
        data: graph[i],
    }]
},
options: {
    scales: {
        x: {
            ticks: {
                color: getComputedStyle(document.documentElement).getPropertyValue('--text--')
            },
            border: {
                color: getComputedStyle(document.documentElement).getPropertyValue('--text--')
            },
            grid: {
                color: getComputedStyle(document.documentElement).getPropertyValue('--text-2')
            }
        },
        y: {
            ticks: {
                color: getComputedStyle(document.documentElement).getPropertyValue('--text--')
            },
            border: {
                color: getComputedStyle(document.documentElement).getPropertyValue('--text--')
            },
            grid: {
                color: getComputedStyle(document.documentElement).getPropertyValue('--text-2')
            },
            suggestedMin: 15,
            suggestedMax: 40
        }
    }
},
});
}
// Код Chart.js для создания графика

});




/*Скрипт для отображения контейнера с графиком(слушатель нажатий, функции)*/

const divs = document.querySelectorAll('.statistic_');

const body = document.body;
const modal = document.querySelector("#statistic_full");

// при нажатии на кнопку Click me
function btnHandler(e) {
    e.preventDefault();
    body.classList.add("lock"); // блокируем скролл веб-страницы
    modal.classList.add("statistic_full--open"); // открываем модальное окно
}

// при нажатии на кнопку Close
function btnCloseHandler(e) {
    e.preventDefault();
    body.classList.remove("lock"); // разблокируем скролл страницы
    modal.classList.remove("statistic_full--open"); // закрываем окно
    modal.innerHTML = '';

}


divs.forEach(div => {
    div.addEventListener('click', handleClick);
});

function handleClick(e){
    const clickedDivId = this.id;
    const number = parseInt(clickedDivId.slice(1)); // Получить число из строки id
    console.log("Нажали на div с числом:", number);
    e.preventDefault();
    body.classList.add("lock"); // блокируем скролл веб-страницы
    modal.classList.add("statistic_full--open"); // открываем модальное окно

    const newElement = document.createElement('h1');

    // Установить атрибут id и класс
    newElement.id = "h"+number;
    newElement.classList.add('text_');

    modal.appendChild(newElement);

    // Создаем новый дочерний контейнер
    const childContainer = document.createElement('div');
    childContainer.classList.add('graph');

    const canvasElement = document.createElement('canvas');
    canvasElement.classList.add('graph');
    canvasElement.id = `myChart${number}`;
    childContainer.appendChild(canvasElement);

    const scriptElement = document.createElement('script');
    scriptElement.textContent = `
        var element = document.getElementById("h${number}");
        var i = ${number};
        element.textContent = head[i];
        // Код Chart.js для создания графика
        var ctx = document.getElementById('myChart${number}').getContext('2d');
        var myChart${number} = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels[i],
                datasets: [{
                    label: '',
                    data: graph[i],
                }]
            },
            options: {
                scales: {
                    x: {
                        ticks: {
                            color: getComputedStyle(document.documentElement).getPropertyValue('--text--')
                        },
                        border: {
                            color: getComputedStyle(document.documentElement).getPropertyValue('--text--')
                        },
                        grid: {
                            color: getComputedStyle(document.documentElement).getPropertyValue('--text-2')
                        }
                    },
                    y: {
                        ticks: {
                            color: getComputedStyle(document.documentElement).getPropertyValue('--text--')
                        },
                        border: {
                            color: getComputedStyle(document.documentElement).getPropertyValue('--text--')
                        },
                        grid: {
                            color: getComputedStyle(document.documentElement).getPropertyValue('--text-2')
                        },
                        suggestedMin: 15,
                        suggestedMax: 40
                    }
                }
            },
        });
        ChartsArray.push(myChart${number});
    `;
    childContainer.appendChild(scriptElement);

    // Добавляем дочерний контейнер в элемент
    modal.appendChild(childContainer);
    const linkElement = document.createElement('a');
    linkElement.href = '#';
    linkElement.classList.add('btn--close');
    linkElement.classList.add('btn');
    linkElement.textContent = 'Close';
    linkElement.id = 'btn_close';
    linkElement.addEventListener("click", btnCloseHandler);
    // Добавляем элемент <a> в качестве дочернего элемента к div
    modal.appendChild(linkElement);

}
