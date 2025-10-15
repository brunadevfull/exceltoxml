using FluentValidation;

namespace ExcelXml.Core.Validation;

public class FolhaValidator : AbstractValidator<string>
{
    public FolhaValidator()
    {
        RuleFor(f => f)
            .NotEmpty().WithMessage("Folha é obrigatória")
            .Must(ValidationUtils.IsValidFolha)
            .WithMessage("Folha deve estar no formato MMAAAA");
    }
}
