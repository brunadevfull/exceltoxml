using System.Runtime.InteropServices;
using System.Text.Encodings.Web;
using System.Text.Json;
using System.Text.Json.Serialization;
using System.Linq;
using ExcelXml.Core.Validation;
using ExcelXml.Core.Models;

namespace ExcelXml.Core.Services;

public class DataManager
{
    private readonly string _configDirectory;
    private readonly string _configFilePath;
    private readonly string _backupDirectory;
    private readonly JsonSerializerOptions _jsonOptions;
    private ConfigurationModel _config;

    public DataManager(string? customDirectory = null)
    {
        _configDirectory = customDirectory ?? ResolveConfigDirectory();
        Directory.CreateDirectory(_configDirectory);

        _backupDirectory = Path.Combine(_configDirectory, "backups");
        Directory.CreateDirectory(_backupDirectory);

        _configFilePath = Path.Combine(_configDirectory, "config.json");

        _jsonOptions = new JsonSerializerOptions
        {
            PropertyNamingPolicy = JsonNamingPolicy.CamelCase,
            WriteIndented = true,
            Encoder = JavaScriptEncoder.UnsafeRelaxedJsonEscaping,
            DefaultIgnoreCondition = JsonIgnoreCondition.WhenWritingNull
        };

        _config = LoadConfig();
    }

    public IReadOnlyCollection<Responsible> GetResponsibles() =>
        _config.Responsaveis
            .Where(r => r.Ativo)
            .Select(CloneResponsible)
            .ToList();

    public Responsible? GetResponsibleById(int id)
    {
        var responsible = _config.Responsaveis.FirstOrDefault(r => r.Id == id && r.Ativo);
        return responsible is null ? null : CloneResponsible(responsible);
    }

    public void AddResponsible(Responsible responsible)
    {
        if (!ValidationUtils.IsValidCpf(responsible.Cpf))
        {
            throw new ArgumentException("CPF inválido", nameof(responsible));
        }

        responsible.Normalize();
        responsible.DataCadastro ??= DateTime.Now;

        if (_config.Responsaveis.Any(r => r.Ativo && r.Cpf == responsible.Cpf))
        {
            throw new InvalidOperationException("CPF já cadastrado");
        }

        var nextId = _config.Responsaveis.Count == 0
            ? 1
            : _config.Responsaveis.Max(r => r.Id ?? 0) + 1;

        responsible.Id = nextId;
        _config.Responsaveis.Add(CloneResponsible(responsible));
        SaveConfig();
    }

    public void UpdateResponsible(int id, Responsible responsible)
    {
        responsible.Normalize();

        var index = _config.Responsaveis.FindIndex(r => r.Id == id);
        if (index == -1)
        {
            throw new KeyNotFoundException("Responsável não encontrado");
        }

        if (_config.Responsaveis
            .Where(r => r.Id != id && r.Ativo)
            .Any(r => r.Cpf == responsible.Cpf))
        {
            throw new InvalidOperationException("CPF já cadastrado");
        }

        responsible.Id = id;
        responsible.DataCadastro ??= _config.Responsaveis[index].DataCadastro ?? DateTime.Now;
        _config.Responsaveis[index] = CloneResponsible(responsible);
        SaveConfig();
    }

    public void RemoveResponsible(int id)
    {
        var responsible = _config.Responsaveis.FirstOrDefault(r => r.Id == id);
        if (responsible is null)
        {
            throw new KeyNotFoundException("Responsável não encontrado");
        }

        responsible.Ativo = false;
        SaveConfig();
    }

    public ConfigurationModel GetConfiguration() => new()
    {
        Versao = _config.Versao,
        UltimaAtualizacao = _config.UltimaAtualizacao,
        Responsaveis = _config.Responsaveis.Select(CloneResponsible).ToList()
    };

    private ConfigurationModel LoadConfig()
    {
        if (File.Exists(_configFilePath))
        {
            try
            {
                var json = File.ReadAllText(_configFilePath);
                var config = JsonSerializer.Deserialize<ConfigurationModel>(json, _jsonOptions);
                if (config is not null)
                {
                    foreach (var responsible in config.Responsaveis)
                    {
                        responsible.Normalize();
                    }

                    return config;
                }
            }
            catch
            {
                // Fallback to default if deserialization fails
            }
        }

        var defaultConfig = CreateDefaultConfig();
        SaveConfig(defaultConfig);
        return defaultConfig;
    }

    private void SaveConfig(ConfigurationModel? config = null)
    {
        var toSave = config ?? _config;
        CreateBackup();

        toSave.UltimaAtualizacao = DateTime.Now;
        var json = JsonSerializer.Serialize(toSave, _jsonOptions);
        File.WriteAllText(_configFilePath, json);

        if (!ReferenceEquals(_config, toSave))
        {
            _config = toSave;
        }
        else
        {
            _config.UltimaAtualizacao = toSave.UltimaAtualizacao;
        }
    }

    private void SaveConfig()
    {
        SaveConfig(_config);
    }

    private void CreateBackup()
    {
        if (!File.Exists(_configFilePath))
        {
            return;
        }

        var timestamp = DateTime.Now.ToString("yyyyMMdd_HHmmss");
        var backupFile = Path.Combine(_backupDirectory, $"config_backup_{timestamp}.json");
        File.Copy(_configFilePath, backupFile, overwrite: true);

        var backups = Directory.GetFiles(_backupDirectory, "config_backup_*.json")
            .OrderBy(File.GetCreationTimeUtc)
            .ToList();

        while (backups.Count > 10)
        {
            var oldest = backups[0];
            File.Delete(oldest);
            backups.RemoveAt(0);
        }
    }

    private Responsible CloneResponsible(Responsible responsible) => new()
    {
        Id = responsible.Id,
        Nome = responsible.Nome,
        Cpf = responsible.Cpf,
        Nip = responsible.Nip,
        Perfil = responsible.Perfil,
        TipoPerfilOm = responsible.TipoPerfilOm,
        CodPapem = responsible.CodPapem,
        Ativo = responsible.Ativo,
        DataCadastro = responsible.DataCadastro
    };

    private ConfigurationModel CreateDefaultConfig()
    {
        var defaultResponsible = new Responsible
        {
            Id = 1,
            Nome = "RESPONSÁVEL PADRÃO",
            Cpf = "00000000000",
            Nip = "00000",
            Perfil = "AGI",
            TipoPerfilOm = "IQM",
            CodPapem = "094",
            Ativo = true,
            DataCadastro = DateTime.Now
        };

        return new ConfigurationModel
        {
            Versao = "2.0",
            UltimaAtualizacao = DateTime.Now,
            Responsaveis = new List<Responsible> { defaultResponsible }
        };
    }

    private string ResolveConfigDirectory()
    {
        if (RuntimeInformation.IsOSPlatform(OSPlatform.Windows))
        {
            var appData = Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData);
            return Path.Combine(appData, "ConversorExcelXML");
        }

        if (RuntimeInformation.IsOSPlatform(OSPlatform.OSX))
        {
            var home = Environment.GetFolderPath(Environment.SpecialFolder.Personal);
            return Path.Combine(home, "Library", "Application Support", "ConversorExcelXML");
        }

        var userProfile = Environment.GetFolderPath(Environment.SpecialFolder.UserProfile);
        return Path.Combine(userProfile, ".config", "conversorexcelxml");
    }
}
