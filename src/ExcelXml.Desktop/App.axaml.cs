using Avalonia;
using Avalonia.Controls.ApplicationLifetimes;
using Avalonia.Markup.Xaml;
using ExcelXml.Core.Services;
using ExcelXml.Desktop.ViewModels;
using ExcelXml.Desktop.Views;

namespace ExcelXml.Desktop;

public partial class App : Application
{
    public override void Initialize()
    {
        AvaloniaXamlLoader.Load(this);
    }

    public override void OnFrameworkInitializationCompleted()
    {
        if (ApplicationLifetime is IClassicDesktopStyleApplicationLifetime desktop)
        {
            var dataManager = new DataManager();
            var viewModel = new MainWindowViewModel(dataManager, new ExcelProcessor(), new XmlGenerator());
            var mainWindow = new MainWindow
            {
                DataContext = viewModel
            };

            desktop.MainWindow = mainWindow;
        }

        base.OnFrameworkInitializationCompleted();
    }
}
