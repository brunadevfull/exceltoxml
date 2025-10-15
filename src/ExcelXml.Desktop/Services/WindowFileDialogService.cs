using System.Threading.Tasks;
using Avalonia.Controls;

namespace ExcelXml.Desktop.Services;

public class WindowFileDialogService : IFileDialogService
{
    private readonly Window _owner;

    public WindowFileDialogService(Window owner)
    {
        _owner = owner;
    }

    public async Task<string?> OpenExcelFileAsync()
    {
        var dialog = new OpenFileDialog
        {
            AllowMultiple = false,
            Filters =
            {
                new FileDialogFilter
                {
                    Name = "Planilhas Excel",
                    Extensions = { "xlsx", "xls" }
                }
            }
        };

        var result = await dialog.ShowAsync(_owner);
        return result is { Length: > 0 } ? result[0] : null;
    }

    public async Task<string?> SaveXmlFileAsync(string suggestedName)
    {
        var dialog = new SaveFileDialog
        {
            DefaultExtension = "xml",
            InitialFileName = suggestedName,
            Filters =
            {
                new FileDialogFilter
                {
                    Name = "Arquivo XML",
                    Extensions = { "xml" }
                }
            }
        };

        return await dialog.ShowAsync(_owner);
    }
}
