using CommunityToolkit.Mvvm.ComponentModel;
using ExcelXml.Core.Models;
using ExcelXml.Core.Validation;

namespace ExcelXml.Desktop.ViewModels;

public partial class ResponsibleDialogViewModel : ObservableObject
{
    public ResponsibleDialogViewModel(string title, Responsible responsible)
    {
        DialogTitle = title;
        Responsible = responsible;
    }

    public string DialogTitle { get; }

    public Responsible Responsible { get; }

    [ObservableProperty]
    [NotifyPropertyChangedFor(nameof(HasValidationMessage))]
    private string? validationMessage;

    public bool HasValidationMessage => !string.IsNullOrWhiteSpace(ValidationMessage);

    public bool Validate()
    {
        Responsible.Normalize();

        if (string.IsNullOrWhiteSpace(Responsible.Nome))
        {
            ValidationMessage = "Informe o nome.";
            return false;
        }

        if (!ValidationUtils.IsValidCpf(Responsible.Cpf))
        {
            ValidationMessage = "CPF deve conter 11 dígitos válidos.";
            return false;
        }

        if (string.IsNullOrWhiteSpace(Responsible.Nip))
        {
            ValidationMessage = "Informe o NIP.";
            return false;
        }

        if (string.IsNullOrWhiteSpace(Responsible.Perfil))
        {
            ValidationMessage = "Informe o perfil.";
            return false;
        }

        if (string.IsNullOrWhiteSpace(Responsible.TipoPerfilOm))
        {
            ValidationMessage = "Informe o tipo de perfil OM.";
            return false;
        }

        ValidationMessage = null;
        return true;
    }
}
