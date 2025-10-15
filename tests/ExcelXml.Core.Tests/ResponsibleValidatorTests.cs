using System.Linq;
using ExcelXml.Core.Models;
using ExcelXml.Core.Validation;
using Xunit;

namespace ExcelXml.Core.Tests;

public class ResponsibleValidatorTests
{
    [Fact]
    public void Validator_ReturnsSuccess_ForValidResponsible()
    {
        var responsible = new Responsible
        {
            Nome = "João Silva",
            Cpf = "52998224725",
            Nip = "12345",
            Perfil = "AGI",
            TipoPerfilOm = "IQM"
        };

        var validator = new ResponsibleValidator();
        var result = validator.Validate(responsible);
        Assert.True(result.IsValid);
    }

    [Fact]
    public void Validator_ReturnsFailure_ForInvalidResponsible()
    {
        var responsible = new Responsible
        {
            Nome = string.Empty,
            Cpf = "11111111111",
            Perfil = string.Empty,
            TipoPerfilOm = string.Empty
        };

        var validator = new ResponsibleValidator();
        var result = validator.Validate(responsible);
        Assert.False(result.IsValid);
        Assert.Contains(result.Errors, error => error.ErrorMessage.Contains("CPF"));
    }
}
