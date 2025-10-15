using System.Collections.Generic;
using System.Linq;
using System.Xml.Linq;
using ExcelXml.Core.Models;
using ExcelXml.Core.Services;
using Xunit;

namespace ExcelXml.Core.Tests;

public class XmlGeneratorTests
{
    [Fact]
    public void GenerateXml_CreatesExpectedStructure()
    {
        var records = new List<CommandRecord>
        {
            new() { Matricula = "10024450", Rubrica = "1208000", Valor = 12000.00m, Tipo = "NO", Trigrama = "BAA", IsValid = true, LineNumber = 2 },
            new() { Matricula = "10024450", Rubrica = "1210005", Valor = 12000.00m, Tipo = "DE", Trigrama = "BAA", IsValid = true, LineNumber = 3 },
            new() { Matricula = "97115215", Rubrica = "1208000", Valor = 3066.09m, Tipo = "NO", Trigrama = "ZXC", IsValid = true, LineNumber = 4 }
        };

        var responsible = new Responsible
        {
            Nome = "Maria Silva",
            Cpf = "52998224725",
            Nip = "12345",
            Perfil = "AGI",
            TipoPerfilOm = "IQM"
        };

        var generator = new XmlGenerator();
        var xml = generator.GenerateXml(records, responsible, "012025");

        Assert.Contains("<?xml version=\"1.0\" encoding=\"iso-8859-1\" standalone=\"yes\"?>", xml);
        Assert.Contains("<trigrama>BAA</trigrama>", xml);
        Assert.Contains("<trigrama>ZXC</trigrama>", xml);

        var document = XDocument.Parse(xml);
        var commands = document.Descendants("ComandoPagamento").ToList();
        Assert.Equal(3, commands.Count);
        Assert.Equal("1", commands[0].Element("identificador")?.Value);
        Assert.Equal("3", commands[^1].Element("identificador")?.Value);
    }
}
