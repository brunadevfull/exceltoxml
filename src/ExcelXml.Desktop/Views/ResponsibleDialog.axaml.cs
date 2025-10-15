using Avalonia.Controls;
using Avalonia.Interactivity;
using ExcelXml.Core.Models;
using ExcelXml.Desktop.ViewModels;

namespace ExcelXml.Desktop.Views;

public partial class ResponsibleDialog : Window
{
    public ResponsibleDialog()
    {
        InitializeComponent();
    }

    private void OnCancel(object? sender, RoutedEventArgs e)
    {
        Close(null);
    }

    private void OnSave(object? sender, RoutedEventArgs e)
    {
        if (DataContext is not ResponsibleDialogViewModel viewModel)
        {
            Close(null);
            return;
        }

        if (!viewModel.Validate())
        {
            return;
        }

        Close(viewModel.Responsible);
    }
}
