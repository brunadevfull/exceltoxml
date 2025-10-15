using System.Linq;
using ClosedXML.Excel;
using ExcelXml.Core.Models;
using ExcelXml.Core.Services;
using Xunit;

namespace ExcelXml.Core.Tests;

public class ExcelProcessorTests : IDisposable
{
    private readonly string _tempFile;

    public ExcelProcessorTests()
    {
        _tempFile = Path.Combine(Path.GetTempPath(), Guid.NewGuid() + ".xlsx");
    }

    [Fact]
    public void ProcessFile_ReturnsValidAndInvalidRecords()
    {
        using (var workbook = new XLWorkbook())
        {
            var worksheet = workbook.AddWorksheet("Comandos");
            worksheet.Cell(1, 1).Value = "matricula";
            worksheet.Cell(1, 2).Value = "rubrica";
            worksheet.Cell(1, 3).Value = "valor";
            worksheet.Cell(1, 4).Value = "tipo";
            worksheet.Cell(1, 5).Value = "trigrama";

            worksheet.Cell(2, 1).Value = "10024450";
            worksheet.Cell(2, 2).Value = "1208000";
            worksheet.Cell(2, 3).Value = "12000,00";
            worksheet.Cell(2, 4).Value = "no";
            worksheet.Cell(2, 5).Value = "baa";

            worksheet.Cell(3, 1).Value = "ABCDE";
            worksheet.Cell(3, 2).Value = "1208000";
            worksheet.Cell(3, 3).Value = "ABC";
            worksheet.Cell(3, 4).Value = "XX";
            worksheet.Cell(3, 5).Value = "BA";

            workbook.SaveAs(_tempFile);
        }

        var processor = new ExcelProcessor();
        var records = processor.ProcessFile(_tempFile);

        Assert.Equal(2, records.Count);

        var valid = records.First(r => r.IsValid);
        Assert.Equal("10024450", valid.Matricula);
        Assert.Equal("1208000", valid.Rubrica);
        Assert.Equal("12000.00", valid.ValorFormatado);
        Assert.Equal("NO", valid.Tipo);
        Assert.Equal("BAA", valid.Trigrama);

        var invalid = records.First(r => !r.IsValid);
        Assert.Contains("Matrícula deve conter apenas números", invalid.Error);
    }

    public void Dispose()
    {
        if (File.Exists(_tempFile))
        {
            File.Delete(_tempFile);
        }
    }
}
