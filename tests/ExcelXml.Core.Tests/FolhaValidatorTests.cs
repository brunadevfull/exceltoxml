using ExcelXml.Core.Validation;
using Xunit;

namespace ExcelXml.Core.Tests;

public class FolhaValidatorTests
{
    [Fact]
    public void Validator_ReturnsSuccess_ForValidFolha()
    {
        var validator = new FolhaValidator();
        var result = validator.Validate("012025");
        Assert.True(result.IsValid);
    }

    [Fact]
    public void Validator_ReturnsFailure_ForInvalidFolha()
    {
        var validator = new FolhaValidator();
        var result = validator.Validate("132025");
        Assert.False(result.IsValid);
    }
}
