// Global variables
let selectedFile = null;
let currentFilename = null;

// Initialize page
document.addEventListener('DOMContentLoaded', function() {
    setupDropArea();
    setupFileInput();
});

// Setup drag and drop area
function setupDropArea() {
    const dropArea = document.getElementById('dropArea');
    const fileInput = document.getElementById('fileInput');

    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        dropArea.addEventListener(eventName, highlight, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, unhighlight, false);
    });

    function highlight(e) {
        dropArea.classList.add('dragover');
    }

    function unhighlight(e) {
        dropArea.classList.remove('dragover');
    }

    dropArea.addEventListener('drop', handleDrop, false);
    dropArea.addEventListener('click', () => fileInput.click());

    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        handleFiles(files);
    }
}

// Setup file input
function setupFileInput() {
    const fileInput = document.getElementById('fileInput');
    fileInput.addEventListener('change', function(e) {
        handleFiles(e.target.files);
    });
}

// Handle selected files
function handleFiles(files) {
    if (files.length > 0) {
        const file = files[0];
        if (file.name.match(/\.(xlsx|xls)$/i)) {
            selectedFile = file;
            uploadFile(file);
        } else {
            showStatus('Formato de arquivo não suportado. Use .xlsx ou .xls', 'error');
        }
    }
}

// Select file button
function selectFile() {
    document.getElementById('fileInput').click();
}

// Upload file to server
function uploadFile(file) {
    const formData = new FormData();
    formData.append('file', file);

    showStatus('Enviando arquivo...', 'info');
    showProgress(30);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            currentFilename = data.filename;
            showFileInfo(file.name, data.records, data.preview);
            showStatus(`Arquivo processado com sucesso! ${data.records} registros encontrados.`, 'success');
            updateConvertButton();
        } else {
            showStatus(data.error || 'Erro ao processar arquivo', 'error');
        }
        hideProgress();
    })
    .catch(error => {
        console.error('Error:', error);
        showStatus('Erro de conexão', 'error');
        hideProgress();
    });
}

// Show file information
function showFileInfo(filename, records, preview) {
    const fileInfo = document.getElementById('fileInfo');
    const fileDetails = document.getElementById('fileDetails');
    
    let previewHtml = '';
    if (preview && preview.length > 0) {
        previewHtml = '<h6 class="mt-3">Prévia dos dados:</h6>';
        previewHtml += '<div class="table-responsive"><table class="table table-sm table-bordered">';
        
        // Headers
        previewHtml += '<thead class="table-light"><tr>';
        Object.keys(preview[0]).forEach(key => {
            previewHtml += `<th>${key}</th>`;
        });
        previewHtml += '</tr></thead>';
        
        // Data
        previewHtml += '<tbody>';
        preview.forEach(row => {
            previewHtml += '<tr>';
            Object.values(row).forEach(value => {
                previewHtml += `<td>${value || '-'}</td>`;
            });
            previewHtml += '</tr>';
        });
        previewHtml += '</tbody></table></div>';
    }
    
    fileDetails.innerHTML = `
        <strong>Nome:</strong> ${filename}<br>
        <strong>Registros:</strong> ${records}
        ${previewHtml}
    `;
    
    fileInfo.style.display = 'block';
}

// Convert file to XML
function convertFile() {
    const responsibleId = document.getElementById('responsibleSelect').value;
    const outputFilename = document.getElementById('outputFilename').value;
    const folha = document.getElementById('folha').value;

    if (!currentFilename) {
        showStatus('Selecione um arquivo primeiro', 'error');
        return;
    }

    if (!responsibleId) {
        showStatus('Selecione um responsável', 'error');
        return;
    }

    if (!folha || folha.length !== 6) {
        showStatus('Informe a folha no formato MMAAAA (ex: 012024)', 'error');
        return;
    }

    const data = {
        filename: currentFilename,
        responsible_id: parseInt(responsibleId),
        output_filename: outputFilename,
        folha: folha
    };

    showStatus('Convertendo arquivo...', 'info');
    showProgress(50);

    fetch('/convert', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showStatus(`Conversão concluída! ${data.records_processed} registros processados.`, 'success');
            showDownloadButton(data.xml_filename);
        } else {
            showStatus(data.error || 'Erro na conversão', 'error');
        }
        hideProgress();
    })
    .catch(error => {
        console.error('Error:', error);
        showStatus('Erro de conexão', 'error');
        hideProgress();
    });
}

