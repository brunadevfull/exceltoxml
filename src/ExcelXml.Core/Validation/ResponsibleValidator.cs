using FluentValidation;
using ExcelXml.Core.Models;

namespace ExcelXml.Core.Validation;

public class ResponsibleValidator : AbstractValidator<Responsible>
{
    public ResponsibleValidator()
    {
        RuleFor(r => r.Nome)
            .NotEmpty().WithMessage("Nome é obrigatório");

        RuleFor(r => r.Cpf)
            .Must(ValidationUtils.IsValidCpf)
            .WithMessage("CPF inválido");

        RuleFor(r => r.Perfil)
            .NotEmpty().WithMessage("Perfil é obrigatório");

        RuleFor(r => r.TipoPerfilOm)
            .NotEmpty().WithMessage("Tipo de perfil é obrigatório");
    }
}
