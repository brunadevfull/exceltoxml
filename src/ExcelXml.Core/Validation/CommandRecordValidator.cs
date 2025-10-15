using FluentValidation;
using ExcelXml.Core.Models;

namespace ExcelXml.Core.Validation;

public class CommandRecordValidator : AbstractValidator<CommandRecord>
{
    public CommandRecordValidator()
    {
        RuleFor(record => record.Matricula)
            .NotEmpty().WithMessage("Matrícula é obrigatória")
            .Must(ValidationUtils.IsValidMatricula).WithMessage("Matrícula deve conter apenas números");

        RuleFor(record => record.Rubrica)
            .NotEmpty().WithMessage("Rubrica é obrigatória")
            .Must(ValidationUtils.IsValidRubrica).WithMessage("Rubrica deve conter 7 dígitos");

        RuleFor(record => record.Valor)
            .NotNull().WithMessage("Valor é obrigatório")
            .GreaterThanOrEqualTo(0).WithMessage("Valor deve ser um número válido");

        RuleFor(record => record.Tipo)
            .NotEmpty().WithMessage("Tipo é obrigatório")
            .Must(ValidationUtils.IsValidTipo).WithMessage("Tipo deve ser NO ou DE");

        RuleFor(record => record.Trigrama)
            .NotEmpty().WithMessage("Trigrama é obrigatório")
            .Must(ValidationUtils.IsValidTrigrama).WithMessage("Trigrama deve conter 3 caracteres");
    }
}
