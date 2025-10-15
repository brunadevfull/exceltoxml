using System;
using System.Collections.ObjectModel;
using System.Collections.Specialized;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using ExcelXml.Core.Models;
using ExcelXml.Core.Services;
using ExcelXml.Core.Validation;
using ExcelXml.Desktop.Services;

namespace ExcelXml.Desktop.ViewModels;

public partial class MainWindowViewModel : ObservableObject
{
    private readonly DataManager _dataManager;
    private readonly ExcelProcessor _excelProcessor;
    private readonly XmlGenerator _xmlGenerator;
    private IFileDialogService? _fileDialogService;

    public MainWindowViewModel(DataManager dataManager, ExcelProcessor excelProcessor, XmlGenerator xmlGenerator)
    {
        _dataManager = dataManager;
        _excelProcessor = excelProcessor;
        _xmlGenerator = xmlGenerator;

        Responsibles = new ObservableCollection<Responsible>();
        Records = new ObservableCollection<CommandRecord>();

        SelectFileCommand = new AsyncRelayCommand(SelectFileAsync, () => !IsBusy && _fileDialogService is not null);
        ProcessExcelCommand = new AsyncRelayCommand(ProcessExcelAsync, CanProcessExcel);
        GenerateXmlCommand = new AsyncRelayCommand(GenerateXmlAsync, CanGenerateXml);

        Records.CollectionChanged += OnRecordsCollectionChanged;

        _ = RefreshResponsiblesAsync();
    }

    public ObservableCollection<Responsible> Responsibles { get; }

    public ObservableCollection<CommandRecord> Records { get; }

    [ObservableProperty]
    [NotifyPropertyChangedFor(nameof(HasValidationMessage))]
    private string? validationMessage;

    [ObservableProperty]
    private string statusMessage = "Selecione um arquivo Excel para iniciar.";

    [ObservableProperty]
    private string? selectedFilePath;

    [ObservableProperty]
    private Responsible? selectedResponsible;

    [ObservableProperty]
    private string folha = string.Empty;

    [ObservableProperty]
    private double progress;

    [ObservableProperty]
    private bool isBusy;

    public bool HasValidationMessage => !string.IsNullOrWhiteSpace(ValidationMessage);

    public bool HasRecords => Records.Count > 0;

    public IAsyncRelayCommand SelectFileCommand { get; }

    public IAsyncRelayCommand ProcessExcelCommand { get; }

    public IAsyncRelayCommand GenerateXmlCommand { get; }

    public void SetDialogService(IFileDialogService dialogService)
    {
        _fileDialogService = dialogService;
        SelectFileCommand.NotifyCanExecuteChanged();
        GenerateXmlCommand.NotifyCanExecuteChanged();
    }

    public Task HandleDroppedFileAsync(string filePath)
    {
        if (string.IsNullOrWhiteSpace(filePath) || !File.Exists(filePath))
        {
            ValidationMessage = "Arquivo inválido.";
            return Task.CompletedTask;
        }

        SelectedFilePath = filePath;
        StatusMessage = $"Arquivo selecionado: {Path.GetFileName(filePath)}";
        ValidationMessage = null;
        ProcessExcelCommand.NotifyCanExecuteChanged();
        return Task.CompletedTask;
    }

    public async Task AddResponsibleAsync(Responsible responsible)
    {
        try
        {
            await Task.Run(() => _dataManager.AddResponsible(responsible));
            await RefreshResponsiblesAsync();
            StatusMessage = $"Responsável {responsible.Nome} cadastrado.";
            ValidationMessage = null;
        }
        catch (Exception ex)
        {
            ValidationMessage = ex.Message;
        }
    }

    public async Task UpdateResponsibleAsync(Responsible responsible)
    {
        if (responsible.Id is null)
        {
            ValidationMessage = "Responsável inválido para atualização.";
            return;
        }

        try
        {
            await Task.Run(() => _dataManager.UpdateResponsible(responsible.Id.Value, responsible));
            await RefreshResponsiblesAsync();
            StatusMessage = $"Responsável {responsible.Nome} atualizado.";
            ValidationMessage = null;
        }
        catch (Exception ex)
        {
            ValidationMessage = ex.Message;
        }
    }

    public Task<Responsible?> GetResponsibleByIdAsync(int id)
    {
        return Task.Run(() => _dataManager.GetResponsibleById(id));
    }

    public async Task RemoveResponsibleAsync(Responsible responsible)
    {
        if (responsible.Id is null)
        {
            return;
        }

        try
        {
            await Task.Run(() => _dataManager.RemoveResponsible(responsible.Id.Value));
            await RefreshResponsiblesAsync();
            StatusMessage = $"Responsável {responsible.Nome} removido.";
            ValidationMessage = null;
        }
        catch (Exception ex)
        {
            ValidationMessage = ex.Message;
        }
    }

