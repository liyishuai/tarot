let currentSpread = null;
let drawnCards = [];

function showStep(stepNumber) {
    document.querySelectorAll('.step').forEach(el => el.classList.remove('active'));
    document.getElementById(`step${stepNumber}`).classList.add('active');
}

async function startReading() {
    const question = document.getElementById('questionInput').value.trim();
    if (!question) {
        alert('请输入您的问题');
        return;
    }

    document.getElementById('loading1').classList.remove('hidden');
    
    try {
        const response = await fetch('/api/start_reading', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({question})
        });

        const data = await response.json();
        
        document.getElementById('loading1').classList.add('hidden');
        
        // 显示对话
        const dialogSection = document.getElementById('dialogSection');
        dialogSection.innerHTML += `<div class="dialog-message user">您的问题：${question}</div>`;
        dialogSection.innerHTML += `<div class="dialog-message assistant">${data.response}</div>`;

        if (data.has_spread && data.spread) {
            showSpreadRecommendation(data.spread);
        }

        showStep(2);
    } catch (error) {
        document.getElementById('loading1').classList.add('hidden');
        alert('发生错误：' + error.message);
    }
}

function showSpreadRecommendation(spread) {
    currentSpread = spread;
    
    document.getElementById('spreadName').textContent = spread.name;
    document.getElementById('spreadDescription').textContent = spread.description;
    
    const positionsList = document.getElementById('spreadPositionsList');
    positionsList.innerHTML = spread.positions.map((pos, i) => `
        <div class="position-item">
            <strong>${i + 1}. ${pos.name}</strong>: ${pos.meaning}
        </div>
    `).join('');
    
    document.getElementById('spreadRecommendation').classList.remove('hidden');
}

async function acceptSpread() {
    if (!currentSpread) return;
    
    // 设置牌阵布局
    setupSpreadLayout();
    showStep(3);
}

async function requestNewSpread() {
    const feedback = prompt('请告诉我您想要什么样的牌阵：');
    if (!feedback) return;

    document.getElementById('loading1').classList.remove('hidden');
    
    try {
        const response = await fetch('/api/request_new_spread', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({feedback})
        });

        const data = await response.json();
        
        document.getElementById('loading1').classList.add('hidden');
        
        if (data.spread) {
            // 清空旧的推荐
            document.getElementById('spreadRecommendation').classList.add('hidden');
            
            // 添加对话
            const dialogSection = document.getElementById('dialogSection');
            dialogSection.innerHTML += `<div class="dialog-message user">${feedback}</div>`;
            dialogSection.innerHTML += `<div class="dialog-message assistant">${data.response}</div>`;
            
            // 显示新推荐
            showSpreadRecommendation(data.spread);
        }
    } catch (error) {
        document.getElementById('loading1').classList.add('hidden');
        alert('发生错误：' + error.message);
    }
}

function setupSpreadLayout() {
    if (!currentSpread) return;
    
    const layout = document.getElementById('spreadLayout');
    layout.innerHTML = '';
    
    currentSpread.positions.forEach((pos, index) => {
        const coord = currentSpread.layout[index];
        const posDiv = document.createElement('div');
        posDiv.className = 'card-position';
        posDiv.style.left = coord.x + '%';
        posDiv.style.top = coord.y + '%';
        posDiv.innerHTML = `
            <div style="font-weight: bold; margin-bottom: 5px;">${index + 1}</div>
            <div style="font-size: 10px;">${pos.name}</div>
        `;
        posDiv.dataset.index = index;
        layout.appendChild(posDiv);
    });
}

async function drawCards() {
    document.getElementById('loading2').classList.remove('hidden');
    
    try {
        const response = await fetch('/api/draw_cards', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'}
        });

        const data = await response.json();
        drawnCards = data.cards;
        
        document.getElementById('loading2').classList.add('hidden');
        
        // 更新牌阵显示
        const positions = document.querySelectorAll('.card-position');
        drawnCards.forEach((card, index) => {
            positions[index].classList.add('filled');
            positions[index].innerHTML = `
                <div style="font-weight: bold; font-size: 11px; margin-bottom: 5px;">${card.card}</div>
                <div style="font-size: 9px;">${card.orientation}</div>
            `;
        });
        
        // 显示牌义
        showCardMeanings();
        showStep(4);
    } catch (error) {
        document.getElementById('loading2').classList.add('hidden');
        alert('发生错误：' + error.message);
    }
}

function showCardMeanings() {
    const meaningsDiv = document.getElementById('cardMeanings');
    meaningsDiv.innerHTML = '<h3>📋 每张牌的含义</h3>';
    
    drawnCards.forEach((card, index) => {
        meaningsDiv.innerHTML += `
            <div class="card-meaning-item">
                <h4>${index + 1}. ${card.position}：${card.card} (${card.orientation})</h4>
                <p><strong>位置含义：</strong>${card.position_meaning}</p>
                <p><strong>关键词：</strong>${card.keywords}</p>
                <p><strong>牌义：</strong>${card.meaning}</p>
            </div>
        `;
    });
}

async function getInterpretation() {
    document.getElementById('loading3').classList.remove('hidden');
    
    try {
        const response = await fetch('/api/get_interpretation', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'}
        });

        const data = await response.json();
        
        document.getElementById('loading3').classList.add('hidden');
        
        const interpretationDiv = document.getElementById('interpretation');
        document.getElementById('interpretationText').innerHTML = data.interpretation.replace(/\n/g, '<br>');
        interpretationDiv.classList.remove('hidden');
        
        // 滚动到解读
        interpretationDiv.scrollIntoView({behavior: 'smooth'});
    } catch (error) {
        document.getElementById('loading3').classList.add('hidden');
        alert('发生错误：' + error.message);
    }
}
