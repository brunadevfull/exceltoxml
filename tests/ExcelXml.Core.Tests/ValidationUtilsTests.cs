using ExcelXml.Core.Validation;
using Xunit;

namespace ExcelXml.Core.Tests;

public class ValidationUtilsTests
{
    [Theory]
    [InlineData("52998224725", true)]
    [InlineData("39053344705", true)]
    [InlineData("11111111111", false)]
    [InlineData("123", false)]
    public void IsValidCpf_ReturnsExpectedResult(string cpf, bool expected)
    {
        Assert.Equal(expected, ValidationUtils.IsValidCpf(cpf));
    }

    [Theory]
    [InlineData("122025", true)]
    [InlineData("002000", false)]
    [InlineData("132025", false)]
    [InlineData("ab2025", false)]
    public void IsValidFolha_ReturnsExpectedResult(string folha, bool expected)
    {
        Assert.Equal(expected, ValidationUtils.IsValidFolha(folha));
    }

    [Theory]
    [InlineData("1208000", true)]
    [InlineData("120800", false)]
    [InlineData("ABC8000", false)]
    public void IsValidRubrica_ReturnsExpectedResult(string rubrica, bool expected)
    {
        Assert.Equal(expected, ValidationUtils.IsValidRubrica(rubrica));
    }

    [Theory]
    [InlineData("NO", true)]
    [InlineData("DE", true)]
    [InlineData("XX", false)]
    public void IsValidTipo_ReturnsExpectedResult(string tipo, bool expected)
    {
        Assert.Equal(expected, ValidationUtils.IsValidTipo(tipo));
    }

    [Theory]
    [InlineData("BAA", true)]
    [InlineData("B1A", false)]
    [InlineData("AB", false)]
    public void IsValidTrigrama_ReturnsExpectedResult(string trigrama, bool expected)
    {
        Assert.Equal(expected, ValidationUtils.IsValidTrigrama(trigrama));
    }
}
