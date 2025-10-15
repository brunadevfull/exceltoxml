using System.Collections.Generic;
using System.Linq;
using ExcelXml.Core.Models;
using ExcelXml.Core.Services;
using Xunit;

namespace ExcelXml.Core.Tests;

public class DataManagerTests : IDisposable
{
    private readonly string _tempDirectory;

    public DataManagerTests()
    {
        _tempDirectory = Path.Combine(Path.GetTempPath(), Guid.NewGuid().ToString("N"));
    }

    [Fact]
    public void Constructor_CreatesDefaultConfiguration()
    {
        var manager = new DataManager(_tempDirectory);

        var configPath = Path.Combine(_tempDirectory, "config.json");
        Assert.True(File.Exists(configPath));

        var responsibles = manager.GetResponsibles();
        Assert.Single(responsibles);
        Assert.Equal("RESPONSÁVEL PADRÃO", responsibles.First().Nome);
    }

    [Fact]
    public void AddResponsible_PersistsNewResponsible()
    {
        var manager = new DataManager(_tempDirectory);
        var responsible = new Responsible
        {
            Nome = "Fulano de Tal",
            Cpf = "529.982.247-25",
            Nip = "12345",
            Perfil = "AGI",
            TipoPerfilOm = "IQM"
        };

        manager.AddResponsible(responsible);

        var responsibles = manager.GetResponsibles();
        Assert.Equal(2, responsibles.Count);
        Assert.Contains(responsibles, r => r.Cpf == "52998224725" && r.Nome == "FULANO DE TAL");
    }

    [Fact]
    public void RemoveResponsible_MarksResponsibleAsInactive()
    {
        var manager = new DataManager(_tempDirectory);
        var responsible = new Responsible
        {
            Nome = "Ciclano",
            Cpf = "390.533.447-05",
            Nip = "54321",
            Perfil = "AGI",
            TipoPerfilOm = "IQM"
        };

        manager.AddResponsible(responsible);
        var added = manager.GetResponsibles().First(r => r.Cpf == "39053344705");

        manager.RemoveResponsible(added.Id!.Value);

        var active = manager.GetResponsibles();
        Assert.DoesNotContain(active, r => r.Cpf == "39053344705");
    }

    [Fact]
    public void SaveConfig_RetainsOnlyTenBackups()
    {
        var manager = new DataManager(_tempDirectory);
        var generated = new HashSet<string>();
        for (var i = 0; i < 12; i++)
        {
            var seed = i + 2;
            string cpf;
            do
            {
                cpf = GenerateCpf(seed++);
            }
            while (!generated.Add(cpf));

            var responsible = new Responsible
            {
                Nome = $"Responsavel {i}",
                Cpf = cpf,
                Nip = "00000",
                Perfil = "AGI",
                TipoPerfilOm = "IQM"
            };

            manager.AddResponsible(responsible);
        }

        var backupDirectory = Path.Combine(_tempDirectory, "backups");
        var backups = Directory.Exists(backupDirectory)
            ? Directory.GetFiles(backupDirectory, "config_backup_*.json")
            : Array.Empty<string>();

        Assert.True(backups.Length <= 10);
    }

    private static string GenerateCpf(int seed)
    {
        var digits = new int[9];
        var current = seed;
        for (var i = 0; i < 9; i++)
        {
            digits[i] = current % 10;
            current = (current * 3 + 7) % 100;
        }

        if (digits.All(d => d == digits[0]))
        {
            digits[0] = (digits[0] + 1) % 10;
        }

        var cpfDigits = new List<int>(digits);
        cpfDigits.Add(CalculateDigit(cpfDigits, 10));
        cpfDigits.Add(CalculateDigit(cpfDigits, 11));
        return string.Concat(cpfDigits.Select(d => d.ToString()));
    }

    private static int CalculateDigit(IReadOnlyList<int> digits, int factor)
    {
        var sum = 0;
        for (var i = 0; i < digits.Count; i++)
        {
            sum += digits[i] * (factor - i);
        }

        var remainder = sum % 11;
        return remainder < 2 ? 0 : 11 - remainder;
    }

    public void Dispose()
    {
        if (Directory.Exists(_tempDirectory))
        {
            Directory.Delete(_tempDirectory, recursive: true);
        }
    }
}
