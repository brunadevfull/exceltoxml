using System.Globalization;

namespace ExcelXml.Core.Models;

public class CommandRecord
{
    public string Matricula { get; set; } = string.Empty;

    public string Rubrica { get; set; } = string.Empty;

    public decimal? Valor { get; set; }

    public string Tipo { get; set; } = string.Empty;

    public string Trigrama { get; set; } = string.Empty;

    public int LineNumber { get; set; }

    public bool IsValid { get; set; }

    public string? Error { get; set; }

    public string ValorFormatado => Valor?.ToString("F2", CultureInfo.InvariantCulture) ?? string.Empty;

    public CommandRecord Clone() => new()
    {
        Matricula = Matricula,
        Rubrica = Rubrica,
        Valor = Valor,
        Tipo = Tipo,
        Trigrama = Trigrama,
        LineNumber = LineNumber,
        IsValid = IsValid,
        Error = Error
    };
}