// Show download button
function showDownloadButton(filename) {
    const statusText = document.getElementById('statusText');
    statusText.innerHTML += `<br><br><a href="/download/${filename}" class="btn btn-success btn-sm">
        <i class="fas fa-download me-1"></i>Baixar XML
    </a>`;
}

// Save new responsible
function saveResponsible() {
    const form = document.getElementById('responsibleForm');
    const formData = new FormData(form);
    
    const data = {
        nome: document.getElementById('nome').value,
        cpf: document.getElementById('cpf').value,
        nip: document.getElementById('nip').value,
        perfil: document.getElementById('perfil').value,
        tipo_perfil_om: document.getElementById('tipoPerfilOm').value,
        cod_papem: document.getElementById('codPapem').value || '094'
    };

    // Basic validation
    if (!data.nome || !data.cpf || !data.nip || !data.perfil || !data.tipo_perfil_om) {
        alert('Preencha todos os campos obrigatórios');
        return;
    }

    if (data.cpf.length !== 11) {
        alert('CPF deve conter 11 dígitos');
        return;
    }

    fetch('/responsibles', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Responsável salvo com sucesso!');
            location.reload(); // Reload to update the lists
        } else {
            alert(data.error || 'Erro ao salvar responsável');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Erro de conexão');
    });
}

// Clear form
function clearForm() {
    selectedFile = null;
    currentFilename = null;
    document.getElementById('fileInfo').style.display = 'none';
    document.getElementById('responsibleSelect').value = '';
    document.getElementById('outputFilename').value = 'comandos_pagamento.xml';
    document.getElementById('folha').value = '';
    hideStatus();
    updateConvertButton();
}

// Update convert button state
function updateConvertButton() {
    const convertBtn = document.getElementById('convertBtn');
    const hasFile = currentFilename !== null;
    const hasResponsible = document.getElementById('responsibleSelect').value !== '';
    const hasFolha = document.getElementById('folha').value.length === 6;
    
    convertBtn.disabled = !(hasFile && hasResponsible && hasFolha);
}

// Show status message
function showStatus(message, type = 'info') {
    const statusPanel = document.getElementById('statusPanel');
    const statusText = document.getElementById('statusText');
    
    let icon = 'fas fa-info-circle';
    let bgColor = '#d1ecf1';
    let borderColor = '#17a2b8';
    
    if (type === 'success') {
        icon = 'fas fa-check-circle';
        bgColor = '#d4edda';
        borderColor = '#28a745';
    } else if (type === 'error') {
        icon = 'fas fa-exclamation-circle';
        bgColor = '#f8d7da';
        borderColor = '#dc3545';
    }
    
    statusPanel.style.backgroundColor = bgColor;
    statusPanel.style.borderLeftColor = borderColor;
    statusText.innerHTML = `<i class="${icon} me-2"></i>${message}`;
    statusPanel.style.display = 'block';
}

// Hide status panel
function hideStatus() {
    document.getElementById('statusPanel').style.display = 'none';
}

// Show progress bar
function showProgress(percent) {
    const progressBar = document.getElementById('progressBar');
    const progressBarInner = progressBar.querySelector('.progress-bar');
    
    progressBarInner.style.width = percent + '%';
    progressBar.style.display = 'block';
}

// Hide progress bar
function hideProgress() {
    document.getElementById('progressBar').style.display = 'none';
}

// Listen for form changes
document.addEventListener('DOMContentLoaded', function() {
    const responsibleSelect = document.getElementById('responsibleSelect');
    const folhaInput = document.getElementById('folha');
    
    responsibleSelect.addEventListener('change', updateConvertButton);
    folhaInput.addEventListener('input', updateConvertButton);
    
    // Format folha input
    folhaInput.addEventListener('input', function(e) {
        let value = e.target.value.replace(/\D/g, '');
        if (value.length > 6) value = value.slice(0, 6);
        e.target.value = value;
        updateConvertButton();
    });
});