using System;
using System.Linq;
using Avalonia.Controls;
using Avalonia.Input;
using Avalonia.Interactivity;
using ExcelXml.Core.Models;
using ExcelXml.Desktop.Services;
using ExcelXml.Desktop.ViewModels;

namespace ExcelXml.Desktop.Views;

public partial class MainWindow : Window
{
    private Border? _dropBorder;

    public MainWindow()
    {
        InitializeComponent();
        _dropBorder = this.FindControl<Border>("DropBorder");
        Opened += OnOpened;
    }

    private void OnOpened(object? sender, EventArgs e)
    {
        if (DataContext is MainWindowViewModel viewModel)
        {
            viewModel.SetDialogService(new WindowFileDialogService(this));
        }
    }

    private void OnDragOver(object? sender, DragEventArgs e)
    {
        if (_dropBorder is not null && !_dropBorder.Classes.Contains("dragover"))
        {
            _dropBorder.Classes.Add("dragover");
        }

        e.DragEffects = DragDropEffects.Copy;
        e.Handled = true;
    }

    private void OnDragLeave(object? sender, DragEventArgs e)
    {
        _dropBorder?.Classes.Remove("dragover");
    }

    private async void OnDrop(object? sender, DragEventArgs e)
    {
        _dropBorder?.Classes.Remove("dragover");

        if (DataContext is not MainWindowViewModel viewModel)
        {
            return;
        }

        var file = e.Data.GetFileNames()?.FirstOrDefault();
        if (string.IsNullOrWhiteSpace(file))
        {
            return;
        }

        await viewModel.HandleDroppedFileAsync(file);
    }

    private async void OnAddResponsible(object? sender, RoutedEventArgs e)
    {
        if (DataContext is not MainWindowViewModel viewModel)
        {
            return;
        }

        var dialog = new ResponsibleDialog
        {
            DataContext = new ResponsibleDialogViewModel("Novo responsável", new Responsible())
        };

        var result = await dialog.ShowDialog<Responsible?>(this);
        if (result is not null)
        {
            await viewModel.AddResponsibleAsync(result);
        }
    }

    private async void OnEditResponsible(object? sender, RoutedEventArgs e)
    {
        if (DataContext is not MainWindowViewModel viewModel)
        {
            return;
        }

        var selected = viewModel.SelectedResponsible;
        if (selected?.Id is null)
        {
            return;
        }

        var responsible = await viewModel.GetResponsibleByIdAsync(selected.Id.Value);
        if (responsible is null)
        {
            return;
        }

        var dialog = new ResponsibleDialog
        {
            DataContext = new ResponsibleDialogViewModel("Editar responsável", responsible)
        };

        var result = await dialog.ShowDialog<Responsible?>(this);
        if (result is not null)
        {
            await viewModel.UpdateResponsibleAsync(result);
        }
    }

    private async void OnRemoveResponsible(object? sender, RoutedEventArgs e)
    {
        if (DataContext is not MainWindowViewModel viewModel)
        {
            return;
        }

        var selected = viewModel.SelectedResponsible;
        if (selected is null)
        {
            return;
        }

        await viewModel.RemoveResponsibleAsync(selected);
    }
}
