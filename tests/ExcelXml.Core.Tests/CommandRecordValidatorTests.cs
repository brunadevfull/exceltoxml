using System.Linq;
using ExcelXml.Core.Models;
using ExcelXml.Core.Validation;
using Xunit;

namespace ExcelXml.Core.Tests;

public class CommandRecordValidatorTests
{
    [Fact]
    public void Validator_ReturnsSuccess_ForValidRecord()
    {
        var validator = new CommandRecordValidator();
        var record = new CommandRecord
        {
            Matricula = "10024450",
            Rubrica = "1208000",
            Valor = 12000m,
            Tipo = "NO",
            Trigrama = "BAA"
        };

        var result = validator.Validate(record);
        Assert.True(result.IsValid);
    }

    [Fact]
    public void Validator_ReturnsFailure_ForInvalidRecord()
    {
        var validator = new CommandRecordValidator();
        var record = new CommandRecord
        {
            Matricula = "ABC",
            Rubrica = "12080",
            Valor = -10m,
            Tipo = "XX",
            Trigrama = "AB"
        };

        var result = validator.Validate(record);
        Assert.False(result.IsValid);
        Assert.Contains(result.Errors, error => error.ErrorMessage.Contains("Matrícula"));
    }
}
