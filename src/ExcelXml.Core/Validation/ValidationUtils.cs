using System.Globalization;
using System.Text;
using System.Linq;

namespace ExcelXml.Core.Validation;

public static class ValidationUtils
{
    public static string CleanCpf(string? cpf)
    {
        if (string.IsNullOrWhiteSpace(cpf))
        {
            return string.Empty;
        }

        var builder = new StringBuilder(cpf.Length);
        foreach (var ch in cpf)
        {
            if (char.IsDigit(ch))
            {
                builder.Append(ch);
            }
        }

        return builder.ToString();
    }

    public static bool IsValidCpf(string? cpf)
    {
        var digits = CleanCpf(cpf);
        if (digits.Length != 11)
        {
            return false;
        }

        if (digits.All(c => c == digits[0]))
        {
            return false;
        }

        var sum1 = 0;
        for (var i = 0; i < 9; i++)
        {
            sum1 += (digits[i] - '0') * (10 - i);
        }

        var remainder1 = sum1 % 11;
        var digit1 = remainder1 < 2 ? 0 : 11 - remainder1;
        if (digits[9] - '0' != digit1)
        {
            return false;
        }

        var sum2 = 0;
        for (var i = 0; i < 10; i++)
        {
            sum2 += (digits[i] - '0') * (11 - i);
        }

        var remainder2 = sum2 % 11;
        var digit2 = remainder2 < 2 ? 0 : 11 - remainder2;
        return digits[10] - '0' == digit2;
    }

    public static bool IsValidFolha(string? folha)
    {
        if (string.IsNullOrWhiteSpace(folha) || folha.Length != 6)
        {
            return false;
        }

        if (!folha.All(char.IsDigit))
        {
            return false;
        }

        var month = int.Parse(folha[..2], CultureInfo.InvariantCulture);
        var year = int.Parse(folha[2..], CultureInfo.InvariantCulture);

        if (month < 1 || month > 12)
        {
            return false;
        }

        return year is >= 2000 and <= 2100;
    }

    public static bool IsValidMatricula(string? matricula)
    {
        if (string.IsNullOrWhiteSpace(matricula))
        {
            return false;
        }

        if (!matricula.All(char.IsDigit))
        {
            return false;
        }

        var length = matricula.Length;
        return length >= 6 && length <= 10;
    }

    public static bool IsValidRubrica(string? rubrica)
    {
        if (string.IsNullOrWhiteSpace(rubrica))
        {
            return false;
        }

        return rubrica.Length == 7 && rubrica.All(char.IsDigit);
    }

    public static bool TryParseValor(string? valor, out decimal parsed)
    {
        parsed = 0m;
        if (string.IsNullOrWhiteSpace(valor))
        {
            return false;
        }

        var normalized = valor.Replace(',', '.');
        if (!decimal.TryParse(normalized, NumberStyles.Number, CultureInfo.InvariantCulture, out parsed))
        {
            return false;
        }

        return parsed >= 0m;
    }

    public static bool IsValidTipo(string? tipo)
    {
        if (string.IsNullOrWhiteSpace(tipo))
        {
            return false;
        }

        var upper = tipo.Trim().ToUpperInvariant();
        return upper is "NO" or "DE";
    }

    public static bool IsValidTrigrama(string? trigrama)
    {
        if (string.IsNullOrWhiteSpace(trigrama))
        {
            return false;
        }

        var trimmed = trigrama.Trim();
        return trimmed.Length == 3 && trimmed.All(char.IsLetter);
    }
}