    private async Task RefreshResponsiblesAsync()
    {
        var previousId = SelectedResponsible?.Id;
        var responsibles = await Task.Run(() => _dataManager.GetResponsibles().ToList());

        Responsibles.Clear();
        foreach (var responsible in responsibles)
        {
            Responsibles.Add(responsible);
        }

        if (Responsibles.Count == 0)
        {
            SelectedResponsible = null;
            return;
        }

        if (previousId is not null)
        {
            var match = Responsibles.FirstOrDefault(r => r.Id == previousId);
            if (match is not null)
            {
                SelectedResponsible = match;
                return;
            }
        }

        SelectedResponsible = Responsibles[0];
    }

    private bool CanProcessExcel() => !IsBusy && !string.IsNullOrWhiteSpace(SelectedFilePath);

    private bool CanGenerateXml() => !IsBusy && Records.Any(r => r.IsValid) && SelectedResponsible is not null && !string.IsNullOrWhiteSpace(Folha);

    private async Task SelectFileAsync()
    {
        if (_fileDialogService is null)
        {
            return;
        }

        var file = await _fileDialogService.OpenExcelFileAsync();
        if (string.IsNullOrWhiteSpace(file))
        {
            return;
        }

        SelectedFilePath = file;
        StatusMessage = $"Arquivo selecionado: {Path.GetFileName(file)}";
        ValidationMessage = null;
        ProcessExcelCommand.NotifyCanExecuteChanged();
    }

    private async Task ProcessExcelAsync()
    {
        if (string.IsNullOrWhiteSpace(SelectedFilePath))
        {
            ValidationMessage = "Selecione um arquivo Excel.";
            return;
        }

        try
        {
            IsBusy = true;
            Progress = 0;
            ValidationMessage = null;
            StatusMessage = "Processando planilha...";

            var records = await Task.Run(() => _excelProcessor.ProcessFile(SelectedFilePath));
            Progress = 70;

            Records.Clear();
            foreach (var record in records)
            {
                Records.Add(record);
            }

            Progress = 100;
            StatusMessage = $"Processamento concluído. {Records.Count} registros encontrados.";
            GenerateXmlCommand.NotifyCanExecuteChanged();
        }
        catch (Exception ex)
        {
            ValidationMessage = ex.Message;
            StatusMessage = "Erro ao processar planilha.";
            Records.Clear();
        }
        finally
        {
            Progress = 0;
            IsBusy = false;
            ProcessExcelCommand.NotifyCanExecuteChanged();
            GenerateXmlCommand.NotifyCanExecuteChanged();
        }
    }

    private async Task GenerateXmlAsync()
    {
        if (SelectedResponsible is null)
        {
            ValidationMessage = "Selecione um responsável.";
            return;
        }

        if (!ValidationUtils.IsValidFolha(Folha))
        {
            ValidationMessage = "Folha deve estar no formato MMAAAA.";
            return;
        }

        var validRecords = Records.Where(r => r.IsValid).ToList();
        if (validRecords.Count == 0)
        {
            ValidationMessage = "Nenhum registro válido disponível.";
            return;
        }

        if (_fileDialogService is null)
        {
            return;
        }

        try
        {
            IsBusy = true;
            Progress = 0;
            StatusMessage = "Gerando XML...";
            ValidationMessage = null;

            var xmlContent = await Task.Run(() => _xmlGenerator.GenerateXml(validRecords, SelectedResponsible, Folha));
            Progress = 60;

            var suggestedName = $"comandos_{Folha}.xml";
            var destination = await _fileDialogService.SaveXmlFileAsync(suggestedName);
            if (string.IsNullOrWhiteSpace(destination))
            {
                StatusMessage = "Exportação cancelada.";
                return;
            }

            await Task.Run(() => File.WriteAllText(destination, xmlContent, Encoding.GetEncoding("iso-8859-1")));
            Progress = 100;
            StatusMessage = $"XML exportado com sucesso: {Path.GetFileName(destination)}";
        }
        catch (Exception ex)
        {
            ValidationMessage = ex.Message;
            StatusMessage = "Erro ao gerar XML.";
        }
        finally
        {
            Progress = 0;
            IsBusy = false;
            GenerateXmlCommand.NotifyCanExecuteChanged();
            ProcessExcelCommand.NotifyCanExecuteChanged();
        }
    }

    partial void OnIsBusyChanged(bool value)
    {
        SelectFileCommand.NotifyCanExecuteChanged();
        ProcessExcelCommand.NotifyCanExecuteChanged();
        GenerateXmlCommand.NotifyCanExecuteChanged();
    }

    partial void OnSelectedFilePathChanged(string? value)
    {
        ProcessExcelCommand.NotifyCanExecuteChanged();
    }

    partial void OnSelectedResponsibleChanged(Responsible? value)
    {
        GenerateXmlCommand.NotifyCanExecuteChanged();
    }

    partial void OnFolhaChanged(string value)
    {
        GenerateXmlCommand.NotifyCanExecuteChanged();
    }

    private void OnRecordsCollectionChanged(object? sender, NotifyCollectionChangedEventArgs e)
    {
        OnPropertyChanged(nameof(HasRecords));
        GenerateXmlCommand.NotifyCanExecuteChanged();
    }
}
