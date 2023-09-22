const searchInput = document.getElementById('search');
const searchSuggestions = document.getElementById('searchSuggestions');
const suggestionList = document.getElementById('suggestionList');
const searchHistory = document.getElementById('searchHistory');
const openHistoryButton = document.getElementById('openHistoryButton');
const historyModal = document.getElementById('historyModal');
const closeHistoryButton = document.getElementById('closeHistoryButton');
const clearHistoryButton = document.getElementById('clearHistoryButton');
let suggestions = []; // Array de sugestões da tabela


clearHistoryButton.addEventListener('click', () => {
    confirmationMessage.classList.remove('hidden'); // Mostra a mensagem de confirmação
});

confirmDeleteButton.addEventListener('click', () => {
    clearSearchHistory(); // Limpa o histórico de pesquisa
    confirmationMessage.classList.add('hidden'); // Oculta a mensagem de confirmação
});

cancelDeleteButton.addEventListener('click', () => {
    confirmationMessage.classList.add('hidden'); // Oculta a mensagem de confirmação
});
document.getElementById('confirmDeleteButton').addEventListener('click', () => {
    clearSearchHistory();
    showSuccessMessage();
});

function showSuccessMessage() {
    const successMessage = document.getElementById('successMessage');
    successMessage.classList.remove('hidden');

    setTimeout(() => {
        successMessage.classList.add('hidden');
    }, 3000); // Esconde a mensagem de sucesso após 3 segundos (ajustado para 3 segundos)
}

// Verifica se o histórico já foi limpado antes
const hasHistoryCleared = localStorage.getItem('historyCleared');

// Se o histórico já foi limpado antes, esconde a mensagem de sucesso
if (hasHistoryCleared) {
    const successMessage = document.getElementById('successMessage');
    successMessage.classList.add('hidden');
}

clearHistoryButton.addEventListener('click', () => {
    // Se o histórico já foi limpado antes, não faz nada
    if (hasHistoryCleared) {
        return;
    }

    // Caso contrário, exibe a mensagem de sucesso e define que o histórico já foi limpado
    showSuccessMessage();
    localStorage.setItem('historyCleared', 'true');
});

function clearSearchHistory() {
    localStorage.removeItem('searchHistory'); // Remove o histórico do localStorage
    searchHistory.innerHTML = ''; // Limpa a lista de histórico exibida na página
    hideHistoryModal(); // Fecha o modal de histórico de pesquisa
}

// Extrai sugestões da tabela
const tableRows = document.querySelectorAll('table tbody tr');
tableRows.forEach(row => {
    const campo = row.querySelector('td:nth-child(1)').textContent.trim();
    const descricao = row.querySelector('td:nth-child(2)').textContent.trim();
    suggestions.push(`${campo} - ${descricao}`);
});

searchInput.addEventListener('input', () => {
    displaySearchSuggestions();
});

searchInput.addEventListener('click', () => {
    displaySearchSuggestions();
});

searchInput.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
        event.preventDefault(); // Impede que o formulário seja enviado, se houver algum
        const query = searchInput.value.trim();
        if (query !== '') {
            addToSearchHistory(query);
            scrollToTableRow(query);
        }
        searchInput.value = ''; // Limpa o valor da barra de pesquisa
        searchSuggestions.classList.add('hidden'); // Fecha a barra de sugestões ao pressionar Enter
    } else if (event.key === 'Tab' && suggestions.length > 0) {
        event.preventDefault(); // Impede o comportamento padrão da tecla "TAB"
        const selectedSuggestion = suggestionList.querySelector('li.active');
        if (!selectedSuggestion) {
            // Se nenhuma sugestão estiver selecionada, selecione a primeira sugestão
            suggestionList.firstChild.classList.add('active');
            searchInput.value = suggestionList.firstChild.textContent; // Preenche a barra de pesquisa com a primeira sugestão
        } else {
            // Desselecione a sugestão atual
            selectedSuggestion.classList.remove('active');
            // Encontre a próxima sugestão
            const nextSuggestion = selectedSuggestion.nextSibling;
            if (nextSuggestion) {
                // Se houver uma próxima sugestão, selecione-a
                nextSuggestion.classList.add('active');
                searchInput.value = nextSuggestion.textContent; // Preenche a barra de pesquisa com a sugestão selecionada
            } else {
                // Se não houver próxima sugestão, selecione a primeira sugestão
                suggestionList.firstChild.classList.add('active');
                searchInput.value = suggestionList.firstChild.textContent; // Preenche a barra de pesquisa com a primeira sugestão
            }
        }
    }
});

// Adicione um evento de escuta para desativar a sugestão selecionada ao clicar em qualquer lugar da página
document.addEventListener('click', () => {
    const selectedSuggestion = suggestionList.querySelector('li.active');
    if (selectedSuggestion) {
        selectedSuggestion.classList.remove('active');
    }
});

function scrollToTableRow(query) {
    const tableRow = document.getElementById(query);
    if (tableRow) {
        tableRow.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}
openHistoryButton.addEventListener('click', () => {
    showHistoryModal();
});

closeHistoryButton.addEventListener('click', () => {
    hideHistoryModal();
});


function displaySearchSuggestions() {
    const userQuery = searchInput.value.toLowerCase();
    suggestionList.innerHTML = '';

    if (userQuery === '') {
        searchSuggestions.classList.add('hidden');
        return;
    }

    let found = false;

    suggestions.forEach(suggestion => {
        const suggestionLC = suggestion.toLowerCase();
        if (suggestionLC.includes(userQuery)) {
            found = true;
            const li = document.createElement('li');
            const highlightedSuggestion = highlightMatch(suggestion, userQuery);
            li.innerHTML = highlightedSuggestion;
            li.addEventListener('click', () => {
                searchInput.value = suggestion; // Preenche a barra de pesquisa com a sugestão completa
                searchSuggestions.classList.add('hidden'); // Esconde as sugestões
                searchInput.focus(); // Move o foco de volta para a barra de pesquisa
        });
            suggestionList.appendChild(li);
        }
    });

    if (!found) {
        searchSuggestions.classList.add('hidden');
        return;
    }

    searchSuggestions.classList.remove('hidden');
}


function highlightMatch(suggestion, query) {
    const regex = new RegExp(`(${query})`, 'gi');
    return suggestion.replace(regex, '<span class="bg-yellow-300">$1</span>');
}

function addToSearchHistory(query) {
    const now = new Date();
    const formattedDate = now.toLocaleDateString(); // Apenas a data, sem a hora

    const historyItem = {
        query: query,
        date: formattedDate,
    };

    const history = JSON.parse(localStorage.getItem('searchHistory')) || [];
    history.push(historyItem);
    localStorage.setItem('searchHistory', JSON.stringify(history));

    const li = document.createElement('li');
    li.textContent = `${formattedDate}: ${query}`;
    searchHistory.appendChild(li);
}

function showHistoryModal() {
    historyModal.classList.remove('hidden');
}

function hideHistoryModal() {
    historyModal.classList.add('hidden');
}

// Recupera e exibe o histórico de pesquisa ao carregar a página
const savedHistory = JSON.parse(localStorage.getItem('searchHistory')) || [];
savedHistory.forEach(historyItem => {
    const li = document.createElement('li');
    li.textContent = `${historyItem.date}: ${historyItem.query}`;
    searchHistory.appendChild(li);
});