using System.Linq;
using ClosedXML.Excel;
using ExcelXml.Core.Models;
using ExcelXml.Core.Validation;

namespace ExcelXml.Core.Services;

public class ExcelProcessor
{
    private static readonly string[] RequiredColumns = { "matricula", "rubrica", "valor", "tipo", "trigrama" };

    public IReadOnlyList<CommandRecord> ProcessFile(string filePath)
    {
        if (string.IsNullOrWhiteSpace(filePath))
        {
            throw new ArgumentException("Caminho do arquivo é obrigatório", nameof(filePath));
        }

        if (!File.Exists(filePath))
        {
            throw new FileNotFoundException("Arquivo não encontrado", filePath);
        }

        using var workbook = new XLWorkbook(filePath);
        var worksheet = workbook.Worksheets.FirstOrDefault(ws => ws.RowsUsed().Any());
        if (worksheet is null)
        {
            throw new InvalidOperationException("Planilha não possui dados");
        }

        var headerMap = BuildHeaderMap(worksheet);
        ValidateColumns(headerMap);

        var results = new List<CommandRecord>();
        foreach (var row in worksheet.RowsUsed().Skip(1))
        {
            if (IsRowEmpty(row, headerMap))
            {
                continue;
            }

            var record = ProcessRow(row, headerMap);
            results.Add(record);
        }

        return results;
    }

    private static Dictionary<string, int> BuildHeaderMap(IXLWorksheet worksheet)
    {
        var headerRow = worksheet.Row(1);
        var map = new Dictionary<string, int>(StringComparer.OrdinalIgnoreCase);
        foreach (var cell in headerRow.CellsUsed())
        {
            var header = cell.GetFormattedString().Trim();
            if (string.IsNullOrEmpty(header))
            {
                continue;
            }

            header = header.ToLowerInvariant();
            if (!map.ContainsKey(header))
            {
                map.Add(header, cell.Address.ColumnNumber);
            }
        }

        return map;
    }

    private static void ValidateColumns(Dictionary<string, int> headerMap)
    {
        var missing = RequiredColumns.Where(column => !headerMap.ContainsKey(column)).ToList();
        if (missing.Count > 0)
        {
            throw new InvalidOperationException($"Colunas obrigatórias ausentes: {string.Join(", ", missing)}");
        }
    }

    private static bool IsRowEmpty(IXLRow row, Dictionary<string, int> headerMap)
    {
        return headerMap.Values.All(col => string.IsNullOrWhiteSpace(row.Cell(col).GetFormattedString()));
    }

    private static CommandRecord ProcessRow(IXLRow row, Dictionary<string, int> headerMap)
    {
        var record = new CommandRecord
        {
            LineNumber = row.RowNumber()
        };

        var matriculaRaw = row.Cell(headerMap["matricula"]).GetFormattedString().Trim();
        var rubricaRaw = row.Cell(headerMap["rubrica"]).GetFormattedString().Trim();
        var valorRaw = row.Cell(headerMap["valor"]).GetFormattedString().Trim();
        var tipoRaw = row.Cell(headerMap["tipo"]).GetFormattedString().Trim();
        var trigramaRaw = row.Cell(headerMap["trigrama"]).GetFormattedString().Trim();

        try
        {
            var matricula = NormalizeToken(matriculaRaw);
            var rubrica = NormalizeToken(rubricaRaw);
            var valorTexto = valorRaw.Replace(" ", string.Empty);
            var tipo = tipoRaw.ToUpperInvariant();
            var trigrama = trigramaRaw.ToUpperInvariant();

            if (string.IsNullOrWhiteSpace(matricula) || string.Equals(matricula, "nan", StringComparison.OrdinalIgnoreCase))
            {
                throw new InvalidOperationException("Matrícula é obrigatória");
            }

            if (!ValidationUtils.IsValidMatricula(matricula))
            {
                throw new InvalidOperationException("Matrícula deve conter apenas números");
            }

            if (string.IsNullOrWhiteSpace(rubrica) || string.Equals(rubrica, "nan", StringComparison.OrdinalIgnoreCase))
            {
                throw new InvalidOperationException("Rubrica é obrigatória");
            }

            if (!ValidationUtils.IsValidRubrica(rubrica))
            {
                throw new InvalidOperationException("Rubrica deve conter 7 dígitos");
            }

            if (string.IsNullOrWhiteSpace(valorTexto) || string.Equals(valorTexto, "nan", StringComparison.OrdinalIgnoreCase))
            {
                throw new InvalidOperationException("Valor é obrigatório");
            }

            if (!ValidationUtils.TryParseValor(valorTexto, out var valor))
            {
                throw new InvalidOperationException("Valor deve ser um número válido");
            }

            if (!ValidationUtils.IsValidTipo(tipo))
            {
                throw new InvalidOperationException($"Tipo deve ser NO ou DE, encontrado: {tipo}");
            }

            if (!ValidationUtils.IsValidTrigrama(trigrama))
            {
                throw new InvalidOperationException("Trigrama deve conter 3 caracteres");
            }

            record.Matricula = matricula;
            record.Rubrica = rubrica;
            record.Valor = Math.Round(valor, 2);
            record.Tipo = tipo;
            record.Trigrama = trigrama;
            record.IsValid = true;
        }
        catch (Exception ex)
        {
            record.Matricula = matriculaRaw;
            record.Rubrica = rubricaRaw;
            record.Valor = null;
            record.Tipo = tipoRaw;
            record.Trigrama = trigramaRaw;
            record.IsValid = false;
            record.Error = ex.Message;
        }

        return record;
    }

    private static string NormalizeToken(string value)
    {
        return value?.Trim() ?? string.Empty;
    }
}
